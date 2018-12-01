import sys
import os
import time
from concurrent import futures
import queue
import itertools

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "protos"))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "utils"))

import threading
import grpc
import random
import file_transfer_pb2 as common_proto
import file_transfer_pb2_grpc as common_proto_rpc
import raft_pb2 as our_proto
import raft_pb2_grpc as our_proto_rpc
from common_utils import get_raft_node
from utils.input_output_util import log_info

from connections.connections import proxy as proxy_info

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
GRPC_TIMEOUT = 1  # grpc calls time out after 1 sec

class ProxyService(our_proto_rpc.ProxyServiceServicer):
    def ProxyHeartbeat(self, request, context):
        return our_proto.Empty()


class DataCenterServer(common_proto_rpc.DataTransferServiceServicer):
    def DownloadChunk(self, request, context):
        file_name = request.fileName
        chunk_id = request.chunkId
        start_seq_num = request.startSeqNum

        request = our_proto.RequestChunkInfo()
        request.fileName = file_name
        request.chunkId = chunk_id

        while True:
            random_raft = get_raft_node()
            stub = our_proto_rpc.RaftServiceStub(grpc.insecure_channel(random_raft["ip"] + ':' + random_raft["port"]))
            try:
                raft_response = stub.GetChunkLocationInfo(request, timeout=GRPC_TIMEOUT)
                log_info("Got raft response with raft ip :", random_raft["ip"], ",port :", random_raft["port"])
                break
            except grpc.RpcError:
                log_info("Could not get response with raft ip :", random_raft["ip"], ",port :", random_raft["port"])
                time.sleep(0.1)

        if raft_response.isChunkFound:
            random_data_center_index = random.randint(0, len(raft_response.lstDataCenter) - 1)
            # data_center
            data_center_address = raft_response.lstDataCenter[random_data_center_index].ip
            data_center_port = raft_response.lstDataCenter[random_data_center_index].port
            log_info("data center selected", data_center_address, data_center_port)
            log_info("requesting for :", file_name, "chunk no :", chunk_id, "from", data_center_address, ":",
                     data_center_port)

            stub = common_proto_rpc.DataTransferServiceStub(grpc.insecure_channel(data_center_address + ':' + data_center_port))
            request = common_proto.ChunkInfo()
            request.fileName = file_name
            request.chunkId = chunk_id
            request.startSeqNum = start_seq_num
            for response in stub.DownloadChunk(request):
                log_info("Response received: ", response.seqNum, "/", response.seqMax)
                yield response

            log_info("request completed for :", file_name, "chunk no :", chunk_id, "from", data_center_address, ":",
                     data_center_port)


    def UploadFile(self, request_iterator, context):
        request = request_iterator.next()
        # Get upload information
        raft_request = our_proto.RequestChunkInfo()
        raft_request.fileName = request.fileName
        raft_request.chunkId = request.chunkId
        file_name = request.fileName
        while True:
            random_raft = get_raft_node()
            raft_stub = our_proto_rpc.RaftServiceStub(grpc.insecure_channel(random_raft["ip"] + ':' + random_raft["port"]))
            try:
                raft_response = raft_stub.GetChunkUploadInfo(raft_request, timeout=GRPC_TIMEOUT)
                log_info("Got raft response with raft ip :", random_raft["ip"], ",port :",
                         random_raft["port"])
                break
            except grpc.RpcError:
                log_info("Could not get response with raft ip :", random_raft["ip"], ",port :",
                         random_raft["port"])
                time.sleep(0.1)

        # data_center
        data_center_address = raft_response.lstDataCenter[0].ip
        data_center_port = raft_response.lstDataCenter[0].port
        log_info("data center for upload of file:", file_name, "chunk:", request.chunkId, "data center:",
                 data_center_address + ":" + data_center_port)
        stub = common_proto_rpc.DataTransferServiceStub(
            grpc.insecure_channel(data_center_address + ':' + data_center_port))
        log_info("Received... File:", file_name, "Chunk:", request.chunkId, ", Seq: ", request.seqNum, "/",
                 request.seqMax)
        stub.UploadFile(itertools.chain([request], request_iterator))

        my_reply = common_proto.FileInfo()
        my_reply.fileName = file_name

        return my_reply


def start_server(username, port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    common_proto_rpc.add_DataTransferServiceServicer_to_server(DataCenterServer(), server)
    our_proto_rpc.add_ProxyServiceServicer_to_server(ProxyService(), server)
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    log_info("server started at port : ", port, "username :", username)
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


def register_proxy():
    global my_ip, my_port
    while True:
        random_raft = get_raft_node()
        stub = our_proto_rpc.RaftServiceStub(grpc.insecure_channel(random_raft["ip"] + ':' + random_raft["port"]))

        request = our_proto.ProxyInfoRaft()
        request.ip = my_ip
        request.port = my_port
        try:
            response = stub.AddProxy(request)
            if response.id != -1:
                log_info("Registered with raft ip :", random_raft["ip"], ",port :", random_raft["port"])
                break
        except grpc.RpcError:
            log_info("Could not register with raft ip :", random_raft["ip"], ",port :", random_raft["port"])
        time.sleep(0.1)


# python3 proxy.py <proxy_name from proxy_center_info>
if __name__ == '__main__':
    proxy_name = sys.argv[1]

    my_ip = proxy_info[proxy_name]["ip"]
    my_port = proxy_info[proxy_name]["port"]

    threading.Thread(target=start_server, args=(proxy_name, my_port)).start()

    threading.Thread(target=register_proxy, args=()).start()

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        exit()
