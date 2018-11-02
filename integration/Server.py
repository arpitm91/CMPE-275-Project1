import pprint
import grpc
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir,"protos"))
import file_transfer_pb2 as file_transfer
import file_transfer_pb2_grpc as rpc

from concurrent import futures
import time
import math

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def get_total_file_chunks(filename):
    return math.ceil(os.path.getsize(os.path.join(os.path.dirname(os.path.realpath(__file__)),filename)) / CHUNK_SIZE)


def get_file_chunks(filename):
    with open(filename, 'rb') as f:
        while True:
            piece = f.read(CHUNK_SIZE);
            if not piece:
                break
            yield piece

class Reply(rpc.DataTransferServiceServicer):

    def RequestFileInfo(self, request, context):
        my_reply = file_transfer.FileLocationInfo()
        my_reply.fileName = request.fileName
        my_reply.isFileFound = True
        my_reply.maxChunks = 1

        proxy_info = file_transfer.ProxyInfo()
        proxy_info.ip = "localhost"
        proxy_info.port = "10012"

        my_reply.lstProxy.extend([
            proxy_info
        ])
        print("Replied to :")
        pprint.pprint(request)
        print("############################")
        return my_reply

    def DownloadChunk(self, request, context):
        current_chunk = 1

        for file_buffer in get_file_chunks(filename):
            my_reply = file_transfer.FileMetaData()

            my_reply.fileName = request.fileName
            my_reply.chunkId = request.chunkId
            my_reply.seqMax = get_total_file_chunks(filename)
            current_chunk += 1

            print("Replied to :")
            pprint.pprint(request)
            print("############################")
            yield my_reply


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc.add_DataTransferServiceServicer_to_server(Reply(), server)
    server.add_insecure_port('[::]:10000')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
