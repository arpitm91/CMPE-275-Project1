import pprint
import grpc
import file_transfer_pb2 as file_transfer
import file_transfer_pb2_grpc as rpc


def run():
    with grpc.insecure_channel('localhost:10000') as channel:
        stub = rpc.DataTransferServiceStub(channel)

        request = file_transfer.FileInfo()
        request.fileid = "file1"

        response = stub.GetFileLocation(request)
    print("Response received: ")
    pprint.pprint(response)


if __name__ == '__main__':
    run()
