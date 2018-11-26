import pprint
import grpc
import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "protos"))

import file_transfer_pb2 as file_transfer
import file_transfer_pb2_grpc as file_transfer_rpc
from utils.common_utils import get_raft_node
from utils.input_output_util import log_info


def run(raft_ip, raft_port):
    with grpc.insecure_channel(raft_ip + ':' + raft_port) as channel:
        stub = file_transfer_rpc.DataTransferServiceStub(channel)

        request = file_transfer.RequestFileList()
        request.isClient = True

        response = stub.ListFiles(request)

        log_info("Got list of files: ")
        pprint.pprint(response)


# python3 client_file_list.py
if __name__ == '__main__':
    start_time = time.time()
    while True:
        random_raft = get_raft_node()
        try:
            log_info("Client connected to raft node :", random_raft["ip"], random_raft["port"])
            run(random_raft["ip"], random_raft["port"])
            break
        except grpc.RpcError:
            log_info("Client could not connect with raft ip :", random_raft["ip"], ",port :", random_raft["port"])
            time.sleep(2)
    print("--- %s seconds ---" % (time.time() - start_time))
