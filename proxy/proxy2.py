import sys
import os
import time
from concurrent import futures

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
from raft.configs.connections import connections
import configs.proxy_info as proxy_info

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

def getRaftNode():
    available_raft_nodes = []
    for key in connections.keys():
        if key[:4] == "raft":
            available_raft_nodes.append((connections[key]))

    random_raft_index = random.randint(0, len(available_raft_nodes) - 1)

    return available_raft_nodes[random_raft_index]["own"]


class ProxyServer(common_proto_rpc.DataTransferServiceServicer,our_proto_rpc.RaftServiceServicer):
    def ProxyHeartbeat(self, request, context):
        reply = our_proto.Empty()
        return reply

    def DownloadChunk(self, request, context):
        pass

    def UploadFile(self, request_iterator, context):
        pass


def start_server(username, port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    common_proto_rpc.add_DataTransferServiceServicer_to_server(ProxyServer(), server)
    our_proto_rpc.add_RaftServiceServicer_to_server(ProxyServer(), server)
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
        random_raft = getRaftNode()
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
                time.sleep(2)


# python3 proxy2.py <proxy_name from proxy_center_info>
if __name__ == '__main__':
    proxy_name = sys.argv[1]

    my_ip = proxy_info.proxy[proxy_name]["ip"]
    my_port = proxy_info.proxy[proxy_name]["port"]

    threading.Thread(target=start_server, args=(proxy_name, my_port)).start()

    threading.Thread(target=register_proxy, args=()).start()

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        exit()
