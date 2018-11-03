import pprint
import grpc
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir,"protos"))
import file_transfer_pb2 as file_transfer
import file_transfer_pb2_grpc as rpc

def run():

    with grpc.insecure_channel('localhost:10010') as channel:
        stub = rpc.DataTransferServiceStub(channel)

        request = file_transfer.ChunkInfo()
        request.fileName = "file1"
        request.chunkId = 0
        request.startSeqNum = 0

        for response in stub.DownloadChunk(request):
            print("Response received: ")
            pprint.pprint(response)


if __name__ == '__main__':
    run()