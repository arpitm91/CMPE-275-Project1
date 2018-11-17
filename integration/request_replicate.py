import grpc
import time
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "protos"))
import raft_pb2 as our_proto
import raft_pb2_grpc as our_proto_rpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def register_dc(ip, port):
    with grpc.insecure_channel(ip + ':' + port) as channel:
        stub = our_proto_rpc.RaftServiceStub(channel)

        request = our_proto.ReplicationInfo()
        request.fileName = "friend_e3_1542077742.064304.mkv"
        request.chunkId = 1
        request.fromDatacenter.ip = "localhost"
        request.fromDatacenter.port = "11002"

        while True:
            try:
                result = stub.ReplicationInitiate(request)
                print(result)
                break
            except grpc.RpcError:
                print("Could not send replication request")
                time.sleep(2)


# python3 datacenter.py <dc_name from data_center_info> <raft ip to register to> <raft port to register to>
if __name__ == '__main__':
    register_dc("10.0.10.3", "11001")

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        exit()
