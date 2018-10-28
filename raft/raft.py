import threading
from concurrent import futures
from collections import defaultdict

import pprint
import grpc, functools
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

lst_clients = []

file_logs = []
file_info_table = {}

def _process_response(client, call_future):
    print(client.server_port)
    print(call_future.result())

class Client:
    def __init__(self, username, server_address, server_port):
        self.username = username
        self.server_port = server_port
        # create a gRPC channel + stub
        channel = grpc.insecure_channel(server_address + ':' + str(server_port))
        print("server_address: ",server_address , " server_port:", server_port)
        self.conn = rpc.DataTransferServiceStub(channel)
        # create new listening thread for when new message streams come in
        # threading.Thread(target=self._RaftHeartbit, daemon=True).start()

    def _RaftHeartbit(self, table):
        call_future = self.conn.RaftHeartbit.future(table)
        call_future.add_done_callback(functools.partial(_process_response, self))

# server
class ChatServer(rpc.DataTransferServiceServicer):
    def __init__(self, username):
        self.username = username

    def RaftHeartbit(self, request: file_transfer.Table, context):
        
        for tl in request.tableLog:            
            file_logs.append(tl)          
            if tl.operation == file_transfer.Remove:            
                if tl.file_number in file_info_table and tl.chunk_number in file_info_table[tl.file_number]:
                    file_info_table[tl.file_number][tl.chunk_number].discard((tl.ip, tl.port))

            elif tl.operation == file_transfer.Add:
                if tl.file_number not in file_info_table:
                    file_info_table[tl.file_number] = {}
                
                if tl.chunk_number not in file_info_table[tl.file_number]:
                    file_info_table[tl.file_number][tl.chunk_number] = set()
                
                file_info_table[tl.file_number][tl.chunk_number].add((tl.ip, tl.port))
        
        ack = file_transfer.Ack()        
        ack.id = len(file_logs)

        print("##############################")        
        pprint.pprint(file_info_table)

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
    # Server starts in background (another thread) so keep waiting
    while True:
        time.sleep(64 * 64 * 100)

def main(argv):
    username = argv[1]
    my_port = connections.connections[username]["own"]["port"]
    threading.Thread(target=start_server, args=(username, my_port), daemon=True).start()

    for client in connections.connections[username]["clients"]:
        # client
        server_address = client["ip"]
        server_port = client["port"]
        c = Client(username, server_address, server_port)
        lst_clients.append(c)

        # threading.Thread(target=start_client, args=(username, server_address, server_port), daemon=True).start()

    cycle = 0

    while True:
        cycle += 1
        table_log = file_transfer.TableLog()
        table_log.file_number = "f1"
        table_log.chunk_number = "c1"
        table_log.ip = "10.0.0.1"
        table_log.port = "10000"
        table_log.operation = file_transfer.Add

        table = file_transfer.Table()
        table.cycle_number = cycle
        table.tableLog.extend([table_log])

        for client in lst_clients:
            client._RaftHeartbit(table)
        
        time.sleep(5)

    # Server starts in background (another thread) so keep waiting
    while True:
        time.sleep(64 * 64 * 100)


if __name__ == '__main__':
    main(sys.argv[:])
