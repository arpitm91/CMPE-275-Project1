import pprint
import grpc
import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "protos"))

import protos.file_transfer_pb2 as file_transfer
import protos.file_transfer_pb2_grpc as rpc
from utils.common_utils import get_raft_node
from utils.input_output_util import log_info

THREAD_POOL_SIZE = 1
next_sequence_to_download = []
maximum_number_of_sequences = []


def run(raft_ip, raft_port, file_name, downloads_folder="Downloads"):
    with grpc.insecure_channel(raft_ip + ':' + raft_port) as channel:
        stub = rpc.DataTransferServiceStub(channel)
        request = file_transfer.FileInfo()
        request.fileName = file_name

        file_location_info = stub.RequestFileInfo(request)
        log_info("Response received: ")
        pprint.pprint(file_location_info)

    proxies = []
    for proxy in file_location_info.lstProxy:
        proxies.append(proxy)

    if file_location_info.isFileFound:
        with open(downloads_folder + "/" + file_name, 'wb') as f:
            with grpc.insecure_channel(proxies[0].ip + ':' + proxies[0].port) as channel:
                stub = rpc.DataTransferServiceStub(channel)
                request = file_transfer.ChunkInfo()
                request.fileName = file_name
                request.startSeqNum = 0
                for chunk_num in range(file_location_info.maxChunks):
                    request.chunkId = chunk_num
                    for response in stub.DownloadChunk(request):
                        f.write(response.data)


# python3 client_download.py <filename>
if __name__ == '__main__':
    start_time = time.time()
    while True:
        random_raft = get_raft_node()
        try:
            log_info("Client connected to raft node :", random_raft["ip"], random_raft["port"])
            run(random_raft["ip"], random_raft["port"], str(sys.argv[1]))
            break
        except grpc.RpcError:
            log_info("Client could not connect with raft ip :", random_raft["ip"], ",port :", random_raft["port"])
            time.sleep(2)
    print("--- %s seconds ---" % (time.time() - start_time))
