import random
import pprint
import grpc
import sys
import os
import time

import math

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "protos"))

import utils.file_utils as file_utils
import protos.raft_pb2 as raft_proto
import protos.file_transfer_pb2 as file_transfer
import protos.file_transfer_pb2_grpc as file_transfer_rpc
from utils.common_utils import get_raft_node
from utils.common_utils import get_rand_hashing_node_from_node_info_object
from utils.input_output_util import log_info

from utils.threading_utils import ThreadPool

THREAD_POOL_SIZE = 16
GRPC_TIMEOUT = 20


def file_upload_iterator(file_path, file_name, chunk_num):
    seq_max = file_utils.get_max_file_seqs_per_chunk(file_path, chunk_num)
    cur_seq_num = 0
    for chunk_buffer in file_utils.get_file_seqs_per_chunk(file_path, chunk_num):
        request = file_transfer.FileUploadData()
        request.fileName = file_name
        request.chunkId = chunk_num
        request.seqMax = seq_max
        request.seqNum = cur_seq_num
        request.data = chunk_buffer
        cur_seq_num += 1
        log_info("Sending... Chunk: ", chunk_num, ", Seq: ", cur_seq_num)
        yield request


def upload_chunk(file_path, file_name, chunk_num, proxy_address, proxy_port):
    log_info("requesting for :", file_path, "chunk no :", chunk_num, "from", proxy_address, ":", proxy_port)
    stub = file_transfer_rpc.DataTransferServiceStub(grpc.insecure_channel(proxy_address + ':' + proxy_port))
    stub.UploadFile(file_upload_iterator(file_path, file_name, chunk_num))


def run(raft_ip, raft_port, file_name):
    stub = file_transfer_rpc.DataTransferServiceStub(grpc.insecure_channel(raft_ip + ':' + raft_port))
    file_path = file_name

    file_info = os.path.basename(file_path).split(".")
    extension = ""
    if len(file_info) > 1:
        extension = "." + file_info[1]

    file_name = "team1_" + file_info[0] + "_" + str(math.ceil(time.time())) + extension
    file_size = file_utils.get_file_size(file_path)

    request = file_transfer.FileUploadInfo()
    request.fileName = file_name
    request.fileSize = file_size

    response = stub.RequestFileUpload(request, timeout=GRPC_TIMEOUT)
    log_info("Got list of proxies: ", response.lstProxy)
    # pprint.pprint(response.lstProxy)

    if len(response.lstProxy) == 0:
        print("Could not upload file. Please try again later.")
        return

    num_of_chunks = file_utils.get_max_file_chunks(file_path)

    lst_chunk_upload_info = []

    pool = ThreadPool(THREAD_POOL_SIZE)

    for chunk_num in range(num_of_chunks):
        selected_proxy = get_rand_hashing_node_from_node_info_object(response.lstProxy, file_name, chunk_num)

        proxy_address = selected_proxy.ip
        proxy_port = selected_proxy.port

        chunk_upload_info = raft_proto.ChunkUploadInfo()
        chunk_upload_info.chunkId = chunk_num
        chunk_upload_info.uploadedDatacenter.ip = proxy_address
        chunk_upload_info.uploadedDatacenter.port = proxy_port

        lst_chunk_upload_info.append(chunk_upload_info)
        pool.add_task(upload_chunk,file_path, file_name, chunk_num, proxy_address, proxy_port)

    pool.wait_completion()
    log_info("################################################################################")
    print("File Upload Completed. To download file use this name: ", file_name)


# python3 client_upload.py <filename>
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
            time.sleep(0.2)
    print("--- %s seconds ---" % (time.time() - start_time))
