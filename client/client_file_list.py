import threading
import random
import pprint
import grpc
import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "protos"))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "utils"))

import file_utils
import raft_pb2 as raft_proto
import raft_pb2_grpc as raft_rpc
import file_transfer_pb2 as file_transfer
import file_transfer_pb2_grpc as file_transfer_rpc

def run(argv):
    with grpc.insecure_channel(str(argv[1]) + ':' + str(argv[2])) as channel:
        stub = file_transfer_rpc.DataTransferServiceStub(channel)

        request = file_transfer.RequestFileList()
        request.isClient = True

        response = stub.ListFiles(request)

        print("Got list of files: ")
        pprint.pprint(response)


# python3 client.py <raft_ip> <raft_port> <filename>
if __name__ == '__main__':
    run(sys.argv[:])
