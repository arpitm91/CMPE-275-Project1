import grpc
from concurrent import futures
import time
import configs.data_center_info as data_center_info
import os
import sys
import threading

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "protos"))
from utils.file_utils import get_file_seqs
from utils.file_utils import get_max_file_seqs
from utils.file_utils import write_file_chunks
import file_transfer_pb2 as common_proto
import file_transfer_pb2_grpc as common_proto_rpc
import raft_pb2 as our_proto
import raft_pb2_grpc as our_proto_rpc
from client.client_download import run as download_as_client

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class RaftService(our_proto_rpc.RaftServiceServicer):
    def DataCenterHeartbeat(self, request, context):
        reply = our_proto.Empty()
        return reply

    def ReplicationInitiate(self, request, context):
        from_datacenter_ip = request.fromDatacenter.ip
        from_datacenter_port = request.fromDatacenter.port
        chunk = request.chunkId
        filename = request.fileName
        global FOLDER

        print("Initiating replication of :", filename, "chunk :", chunk, "from ip:", from_datacenter_ip, ",port :",
              from_datacenter_port)
        threading.Thread(target=download_as_client,
                         args=("", "", filename, chunk, FOLDER, from_datacenter_ip, from_datacenter_port)).start()
        reply = our_proto.Ack()
        reply.id = 1
        return reply

    def RaftHeartbit(self, request, context):
        pass

    def RequestVote(self, request, context):
        pass

    def AddFileLog(self, request, context):
        pass

    def AddDataCenter(self, request, context):
        pass

    def AddProxy(self, request, context):
        pass

    def ProxyHeartbeat(self, request, context):
        pass

    def FileUploadCompleted(self, request, context):
        pass

    def GetChunkLocationInfo(self, request, context):
        pass

    def GetChunkUploadInfo(self, request, context):
        pass


class DataCenterServer(common_proto_rpc.DataTransferServiceServicer):
    def UploadFile(self, request_iterator, context):
        file_name = ""
        chunk_id = None
        seq_num = 0
        seq_max = float('inf')
        for request in request_iterator:
            file_name = request.fileName
            chunk_id = request.chunkId
            seq_num = request.seqNum
            seq_max = request.seqMax
            file_path = os.path.join(FOLDER, file_name)
            print("Received... File:", file_name, "Chunk:", chunk_id, ", Seq: ", seq_num, "/", seq_max)
            if seq_num == 0:
                print("Upload request received for", file_name, "chunk", chunk_id)
                if os.path.isfile(os.path.join(file_path, str(chunk_id))):
                    os.remove(os.path.join(file_path, str(chunk_id)))
            write_file_chunks(request, FOLDER)

        my_reply = common_proto.FileInfo()
        my_reply.fileName = file_name

        if chunk_id is not None:
            if seq_num == seq_max - 1:
                # full chunk received
                upload_completed(file_name, chunk_id, True)
            else:
                # full chunk not received
                upload_completed(file_name, chunk_id, False)

        return my_reply

    def DownloadChunk(self, request, context):
        file_name = request.fileName
        chunk_id = request.chunkId
        start_seq_num = request.startSeqNum
        print("Download request received for", file_name, "chunk", chunk_id, "seq", start_seq_num)

        chunk_path = os.path.join(FOLDER, file_name, str(chunk_id))
        current_seq = 0

        if os.path.isfile(chunk_path):
            total_seq = get_max_file_seqs(chunk_path)

            for chunk_buffer in get_file_seqs(chunk_path):
                if current_seq >= start_seq_num:
                    reply = common_proto.FileMetaData()
                    reply.fileName = file_name
                    reply.chunkId = chunk_id
                    reply.data = chunk_buffer
                    reply.seqNum = current_seq
                    reply.seqMax = total_seq
                    print("Sent...", file_name, "chunk", chunk_id, "seq", current_seq)
                    current_seq += 1
                    # time.sleep(1)
                    yield reply
                else:
                    current_seq += 1
        else:
            reply = common_proto.FileMetaData()
            reply.fileName = file_name
            reply.chunkId = chunk_id
            reply.data = str.encode("")
            reply.seqNum = 0
            reply.seqMax = 0
            print("Could not find", file_name, "chunk", chunk_id, "seq", start_seq_num)
            upload_completed(file_name, chunk_id, False)
            return reply

        print("Download request completed for", file_name, "chunk", chunk_id, "seq", start_seq_num)
        upload_completed(file_name, chunk_id, True)


def start_server(username, port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    common_proto_rpc.add_DataTransferServiceServicer_to_server(DataCenterServer(), server)
    our_proto_rpc.add_RaftServiceServicer_to_server(RaftService(), server)
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    print("server started at port : ", port, "username :", username)
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


def upload_completed(file_name, chunk_id, is_success):
    global raft_ip, raft_port, my_ip, my_port
    with grpc.insecure_channel(raft_ip + ':' + raft_port) as channel:
        stub = our_proto_rpc.RaftServiceStub(channel)

        request = our_proto.UploadCompleteFileInfo()

        request.fileName = file_name
        request.chunkUploadInfo.chunkId = chunk_id
        request.chunkUploadInfo.uploadedDatacenter.ip = my_ip
        request.chunkUploadInfo.uploadedDatacenter.port = my_port
        request.isSuccess = is_success

        while True:
            try:
                stub.FileUploadCompleted(request)
                print("Upload completed sent to raft ip :", raft_ip, ",port :", raft_port, ", success:", is_success)
                break
            except grpc.RpcError:
                print("Could not sent upload complete to raft ip :", raft_ip, ",port :", raft_port, ", success:", is_success)
                time.sleep(2)


def register_dc():
    global raft_ip, raft_port, my_ip, my_port
    with grpc.insecure_channel(raft_ip + ':' + raft_port) as channel:
        stub = our_proto_rpc.RaftServiceStub(channel)

        request = our_proto.DataCenterInfo()
        request.ip = my_ip
        request.port = my_port
        while True:
            try:
                stub.AddDataCenter(request)
                print("Registered with raft ip :", raft_ip, ",port :", raft_port)
                break
            except grpc.RpcError:
                print("Could not register with raft ip :", raft_ip, ",port :", raft_port)
                time.sleep(2)


# python3 datacenter.py <dc_name from data_center_info> <raft ip to register to> <raft port to register to>
if __name__ == '__main__':
    data_center_name = sys.argv[1]

    my_ip = data_center_info.data_center[data_center_name]["ip"]
    my_port = data_center_info.data_center[data_center_name]["port"]
    FOLDER = data_center_info.data_center[data_center_name]["folder"]
    raft_ip = sys.argv[2]
    raft_port = sys.argv[3]

    threading.Thread(target=start_server, args=(data_center_name, my_port)).start()

    threading.Thread(target=register_dc, args=()).start()

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        exit()
