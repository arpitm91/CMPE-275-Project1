import threading
import random
import pprint

import google
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
failed_chunks = {}
next_sequence_to_download = []
maximum_number_of_sequences = []


def download_chunk(file_name, chunk_num, startSeqNum, proxy_address, proxy_port, downloads_folder="Downloads"):
    print("requesting for :", file_name, "chunk no :", chunk_num, "from", proxy_address, ":", proxy_port)

    global next_sequence_to_download
    global maximum_number_of_sequences
    with grpc.insecure_channel(proxy_address + ':' + proxy_port) as channel:
        stub = rpc.DataTransferServiceStub(channel)
        request = file_transfer.ChunkInfo()
        request.fileName = file_name
        request.chunkId = chunk_num
        request.startSeqNum = startSeqNum
        try:
            for response in stub.DownloadChunk(request):
                print("Response received: ", response.seqNum, "/", response.seqMax)
                next_sequence_to_download[chunk_num] = response.seqNum + 1
                maximum_number_of_sequences[chunk_num] = response.seqMax
                write_file_chunks(response, os.path.join(os.path.dirname(os.path.realpath(__file__)), downloads_folder))
                print(chunk_num, "last seq :", next_sequence_to_download[chunk_num], "max seq :",
                      maximum_number_of_sequences[chunk_num])
        except grpc.RpcError:
            print("Failed to connect to data center..Retrying !!")

        print("request completed for :", file_name, "chunk no :", chunk_num, "from", proxy_address, ":", proxy_port,
              "last seq :", next_sequence_to_download[chunk_num], "max seq :", maximum_number_of_sequences[chunk_num])

def getFileLocation(stub, request):
    file_location_info = stub.RequestFileInfo(request)
    print("Response received: ")
    pprint.pprint(file_location_info)
    print(file_location_info.maxChunks)
    return file_location_info

def run(raft_ip, raft_port, file_name, chunks="all",downloads_folder = "Downloads"):
    with grpc.insecure_channel(raft_ip + ':' + raft_port) as channel:
        stub = rpc.DataTransferServiceStub(channel)
        request = file_transfer.FileInfo()
        request.fileName = file_name

        file_location_info = getFileLocation(stub, request)

        global next_sequence_to_download
        global maximum_number_of_sequences

        if chunks=="all":
            next_sequence_to_download = [0] * file_location_info.maxChunks
            maximum_number_of_sequences = [float('inf')] * file_location_info.maxChunks
        else:
            next_sequence_to_download = [0] * file_location_info.maxChunks
            maximum_number_of_sequences = [0] * file_location_info.maxChunks
            maximum_number_of_sequences[int(chunks)] = float('inf')

    while not wholeFileDownloaded():
        for chunk_num in failed_chunks.keys():
            random_proxy_index = random.randint(0, len(file_location_info.lstProxy) - 1)
            # proxy
            proxy_address = file_location_info.lstProxy[random_proxy_index].ip
            proxy_port = file_location_info.lstProxy[random_proxy_index].port
            print("proxy selected", proxy_address, proxy_port)

            threads.append(
                threading.Thread(target=download_chunk, args=(
                    file_name, chunk_num, next_sequence_to_download[chunk_num], proxy_address, proxy_port,downloads_folder)))
            threads[-1].start()
        for t in threads:
            t.join()
        threads.clear()

        print("number_of_sequences_downloaded ", next_sequence_to_download)
        print("maximum_number_of_sequences ", maximum_number_of_sequences)

    threads.clear()

    if chunks == "all":
        print("calling merge ")
        merge_chunks(file_location_info.fileName,
                     os.path.join(os.path.dirname(os.path.realpath(__file__)), "Downloads"),
                     file_location_info.maxChunks)


def wholeFileDownloaded():
    isWholeFileDownloaded = True

    for i in range(len(next_sequence_to_download)):
        if next_sequence_to_download[i] < maximum_number_of_sequences[i]:
            global failed_chunks
            failed_chunks[i] = next_sequence_to_download[i]
            isWholeFileDownloaded = False

    return isWholeFileDownloaded


# python3 client_download.py <raft_ip> <raft_port> <filename>
# python3 client/client_download.py localhost 10000 file1
# python3 integration/Server.py
# python3 data_center/datacenter.py dc_aartee
if __name__ == '__main__':
    # run(sys.argv[:])
    run(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
