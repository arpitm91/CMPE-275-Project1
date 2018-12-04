import grpc
import sys
import os
import time
import pprint

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "protos"))

import protos.file_transfer_pb2 as file_transfer
import protos.file_transfer_pb2_grpc as rpc
from utils.input_output_util import log_info

THREAD_POOL_SIZE = 4
next_sequence_to_download = []
maximum_number_of_sequences = []


def run(raft_ip, raft_port, file_name):
    stub = rpc.DataTransferServiceStub(grpc.insecure_channel(raft_ip + ':' + raft_port))
    request = file_transfer.FileInfo()
    request.fileName = file_name

    file_location_info = stub.RequestFileInfo(request)
    # pprint.pprint(file_location_info)

    if file_location_info.isFileFound:
        proxies = []
        for proxy in file_location_info.lstProxy:
            proxies.append(proxy)

        stub = rpc.DataTransferServiceStub(grpc.insecure_channel(proxies[0].ip + ':' + proxies[0].port))
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "Downloads",
                               str(time.time()) + "_" + file_name), 'wb') as f:
            for chunk in range(file_location_info.maxChunks):
                request = file_transfer.ChunkInfo()
                request.fileName = file_name
                request.chunkId = chunk
                request.startSeqNum = 0
                for response in stub.DownloadChunk(request):
                    f.write(response.data)
    else:
        log_info("File not found", file_name)


# python3 client_download.py <filename> <no of downloads>
if __name__ == '__main__':
    start_time = time.time()
    no_of_downloads = 1
    if len(sys.argv) >= 3:
        no_of_downloads = int(sys.argv[2])

    print("sdvdsvdsv", no_of_downloads, len(sys.argv))

    for i in range(no_of_downloads):
        if i % 10 == 0:
            print(i)
        random_raft = {"ip": "10.0.10.1", "port": "10000"}
        run(random_raft["ip"], random_raft["port"], str(sys.argv[1]))

    print("--- %s seconds ---" % (time.time() - start_time))
