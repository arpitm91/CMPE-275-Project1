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


class DataCenterServer(common_proto_rpc.DataTransferServiceServicer):
    def UploadFile(self, request_iterator, context):
        file_name = ""
        for request in request_iterator:
            file_name = request.fileName
            chunk_id = request.chunkId
            seq_num = request.seqNum
            file_path = os.path.join(FOLDER, file_name)
            print("Received... Chunk: ", chunk_id, ", Seq: ", seq_num)
            if seq_num == 0:
                print("Upload request received for", file_name, "chunk", chunk_id)
                if os.path.isfile(os.path.join(file_path, str(chunk_id))):
                    os.remove(os.path.join(file_path, str(chunk_id)))
            write_file_chunks(request, FOLDER)

        my_reply = common_proto.FileInfo()
        my_reply.fileName = file_name

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
            return reply

        print("Download request completed for", file_name, "chunk", chunk_id, "seq", start_seq_num)


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


def register_dc(raft_ip, raft_port, ip, port):
    with grpc.insecure_channel(raft_ip + ':' + raft_port) as channel:
        stub = our_proto_rpc.RaftServiceStub(channel)

        request = our_proto.DataCenterInfo()
        request.ip = ip
        request.port = port
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

    threading.Thread(target=start_server, args=(data_center_name, my_port)).start()

    threading.Thread(target=register_dc, args=(sys.argv[2], sys.argv[3], my_ip, my_port)).start()

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        exit()
