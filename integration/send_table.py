import pprint
import grpc
import file_transfer_pb2 as file_transfer
import file_transfer_pb2_grpc as rpc

from concurrent import futures
import time

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Reply(rpc.DataTransferServiceServicer):

    def GetFileLocation(self, request, context):
        my_reply = file_transfer.FileLocationInfo()
        my_reply.fileName = request.fileid
        my_reply.isFileFound = True

        first_chunk = file_transfer.ChunkLocationInfo()
        first_chunk.chunkId = 0
        first_chunk.ip = "10.0.0.1"
        first_chunk.port = "5000"

        second_chunk = file_transfer.ChunkLocationInfo()
        second_chunk.chunkId = 1
        second_chunk.ip = "10.0.0.2"
        second_chunk.port = "5001"

        third_chunk = file_transfer.ChunkLocationInfo()
        third_chunk.chunkId = 2
        third_chunk.ip = "10.0.0.3"
        third_chunk.port = "5002"

        my_reply.lstChunkLocation.extend([
            first_chunk,
            second_chunk,
            third_chunk
        ])
        print("Replied to :")
        pprint.pprint(request)
        print("############################")
        return my_reply


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc.add_DataTransferServiceServicer_to_server(Reply(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
