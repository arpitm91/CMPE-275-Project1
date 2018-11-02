import grpc
from concurrent import futures
import time
import configs.data_center_info as data_center_info
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir,"protos"))
from utils.file_utils import get_file_seqs
from utils.file_utils import get_max_file_seqs
import file_transfer_pb2 as file_transfer
import file_transfer_pb2_grpc as rpc


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class DataCenterServer(rpc.DataTransferServiceServicer):
    def DownloadChunk(self, request, context):
        print("fvdfvvdv")
        file_name = request.fileName
        chunk_id = request.chunkId
        start_seq_num = request.startSeqNum

        chunk_path = folder + "/" + file_name + "/" + str(chunk_id)
        current_seq = 0

        if os.path.isfile(chunk_path):
            total_seq = get_max_file_seqs(chunk_path)

            for chunk_buffer in get_file_seqs(chunk_path):
                if current_seq >= start_seq_num:
                    reply = file_transfer.FileMetaData()
                    reply.fileName = file_name
                    reply.chunkId = chunk_id
                    reply.data = chunk_buffer
                    reply.seqNum = current_seq
                    reply.seqMax = total_seq
                    current_seq += 1
                    yield reply

        else:
            reply = file_transfer.FileMetaData()
            reply.fileName = file_name
            reply.chunkId = chunk_id
            reply.data = str.encode("")
            reply.seqNum = 0
            reply.seqMax = 0
            return reply


def start_server(username, my_port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc.add_DataTransferServiceServicer_to_server(DataCenterServer(), server)
    server.add_insecure_port('[::]:' + str(my_port))
    server.start()
    print("server started at port : ", my_port)
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    data_center_name = sys.argv[1]
    port = data_center_info.data_center[data_center_name]["port"]
    folder = data_center_info.data_center[data_center_name]["folder"]
    start_server(data_center_name, port)
