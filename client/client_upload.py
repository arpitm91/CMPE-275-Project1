import threading
import random
import pprint
import grpc
import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "protos"))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "utils"))

import file_utils
import raft_pb2 as raft_proto
import file_transfer_pb2 as file_transfer
import file_transfer_pb2_grpc as file_transfer_rpc
from common_utils import get_raft_node

threads = []
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
        print("Sending... Chunk: ", chunk_num, ", Seq: ", cur_seq_num)
        yield request


def upload_chunk(file_path, file_name, chunk_num, proxy_address, proxy_port):
    print("requesting for :", file_path, "chunk no :", chunk_num, "from", proxy_address, ":", proxy_port)
    with grpc.insecure_channel(proxy_address + ':' + proxy_port) as channel:
        stub = file_transfer_rpc.DataTransferServiceStub(channel)
        stub.UploadFile(file_upload_iterator(file_path, file_name, chunk_num))


def run(argv):
    random_raft = get_raft_node()
    print("Client connected to raft node :", random_raft["ip"], random_raft["port"])

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

        print("Got list of proxies: ", response.lstProxy)
        pprint.pprint(response.lstProxy)

    num_of_chunks = file_utils.get_max_file_chunks(file_path)

    lst_chunk_upload_info = []

    threads_done_of_chunk = 0
    while threads_done_of_chunk < num_of_chunks:
        for chunk_num in range(threads_done_of_chunk, min(num_of_chunks, threads_done_of_chunk + THREAD_POOL_SIZE)):
            random_proxy_index = random.randint(0, len(response.lstProxy) - 1)
            proxy_address = response.lstProxy[random_proxy_index].ip
            proxy_port = response.lstProxy[random_proxy_index].port

            chunk_upload_info = raft_proto.ChunkUploadInfo()
            chunk_upload_info.chunkId = chunk_num
            chunk_upload_info.uploadedDatacenter.ip = proxy_address
            chunk_upload_info.uploadedDatacenter.port = proxy_port

            lst_chunk_upload_info.append(chunk_upload_info)

            threads.append(
                threading.Thread(target=upload_chunk, args=(file_path, file_name, chunk_num, proxy_address, proxy_port),
                                 daemon=True))
            threads[-1].start()

        for t in threads:
            t.join()

        threads_done_of_chunk = threads_done_of_chunk + THREAD_POOL_SIZE

    # with grpc.insecure_channel(raft_ip + ':' + raft_port) as channel:
    #     stub = raft_proto_rpc.RaftServiceStub(channel)
    #
    #     request = raft_proto.UploadCompleteFileInfo()
    #     request.fileName = file_name
    #     request.lstChunkUploadInfo.extend(lst_chunk_upload_info)
    #     stub.FileUploadCompleted(request)

    print("################################################################################")
    print("File Upload Completed. To download file use this name: ", file_name)


# python3 client_upload.py <filename>
if __name__ == '__main__':
    run(sys.argv[:])
