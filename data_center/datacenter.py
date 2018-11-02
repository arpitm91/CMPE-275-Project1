# from file_utils import get_file_seqs
# from file_utils import get_max_file_seqs
# import grpc
# import file_transfer_pb2 as file_transfer
# import file_transfer_pb2_grpc as rpc
# from concurrent import futures
# import time
# import configs.data_center_info as data_center_info
# import os
# import sys
#
# _ONE_DAY_IN_SECONDS = 60 * 60 * 24
#
#
# class DataCenterServer(rpc.DataTransferServiceServicer):
#     def DownloadChunk(self, request, context):
#         print("fvdfvvdv")
#         file_name = request.fileName
#         chunk_id = request.chunkId
#         start_seq_num = request.startSeqNum
#
#         chunk_path = folder + "/" + file_name + "/" + chunk_id
#         current_seq = 0
#         reply = file_transfer.FileMetaData()
#
#         # if os.path.isfile(chunk_path):
#         #     total_seq = get_max_file_seqs(chunk_path)
#         #
#         #     for chunk_buffer in get_file_seqs(chunk_path):
#         #         if current_seq >= start_seq_num:
#         #             reply.fileName = file_name
#         #             reply.chunkId = chunk_id
#         #             reply.data = chunk_buffer
#         #             reply.seqNum = current_seq
#         #             reply.seqMax = total_seq
#         #             current_seq += 1
#         #             yield reply
#         #
#         # else:
#         reply.fileName = file_name
#         reply.chunkId = chunk_id
#         reply.data = str.encode("")
#         reply.seqNum = 0
#         reply.seqMax = 0
#         return reply
#
#
# def start_server(username, my_port):
#     server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
#     rpc.add_DataTransferServiceServicer_to_server(DataCenterServer(), server)
#     server.add_insecure_port('[::]:' + str(my_port))
#     server.start()
#     print("server started at port : ", my_port)
#     try:
#         while True:
#             time.sleep(_ONE_DAY_IN_SECONDS)
#     except KeyboardInterrupt:
#         server.stop(0)
#
#
# if __name__ == '__main__':
#     data_center_name = sys.argv[1]
#     port = data_center_info.data_center[data_center_name]["port"]
#     folder = data_center_info.data_center[data_center_name]["folder"]
#     start_server(data_center_name, port)


import pprint
import grpc
import file_transfer_pb2 as file_transfer
import file_transfer_pb2_grpc as rpc

from concurrent import futures
import time
import os
import math

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class Reply(rpc.DataTransferServiceServicer):

    def DownloadChunk(self, request, context):
        print("request received")
        my_reply = file_transfer.FileMetaData()

        my_reply.fileName = request.fileName
        my_reply.chunkId = request.chunkId
        my_reply.data = str.encode("dfvsv")
        my_reply.seqNum = 0
        my_reply.seqMax = 0

        print("Replied to :")
        pprint.pprint(request)
        print("############################")
        return my_reply


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc.add_DataTransferServiceServicer_to_server(Reply(), server)
    server.add_insecure_port('localhost:10012')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
