import threading
import random
import pprint
import grpc
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "protos"))
from utils.file_utils import write_file_chunks
import file_transfer_pb2 as file_transfer
import file_transfer_pb2_grpc as rpc


def download_chunk(file_name, chunk_num, proxy_address, proxy_port):
    with grpc.insecure_channel(proxy_address + ':' + proxy_port) as channel:
        stub = rpc.DataTransferServiceStub(channel)
        request = file_transfer.ChunkInfo()
        request.fileName = file_name
        request.chunkId = chunk_num
        request.startSeqNum = 0

        for response in stub.DownloadChunk(request):
            print("Response received: ",response.seqNum,"/",response.seqMax)
            write_file_chunks(response)



def run(argv):
    with grpc.insecure_channel(str(argv[1]) + ':' + str(argv[2])) as channel:
        stub = rpc.DataTransferServiceStub(channel)
        file_name = str(argv[3])
        request = file_transfer.FileInfo()
        request.fileName = file_name

        file_location_info = stub.RequestFileInfo(request):
        print("Response received: ")
        pprint.pprint(file_location_info)

    for chunk_num in file_location_info["maxChunks"]:
        proxies = file_location_info["lstProxy"]

        random_proxy_index = random.randint(len(proxies))
        # proxy
        proxy_address = proxies[random_proxy_index]["ip"]
        proxy_port = proxies[random_proxy_index]["port"]

        threading.Thread(target=download_chunk, args=(file_name, chunk_num, proxy_address, proxy_port),
                         daemon=True).start()


# python3 client.py <raft_ip> <raft_port> <filename>
if __name__ == '__main__':
    run(sys.argv[:])
