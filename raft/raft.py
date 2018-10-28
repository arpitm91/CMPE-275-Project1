import threading
from concurrent import futures

import grpc
import time
import sys

import file_transfer_pb2 as file_transfer
import file_transfer_pb2_grpc as rpc

from utils.input_output_util import get_input
from utils.input_output_util import print_msg
from utils.input_output_util import log_error
from utils.input_output_util import log_info
from utils.input_output_util import print_take_input_msg
from utils.input_output_util import log_forwarding_info
from utils.input_output_util import print_file_info

from utils.file_utils import get_file_chunks
from utils.file_utils import write_file_chunks
from utils.file_utils import get_total_file_chunks
import configs.connections as connections

def _process_response(call_future):
    print(call_future.result())

class Client:
    def __init__(self, username, server_address, server_port):

        self.username = username

        # create a gRPC channel + stub
        channel = grpc.insecure_channel(server_address + ':' + str(server_port))
        print("server_address: ",server_address , " server_port:", server_port)
        self.conn = rpc.DataTransferServiceStub(channel)
        # create new listening thread for when new message streams come in
        threading.Thread(target=self._RaftHeartbit, daemon=True).start()

    def _RaftHeartbit(self):

        table_log = file_transfer.TableLog()
        table_log.file_number = "f1"
        table_log.chunk_number = "c1"
        table_log.ip = "10.0.0.1"
        table_log.port = "10000"
        table_log.operation = file_transfer.Add

        table = file_transfer.Table()
        table.cycle_number = 1
        table.tableLog.extend([table_log])

        self.conn.RaftHeartbit(table)

        # call_future = self.conn.RaftHeartbit.future(table)
        # call_future.add_done_callback(_process_response)

# server
class ChatServer(rpc.DataTransferServiceServicer):
    def __init__(self, username):
        self.username = username

    def RaftHeartbit(self, request: file_transfer.Table, context):
        ack = file_transfer.Ack()
        ack.id = 1
        return ack


    def RequestVote(self, request: file_transfer.Candidacy, context):
        # return CandidacyResponse
        pass


def start_client(username, server_address, server_port):
    c = Client(username, server_address, server_port)


def start_server(username, my_port):
    # create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_object = ChatServer(username)
    rpc.add_DataTransferServiceServicer_to_server(server_object, server)

    print('Starting server. Listening...', my_port)
    server.add_insecure_port('[::]:' + str(my_port))
    server.start()
    print('server started')

def main(argv):
    username = argv[1]
    my_port = connections.connections[username]["own"]["port"]
    threading.Thread(target=start_server, args=(username, my_port), daemon=True).start()


    # time.sleep(5)
    print("starting clients")

    for client in connections.connections[username]["clients"]:
        # client
        server_address = client["ip"]
        server_port = client["port"]

        threading.Thread(target=start_client, args=(username, server_address, server_port), daemon=True).start()

    # Server starts in background (another thread) so keep waiting
    while True:
        time.sleep(64 * 64 * 100)


if __name__ == '__main__':
    main(sys.argv[:])
