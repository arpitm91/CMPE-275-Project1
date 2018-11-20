import pprint
import grpc
import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "protos"))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "utils"))

import file_transfer_pb2 as file_transfer
import file_transfer_pb2_grpc as file_transfer_rpc
from common_utils import get_raft_node


def run(raft_ip, raft_port):
    with grpc.insecure_channel(raft_ip + ':' + raft_port) as channel:
        stub = file_transfer_rpc.DataTransferServiceStub(channel)

        request = file_transfer.RequestFileList()
        request.isClient = True

        response = stub.ListFiles(request)

        print("Got list of files: ")
        pprint.pprint(response)


# python3 client_file_list.py
if __name__ == '__main__':
    while True:
        random_raft = get_raft_node()
        try:
            print("Client connected to raft node :", random_raft["ip"], random_raft["port"])
            run(random_raft["ip"], random_raft["port"])
            break
        except grpc.RpcError:
            print("Client could not connect with raft ip :", random_raft["ip"], ",port :", random_raft["port"])
            time.sleep(2)
