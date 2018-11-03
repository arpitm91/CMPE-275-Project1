import threading
import random
import pprint
import grpc
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "protos"))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "utils"))

import file_utils
import file_transfer_pb2 as file_transfer
import file_transfer_pb2_grpc as rpc

threads = []


def file_upload_iterator(file_name, chunk_num):
    seq_max = file_utils.get_max_file_seqs_per_chunk(file_name)
    cur_seq_num = 0
    for chunk_buffer in file_utils.get_file_seqs_per_chunk(file_name, chunk_num):
        request = file_transfer.FileUploadData()
        request.fileName = file_name
        request.chunkId = chunk_num
        request.seqMax = seq_max
        request.seqNum = cur_seq_num
        request.data = chunk_buffer
        cur_seq_num += 1
        yield request


def upload_chunk(file_name, chunk_num, proxy_address, proxy_port):
    print("requesting for :", file_name, "chunk no :", chunk_num, "from", proxy_address, ":", proxy_port)
    with grpc.insecure_channel(proxy_address + ':' + proxy_port) as channel:
        stub = rpc.DataTransferServiceStub(channel)
        stub.UploadFile(file_upload_iterator(file_name, chunk_num))


def run(argv):
    with grpc.insecure_channel(str(argv[1]) + ':' + str(argv[2])) as channel:
        stub = rpc.DataTransferServiceStub(channel)
        file_name = str(argv[3])
        file_size = file_utils.get_file_size(file_name)
        request = file_transfer.FileUploadInfo()
        request.fileName = file_name
        request.fileSize = file_size

        lst_proxy = stub.RequestFileUpload(request)
        print("Got list of proxies: ", lst_proxy)
        pprint.pprint(lst_proxy)

    num_of_chunks = file_utils.get_max_file_chunks(file_name)

    for chunk_num in range(num_of_chunks):
        random_proxy_index = random.randint(0, len(lst_proxy) - 1)
        proxy_address = lst_proxy[random_proxy_index].ip
        proxy_port = lst_proxy[random_proxy_index].port

        threads.append(threading.Thread(target=upload_chunk, args=(file_name, chunk_num, proxy_address, proxy_port),
                                        daemon=True))
        threads[-1].start()

    for t in threads:
        t.join()


# python3 client.py <raft_ip> <raft_port> <filename>
if __name__ == '__main__':
    run(sys.argv[:])
