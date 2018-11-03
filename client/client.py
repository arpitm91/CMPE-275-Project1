import threading
import random
import pprint
import grpc
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "protos"))
from utils.file_utils import write_file_chunks
from utils.file_utils import merge_chunks
import file_transfer_pb2 as file_transfer
import file_transfer_pb2_grpc as rpc

threads = []


def download_chunk(file_name, chunk_num, proxy_address, proxy_port):
    print("requesting for :", file_name, "chunk no :", chunk_num, "from", proxy_address, ":", proxy_port)
    with grpc.insecure_channel(proxy_address + ':' + proxy_port) as channel:
        stub = rpc.DataTransferServiceStub(channel)
        request = file_transfer.ChunkInfo()
        request.fileName = file_name
        request.chunkId = chunk_num
        request.startSeqNum = 0

        for response in stub.DownloadChunk(request):
            print("Response received: ", response.seqNum, "/", response.seqMax)
            write_file_chunks(response, os.path.join(os.path.dirname(os.path.realpath(__file__)), "Downloads"))


def run(argv):
    with grpc.insecure_channel(str(argv[1]) + ':' + str(argv[2])) as channel:
        stub = rpc.DataTransferServiceStub(channel)
        file_name = str(argv[3])
        request = file_transfer.FileInfo()
        request.fileName = file_name

        file_location_info = stub.RequestFileInfo(request)
        print("Response received: ")
        pprint.pprint(file_location_info)

    for chunk_num in range(file_location_info.maxChunks):
        random_proxy_index = random.randint(0, len(file_location_info.lstProxy) - 1)
        # proxy
        proxy_address = file_location_info.lstProxy[random_proxy_index].ip
        proxy_port = file_location_info.lstProxy[random_proxy_index].port

        threads.append(threading.Thread(target=download_chunk, args=(file_name, chunk_num, proxy_address, proxy_port),
                                        daemon=True))
        threads[-1].start()

    for t in threads:
        t.join()

    merge_chunks(file_location_info.fileName, os.path.join(os.path.dirname(os.path.realpath(__file__)), "Downloads"), file_location_info.maxChunks)

# python3 client.py <raft_ip> <raft_port> <filename>
if __name__ == '__main__':
    run(sys.argv[:])
