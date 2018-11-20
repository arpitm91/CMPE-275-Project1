import random
import pprint
import grpc
import sys
import os
import time
from multiprocessing.dummy import Pool as ThreadPool

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "protos"))

from utils.file_utils import write_file_chunks
from utils.file_utils import merge_chunks
import protos.file_transfer_pb2 as file_transfer
import protos.file_transfer_pb2_grpc as rpc
from utils.common_utils import get_raft_node

THREAD_POOL_SIZE = 4
next_sequence_to_download = []
maximum_number_of_sequences = []


def download_chunk(file_name, chunk_num, start_seq_num, proxy_address, proxy_port, downloads_folder="Downloads"):
    print("requesting for :", file_name, "chunk no :", chunk_num, "from", proxy_address, ":", proxy_port)

    global next_sequence_to_download
    global maximum_number_of_sequences
    with grpc.insecure_channel(proxy_address + ':' + proxy_port) as channel:
        stub = rpc.DataTransferServiceStub(channel)
        request = file_transfer.ChunkInfo()
        request.fileName = file_name
        request.chunkId = chunk_num
        request.startSeqNum = start_seq_num
        try:
            for response in stub.DownloadChunk(request):
                print("Response received: Chunk", response.chunkId, "Sequence:", response.seqNum, "/", response.seqMax)
                next_sequence_to_download[chunk_num] = response.seqNum + 1
                maximum_number_of_sequences[chunk_num] = response.seqMax
                write_file_chunks(response, os.path.join(os.path.dirname(os.path.realpath(__file__)), downloads_folder))
        except grpc.RpcError:
            print("Failed to connect to data center..Retrying !!")

        print("request completed for :", file_name, "chunk no :", chunk_num, "from", proxy_address, ":", proxy_port,
              "last seq :", next_sequence_to_download[chunk_num], "max seq :", maximum_number_of_sequences[chunk_num])


def get_file_location(stub, request):
    file_location_info = stub.RequestFileInfo(request)
    print("Response received: ")
    pprint.pprint(file_location_info)
    print(file_location_info.maxChunks)
    print("is file found :", file_location_info.isFileFound)
    return file_location_info


def run(raft_ip, raft_port, file_name, chunks=-1, downloads_folder="Downloads", dc_ip="", dc_port=""):
    global next_sequence_to_download
    global maximum_number_of_sequences

    failed_chunks = {}

    def whole_file_downloaded(failed_chunks):
        is_whole_file_downloaded = True

        for i in range(len(next_sequence_to_download)):
            if next_sequence_to_download[i] < maximum_number_of_sequences[i]:
                failed_chunks[i] = next_sequence_to_download[i]
                is_whole_file_downloaded = False

        return is_whole_file_downloaded

    file_location_info = file_transfer.FileLocationInfo()

    if chunks == -1:
        with grpc.insecure_channel(raft_ip + ':' + raft_port) as channel:
            stub = rpc.DataTransferServiceStub(channel)
            request = file_transfer.FileInfo()
            request.fileName = file_name

            file_location_info = get_file_location(stub, request)
            print("file_location_info")
            pprint.pprint(file_location_info)

            next_sequence_to_download = [0] * file_location_info.maxChunks
            maximum_number_of_sequences = [float('inf')] * file_location_info.maxChunks
    else:
        next_sequence_to_download = [0] * (chunks + 1)
        maximum_number_of_sequences = [0] * (chunks + 1)
        maximum_number_of_sequences[chunks] = float('inf')

    while not whole_file_downloaded(failed_chunks):
        file_names = []
        chunk_nums = []
        next_sequence_to_download_arr = []
        proxy_addresses = []
        proxy_ports = []
        downloads_folders = []

        for chunk_num in failed_chunks.keys():
            if chunks == -1:
                random_proxy_index = random.randint(0, len(file_location_info.lstProxy) - 1)
                # proxy
                proxy_address = file_location_info.lstProxy[random_proxy_index].ip
                proxy_port = file_location_info.lstProxy[random_proxy_index].port
                print("proxy selected", proxy_address, proxy_port)
            else:
                # data_center direct
                proxy_address = dc_ip
                proxy_port = dc_port
                print("data center selected", proxy_address, proxy_port)

            file_names.append(file_name)
            chunk_nums.append(chunk_num)
            next_sequence_to_download_arr.append(next_sequence_to_download[chunk_num])
            proxy_addresses.append(proxy_address)
            proxy_ports.append(proxy_port)
            downloads_folders.append(downloads_folder)

        pool = ThreadPool(THREAD_POOL_SIZE)
        pool.starmap(download_chunk,
                     zip(file_names, chunk_nums, next_sequence_to_download_arr, proxy_addresses, proxy_ports,
                         downloads_folders))
        pool.close()
        pool.join()

        print("number_of_sequences_downloaded ", next_sequence_to_download)
        print("maximum_number_of_sequences ", maximum_number_of_sequences)

    if chunks == -1:
        print("calling merge ")
        merge_chunks(file_location_info.fileName,
                     os.path.join(os.path.dirname(os.path.realpath(__file__)), "Downloads"),
                     file_location_info.maxChunks)


# python3 client_download.py <filename>
if __name__ == '__main__':
    while True:
        random_raft = get_raft_node()
        try:
            print("Client connected to raft node :", random_raft["ip"], random_raft["port"])
            run(random_raft["ip"], random_raft["port"], str(sys.argv[1]))
            break
        except grpc.RpcError:
            print("Client could not connect with raft ip :", random_raft["ip"], ",port :", random_raft["port"])
            time.sleep(2)
