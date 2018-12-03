import grpc
import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "protos"))

from utils.file_utils import write_file_chunks
from utils.file_utils import merge_chunks
import protos.file_transfer_pb2 as file_transfer
import protos.file_transfer_pb2_grpc as rpc
from utils.common_utils import get_raft_node
from utils.common_utils import get_rand_hashing_node_from_node_info_object
from utils.input_output_util import log_info

from utils.threading_utils import ThreadPool

THREAD_POOL_SIZE = 4


def download_chunk(file_name, chunk_num, start_seq_num, proxy_address, proxy_port, next_sequence_to_download,
                   maximum_number_of_sequences, downloads_folder="Downloads"):
    log_info("requesting for :", file_name, "chunk no :", chunk_num, "from", proxy_address, ":", proxy_port)

    stub = rpc.DataTransferServiceStub(grpc.insecure_channel(proxy_address + ':' + proxy_port))
    request = file_transfer.ChunkInfo()
    request.fileName = file_name
    request.chunkId = chunk_num
    request.startSeqNum = start_seq_num
    try:
        for response in stub.DownloadChunk(request):
            # log_info("Response received: Chunk", response.chunkId, "Sequence:", response.seqNum, "/",
            #          response.seqMax)
            next_sequence_to_download[chunk_num] = response.seqNum + 1
            maximum_number_of_sequences[chunk_num] = response.seqMax
            write_file_chunks(response, os.path.join(os.path.dirname(os.path.realpath(__file__)), downloads_folder))
    except grpc.RpcError:
        log_info("Failed to connect to data center..Retrying !!")

    log_info("request completed for :", file_name, "chunk no :", chunk_num, "from", proxy_address, ":", proxy_port,
             "last seq :", next_sequence_to_download[chunk_num], "max seq :",
             maximum_number_of_sequences[chunk_num])


def get_file_location(stub, request):
    file_location_info = stub.RequestFileInfo(request)
    log_info("Response received: ")
    # pprint.pprint(file_location_info)
    log_info(file_location_info.maxChunks)
    log_info("is file found :", file_location_info.isFileFound)
    return file_location_info


def run(raft_ip, raft_port, file_name, chunks=-1, downloads_folder="Downloads", dc_ip="", dc_port=""):
    next_sequence_to_download = []
    maximum_number_of_sequences = []

    failed_chunks = {}

    def whole_file_downloaded(failed_chunks_dict):
        is_whole_file_downloaded = True

        for i in range(len(next_sequence_to_download)):
            if next_sequence_to_download[i] < maximum_number_of_sequences[i]:
                failed_chunks_dict[i] = next_sequence_to_download[i]
                is_whole_file_downloaded = False

        return is_whole_file_downloaded

    file_location_info = file_transfer.FileLocationInfo()

    if chunks == -1:
        stub = rpc.DataTransferServiceStub(grpc.insecure_channel(raft_ip + ':' + raft_port))
        request = file_transfer.FileInfo()
        request.fileName = file_name

        file_location_info = get_file_location(stub, request)
        log_info("file_location_info")
        # pprint.pprint(file_location_info)

        next_sequence_to_download = [0] * file_location_info.maxChunks
        maximum_number_of_sequences = [float('inf')] * file_location_info.maxChunks
    else:
        next_sequence_to_download = [100] * (chunks + 1)
        maximum_number_of_sequences = [100] * (chunks + 1)
        next_sequence_to_download[chunks] = 0
        maximum_number_of_sequences[chunks] = float('inf')

    pool = ThreadPool(THREAD_POOL_SIZE)

    while not whole_file_downloaded(failed_chunks):
        for chunk_num in failed_chunks.keys():
            if chunks == -1:
                selected_proxy = get_rand_hashing_node_from_node_info_object(file_location_info.lstProxy, file_name,
                                                                             chunk_num)
                proxy_address = selected_proxy.ip
                proxy_port = selected_proxy.port
                log_info("proxy selected", proxy_address, proxy_port)
            else:
                # data_center direct
                proxy_address = dc_ip
                proxy_port = dc_port
                log_info("data center selected", proxy_address, proxy_port)

            pool.add_task(download_chunk, file_name, chunk_num, next_sequence_to_download[chunk_num], proxy_address,
                          proxy_port,next_sequence_to_download, maximum_number_of_sequences, downloads_folder)

        pool.wait_completion()
        log_info("number_of_sequences_downloaded ", next_sequence_to_download)
        log_info("maximum_number_of_sequences ", maximum_number_of_sequences)
        failed_chunks = {}

    if chunks == -1:
        log_info("calling merge ")
        merge_chunks(file_location_info.fileName,
                     os.path.join(os.path.dirname(os.path.realpath(__file__)), "Downloads"),
                     file_location_info.maxChunks)


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
