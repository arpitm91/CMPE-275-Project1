import random
import pprint
import grpc
import sys
import os
import time
from multiprocessing import Pool as ThreadPool
import threading
import math
import functools

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "protos"))

import utils.file_utils as file_utils
import protos.raft_pb2 as raft_proto
import protos.file_transfer_pb2 as file_transfer
import protos.file_transfer_pb2_grpc as file_transfer_rpc
from utils.common_utils import get_raft_node
from utils.common_utils import get_rand_hashing_node_from_node_info_object
from utils.input_output_util import log_info
from constants import SEQUENCE_SIZE
from constants import CHUNK_SIZE

THREAD_POOL_SIZE = 1

my_logs_read = [0]
read_diff = []
my_logs_send = [0]
send_diff = []

def file_upload_iterator(file_path, file_name, chunk_num):
    seq_max = file_utils.get_max_file_seqs_per_chunk(file_path, chunk_num)
    cur_seq_num = 0

    with open(file_path, 'rb') as f:
        # seek file pointer to start position for chunk before reading file
        f.seek(chunk_num * CHUNK_SIZE)
        total_seq = CHUNK_SIZE / SEQUENCE_SIZE

        last_time = round(time.time(), 4)
        while total_seq > 0:
            total_seq -= 1

            x = f.read(SEQUENCE_SIZE)

            if not x:
                break

            request = file_transfer.FileUploadData()
            request.fileName = file_name
            request.chunkId = chunk_num
            request.seqMax = seq_max
            request.seqNum = cur_seq_num
            request.data = x
            cur_seq_num += 1

            yield request
        read_diff.append(round(time.time(), 4) - last_time)
        # last_time = round(time.time(), 4)

        # pieces.append(x)

        # start_time = time.time()
        #
        # for chunk_data in pieces:
        #     request = file_transfer.FileUploadData()
        #     request.fileName = file_name
        #     request.chunkId = chunk_num
        #     request.seqMax = seq_max
        #     request.seqNum = cur_seq_num
        #     request.data = chunk_data
        #     cur_seq_num += 1
        #
        #     #
        #     # cur_time = round(time.time(), 4)
        #     # my_logs_send.append(cur_time)
        #     # if len(my_logs_send) != 0:
        #     #     last_time = my_logs_send[-2]
        #     #     send_diff.append(cur_time - last_time)
        #
        #     yield request
        log_info("Sent... Chunk: ", chunk_num)
        # send_diff.append((chunk_num , time.time() - start_time))

def upload_chunk(file_path, file_name, chunk_num, proxy_address, proxy_port):
    # log_info("requesting for :", file_path, "chunk no :", chunk_num, "from", proxy_address, ":", proxy_port)
    with grpc.insecure_channel(proxy_address + ':' + proxy_port) as channel:
        stub = file_transfer_rpc.DataTransferServiceStub(channel)
        stub.UploadFile(file_upload_iterator(file_path, file_name, chunk_num))
        print("Chunk Uploaded:", chunk_num)

threads = []

def process_response(call_future):
    pass

def run(raft_ip, raft_port, file_name):
    with grpc.insecure_channel(raft_ip + ':' + raft_port) as channel:
        stub = file_transfer_rpc.DataTransferServiceStub(channel)
        file_path = file_name

        file_info = os.path.basename(file_path).split(".")
        extension = ""
        if len(file_info) > 1:
            extension = "." + file_info[1]

        file_name = file_info[0] + "_" + str(math.ceil(time.time())) + extension
        file_size = file_utils.get_file_size(file_path)

        request = file_transfer.FileUploadInfo()
        request.fileName = file_name
        request.fileSize = file_size

        response = stub.RequestFileUpload(request)
        log_info("Got list of proxies: ", response.lstProxy)
        # pprint.pprint(response.lstProxy)

        if len(response.lstProxy) == 0:
            print("Could not upload file. Please try again later.")
            return

    num_of_chunks = file_utils.get_max_file_chunks(file_path)

    lst_chunk_upload_info = []

    file_paths = []
    file_names = []
    chunk_nums = []
    proxy_addresses = []
    proxy_ports = []

    for chunk_num in range(num_of_chunks):
        selected_proxy = get_rand_hashing_node_from_node_info_object(response.lstProxy, file_name, chunk_num)

        proxy_address = selected_proxy.ip
        proxy_port = selected_proxy.port

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

    print("READ DIFF")
    pprint.pprint(read_diff)
    print("SEND DIFF")
    pprint.pprint(send_diff)

    print("TOTAL READ TIME:", sum(read_diff))
    s = 0
    for x in send_diff[1:]:
        s += x[1]
    print("TOTAL SEND TIME:", s)

    log_info("################################################################################")
    log_info("File Upload Completed. To download file use this name: ", file_name)


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
            time.sleep(2)
    print("--- %s seconds ---" % (time.time() - start_time))
