import grpc
from concurrent import futures
import time
import os
import sys
import threading
from multiprocessing import Process

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
from common_utils import get_raft_node
from connections.connections import data_center as data_center_info
from utils.input_output_util import log_info
from utils.constants import HEARTBEAT_PORT_INCREMENT

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
GRPC_TIMEOUT = 10  # grpc calls time out after 1 sec


def start_download_as_client(filename, chunk, download_folder, from_datacenter_ip, from_datacenter_port):
    download_as_client("", "", filename, chunk, download_folder, from_datacenter_ip, from_datacenter_port)
    upload_completed(filename, chunk, True)


class DataCenterService(our_proto_rpc.DataCenterServiceServicer):
    def DataCenterHeartbeat(self, request, context):
        reply = our_proto.Empty()
        return reply

    def ReplicationInitiate(self, request, context):
        from_datacenter_ip = request.fromDatacenter.ip
        from_datacenter_port = request.fromDatacenter.port
        chunk = request.chunkId
        filename = request.fileName
        global FOLDER

        log_info("Initiating replication of :", filename, "chunk :", chunk, "from ip:", from_datacenter_ip, ",port :",
                 from_datacenter_port)
        threading.Thread(target=start_download_as_client,
                         args=(filename, chunk, FOLDER, from_datacenter_ip, from_datacenter_port)).start()
        reply = our_proto.Ack()
        reply.id = 1
        return reply


class DataTransferService(common_proto_rpc.DataTransferServiceServicer):
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
                log_info("Upload request received for", file_name, "chunk", chunk_id)
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
                    log_info("Sent...", file_name, "chunk", chunk_id, "seq", current_seq)
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
            log_info("Could not find", file_name, "chunk", chunk_id, "seq", start_seq_num)
            return reply

        print("Download request completed for", file_name, "chunk", chunk_id, "seq", start_seq_num)


def start_server(username, port, workers=10):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=workers))
    common_proto_rpc.add_DataTransferServiceServicer_to_server(DataTransferService(), server)
    our_proto_rpc.add_DataCenterServiceServicer_to_server(DataCenterService(), server)
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    log_info("server started at port : ", port, "username :", username)
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


def start_heartbeat_server(username, port, workers=10):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=workers))
    our_proto_rpc.add_DataCenterServiceServicer_to_server(DataCenterService(), server)
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    log_info("server started at port : ", port, "username :", username)
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


def upload_completed(file_name, chunk_id, is_success):
    global my_ip, my_port

    request = our_proto.UploadCompleteFileInfo()
    request.fileName = file_name
    request.chunkUploadInfo.chunkId = chunk_id
    request.chunkUploadInfo.uploadedDatacenter.ip = my_ip
    request.chunkUploadInfo.uploadedDatacenter.port = my_port
    request.isSuccess = is_success

    while True:
        random_raft = {}
        try:
            random_raft = get_raft_node()
            stub = our_proto_rpc.RaftServiceStub(grpc.insecure_channel(random_raft["ip"] + ':' + random_raft["port"]))
            response = stub.FileUploadCompleted(request, timeout=GRPC_TIMEOUT)
            if response.id != -1:
                print("Upload completed sent to raft ip :", random_raft["ip"], ",port :", random_raft["port"],
                      ", success:",
                      is_success)
                break
        except grpc.RpcError:
            log_info("Could not sent upload complete to raft ip :", random_raft["ip"], ",port :", random_raft["port"],
                     ", success:",
                     is_success)
            time.sleep(0.1)


def register_dc():
    global my_ip, my_port

    request = our_proto.ProxyInfoRaft()
    request.ip = my_ip
    request.port = my_port

    while True:
        random_raft = get_raft_node()
        stub = our_proto_rpc.RaftServiceStub(grpc.insecure_channel(random_raft["ip"] + ':' + random_raft["port"]))
        try:
            response = stub.AddDataCenter(request, timeout=GRPC_TIMEOUT)
            if response.id != -1:
                log_info("Registered with raft ip :", random_raft["ip"], ",port :", random_raft["port"])
                break
            else:
                log_info("No Consensus: Could not register with raft ip :", random_raft["ip"], ",port :",
                         random_raft["port"])
        except grpc.RpcError:
            log_info("Could not register with raft ip :", random_raft["ip"], ",port :", random_raft["port"])
        time.sleep(0.1)


# python3 datacenter.py <dc_name from data_center_info>
if __name__ == '__main__':
    data_center_name = sys.argv[1]

    my_ip = data_center_info[data_center_name]["ip"]
    my_port = data_center_info[data_center_name]["port"]
    FOLDER = data_center_info[data_center_name]["folder"]

    threading.Thread(target=start_server, args=(data_center_name, my_port)).start()
    threading.Thread(target=start_heartbeat_server,
                     args=(data_center_name, str(int(my_port) + HEARTBEAT_PORT_INCREMENT), 5)).start()
    threading.Thread(target=register_dc, args=()).start()

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        exit()
