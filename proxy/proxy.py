import sys
import os
import time
from concurrent import futures
import queue

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

from connections.connections import proxy as proxy_info

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
GRPC_TIMEOUT = 1  # grpc calls time out after 1 sec


def file_upload_iterator(common_q, data_center_address, data_center_port):
    while True:
        common_q_front = common_q.get(block=True)
        if common_q_front is None:
            break
        print("Sending to DataCenter:", data_center_address + ":" + data_center_port, "Filename",
              common_q_front.fileName, "Chunk: ", common_q_front.chunkId, ", Seq: ",
              common_q_front.seqNum, "/", common_q_front.seqMax)
        yield common_q_front

    return


def upload_to_data_center(common_queue, file_name, chunk_id):
    # Get upload information
    request = our_proto.RequestChunkInfo()
    request.fileName = file_name
    request.chunkId = chunk_id
    while True:
        random_raft = get_raft_node()
        with grpc.insecure_channel(random_raft["ip"] + ':' + random_raft["port"]) as channel:
            stub = our_proto_rpc.RaftServiceStub(channel)
            try:
                raft_response = stub.GetChunkUploadInfo(request, timeout=GRPC_TIMEOUT)
                print("Got raft response with raft ip :", random_raft["ip"], ",port :", random_raft["port"])
                break
            except grpc.RpcError:
                print("Could not get response with raft ip :", random_raft["ip"], ",port :",
                      random_raft["port"])
                time.sleep(0.1)

    # data_center
    data_center_address = raft_response.lstDataCenter[0].ip
    data_center_port = raft_response.lstDataCenter[0].port
    print("data center for upload of file:", file_name, "chunk:", chunk_id, "data center:",
          data_center_address + ":" + data_center_port)

    with grpc.insecure_channel(data_center_address + ':' + data_center_port) as channel:
        stub = common_proto_rpc.DataTransferServiceStub(channel)
        stub.UploadFile(file_upload_iterator(common_queue, data_center_address, data_center_port))


def download_chunk_to_queue(common_queue, file_name, chunk_num, start_seq_num, data_center_address, data_center_port):
    print("requesting for :", file_name, "chunk no :", chunk_num, "from", data_center_address, ":", data_center_port)

    with grpc.insecure_channel(data_center_address + ':' + data_center_port) as channel:
        stub = common_proto_rpc.DataTransferServiceStub(channel)
        request = common_proto.ChunkInfo()
        request.fileName = file_name
        request.chunkId = chunk_num
        request.startSeqNum = start_seq_num
        try:
            for response in stub.DownloadChunk(request):
                print("Response received: ", response.seqNum, "/", response.seqMax)
                common_queue.put(response)
        except grpc.RpcError:
            print("Failed to connect to data center !!")
            common_queue.put(None)

        print("request completed for :", file_name, "chunk no :", chunk_num, "from", data_center_address, ":",
              data_center_port)
        common_queue.put(None)


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
            with grpc.insecure_channel(random_raft["ip"] + ':' + random_raft["port"]) as channel:
                stub = our_proto_rpc.RaftServiceStub(channel)
                try:
                    raft_response = stub.GetChunkLocationInfo(request, timeout=GRPC_TIMEOUT)
                    print("Got raft response with raft ip :", random_raft["ip"], ",port :", random_raft["port"])
                    break
                except grpc.RpcError:
                    print("Could not get response with raft ip :", random_raft["ip"], ",port :", random_raft["port"])
                    time.sleep(0.1)

        if not raft_response.isChunkFound:
            return

        # queue terminates on None
        common_q = queue.Queue()
        random_data_center_index = random.randint(0, len(raft_response.lstDataCenter) - 1)
        # data_center
        data_center_address = raft_response.lstDataCenter[random_data_center_index].ip
        data_center_port = raft_response.lstDataCenter[random_data_center_index].port
        print("data center selected", data_center_address, data_center_port)

        threading.Thread(target=download_chunk_to_queue, args=(
            common_q, file_name, chunk_id, start_seq_num, data_center_address, data_center_port)).start()

        while True:
            common_q_front = common_q.get(block=True)
            if common_q_front is None:
                break
            yield common_q_front

        return

    def UploadFile(self, request_iterator, context):
        file_name = ""
        # queue terminates on None
        common_q = queue.Queue()
        for request in request_iterator:
            file_name = request.fileName
            chunk_id = request.chunkId
            seq_num = request.seqNum
            seq_max = request.seqMax
            print("Received... File:", file_name, "Chunk:", chunk_id, ", Seq: ", seq_num, "/", seq_max)
            common_q.put(request)
            if seq_num == 0:
                uploading_to_dc_thread = threading.Thread(target=upload_to_data_center,
                                                          args=(common_q, file_name, chunk_id))
                uploading_to_dc_thread.start()

        common_q.put(None)

        uploading_to_dc_thread.join()

        my_reply = common_proto.FileInfo()
        my_reply.fileName = file_name

        return my_reply


def start_server(username, port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    common_proto_rpc.add_DataTransferServiceServicer_to_server(DataCenterServer(), server)
    our_proto_rpc.add_ProxyServiceServicer_to_server(ProxyService(), server)
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    print("server started at port : ", port, "username :", username)
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


def register_proxy():
    global my_ip, my_port
    while True:
        random_raft = get_raft_node()
        with grpc.insecure_channel(random_raft["ip"] + ':' + random_raft["port"]) as channel:
            stub = our_proto_rpc.RaftServiceStub(channel)

            request = our_proto.ProxyInfoRaft()
            request.ip = my_ip
            request.port = my_port
            try:
                stub.AddProxy(request)
                print("Registered with raft ip :", random_raft["ip"], ",port :", random_raft["port"])
                break
            except grpc.RpcError:
                print("Could not register with raft ip :", random_raft["ip"], ",port :", random_raft["port"])
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
