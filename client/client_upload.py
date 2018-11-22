import random
import pprint
import grpc
import sys
import os
import time
from multiprocessing.dummy import Pool as ThreadPool

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "protos"))

import utils.file_utils as file_utils
import protos.raft_pb2 as raft_proto
import protos.file_transfer_pb2 as file_transfer
import protos.file_transfer_pb2_grpc as file_transfer_rpc
from utils.common_utils import get_raft_node
from utils.input_output_util import log_info

THREAD_POOL_SIZE = 4


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
    with grpc.insecure_channel(proxy_address + ':' + proxy_port) as channel:
        stub = file_transfer_rpc.DataTransferServiceStub(channel)
        stub.UploadFile(file_upload_iterator(file_path, file_name, chunk_num))


def run(argv):
    random_raft = get_raft_node()
    log_info("Client connected to raft node :", random_raft["ip"], random_raft["port"])

    raft_ip = random_raft["ip"]
    raft_port = random_raft["port"]
    with grpc.insecure_channel(raft_ip + ':' + raft_port) as channel:
        stub = file_transfer_rpc.DataTransferServiceStub(channel)
        file_path = str(argv[1])

        file_info = os.path.basename(file_path).split(".")
        extension = ""
        if len(file_info) > 1:
            extension = "." + file_info[1]

        file_name = file_info[0] + "_" + str(time.time()) + extension
        file_size = file_utils.get_file_size(file_path)

        request = file_transfer.FileUploadInfo()
        request.fileName = file_name
        request.fileSize = file_size

        response = stub.RequestFileUpload(request)

        log_info("Got list of proxies: ", response.lstProxy)
        #pprint.pprint(response.lstProxy)

    num_of_chunks = file_utils.get_max_file_chunks(file_path)

    lst_chunk_upload_info = []

    file_paths = []
    file_names = []
    chunk_nums = []
    proxy_addresses = []
    proxy_ports = []

    proxy_index = 0
    for chunk_num in range(num_of_chunks):
        # random_proxy_index = random.randint(0, len(response.lstProxy) - 1)
        random_proxy_index = proxy_index % len(response.lstProxy)
        proxy_index = proxy_index + 1

        proxy_address = response.lstProxy[random_proxy_index].ip
        proxy_port = response.lstProxy[random_proxy_index].port

        chunk_upload_info = raft_proto.ChunkUploadInfo()
        chunk_upload_info.chunkId = chunk_num
        chunk_upload_info.uploadedDatacenter.ip = proxy_address
        chunk_upload_info.uploadedDatacenter.port = proxy_port

        lst_chunk_upload_info.append(chunk_upload_info)

        file_paths.append(file_path)
        file_names.append(file_name)
        chunk_nums.append(chunk_num)
        proxy_addresses.append(proxy_address)
        proxy_ports.append(proxy_port)

    pool = ThreadPool(THREAD_POOL_SIZE)
    pool.starmap(upload_chunk, zip(file_paths, file_names, chunk_nums, proxy_addresses, proxy_ports))
    pool.close()
    pool.join()

    log_info("################################################################################")
    log_info("File Upload Completed. To download file use this name: ", file_name)


# python3 client_upload.py <filename>
if __name__ == '__main__':
    start_time = time.time()
    run(sys.argv[:])
    print("--- %s seconds ---" % (time.time() - start_time))
