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
    try:
        with open(filename, 'rb') as f:
            while True:
                piece = f.read(CHUNK_SIZE)
                if not piece:
                    break
                yield piece
    except:
        print("chunk reading exception..")

class Reply(rpc.DataTransferServiceServicer):

    def RequestFileInfo(self, request, context):
        my_reply = file_transfer.FileLocationInfo()
        my_reply.fileName = request.fileName
        my_reply.isFileFound = True
        my_reply.maxChunks = 2

        proxy_info_0 = file_transfer.ProxyInfo()
        proxy_info_0.ip = "localhost"
        proxy_info_0.port = "10004"

        proxy_info_1 = file_transfer.ProxyInfo()
        proxy_info_1.ip = "localhost"
        proxy_info_1.port = "10001"

        proxy_info_2 = file_transfer.ProxyInfo()
        proxy_info_2.ip = "localhost"
        proxy_info_2.port = "10002"

        proxy_info_3 = file_transfer.ProxyInfo()
        proxy_info_3.ip = "localhost"
        proxy_info_3.port = "10003"

        my_reply.lstProxy.extend([
            proxy_info_0,
            proxy_info_1,
            proxy_info_2,
            proxy_info_3
        ])
        print("Replied to :")
        pprint.pprint(request)
        print("############################")
        return my_reply

    def RequestFileUpload(self, request, context):
        my_reply = file_transfer.ProxyList()

        proxy_info = file_transfer.ProxyInfo()
        proxy_info.ip = "localhost"
        proxy_info.port = "10001"
        my_reply.lstProxy.extend([
            proxy_info
        ])

        print("Replied to :")
        pprint.pprint(request)
        print("############################")
        return my_reply

    def DownloadChunk(self, request, context):
        current_chunk = 1

        for file_buffer in get_file_chunks(request.filename):
            my_reply = file_transfer.FileMetaData()

            my_reply.fileName = request.fileName
            my_reply.chunkId = request.chunkId
            my_reply.seqMax = get_total_file_chunks(request.filename)
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
