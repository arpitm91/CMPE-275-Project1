import grpc
import functools
import time
import sys

import file_transfer_pb2 as file_transfer
import file_transfer_pb2_grpc as rpc
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
        print("server_address: ", server_address, " server_port:", server_port)
        self.conn = rpc.DataTransferServiceStub(channel)
        # create new listening thread for when new message streams come in
        # threading.Thread(target=self._RaftHeartbeat, daemon=True).start()

    def _RaftHeartbeat(self, table):
        call_future = self.conn.RaftHeartbeat.future(table)
        call_future.add_done_callback(functools.partial(_process_response, self))

    def _AddFileLog(self, table_log):
        call_future = self.conn.AddFileLog.future(table_log)
        call_future.add_done_callback(functools.partial(_process_response, self))


# server
class ChatServer(rpc.DataTransferServiceServicer):
    def __init__(self, username):
        self.username = username

    def RaftHeartbeat(self, request: file_transfer.Table, context):
        pass

    def RequestVote(self, request: file_transfer.Candidacy, context):
        # return CandidacyResponse
        pass


def main(argv):
    username = argv[1]

    print(username)
    print(connections.connections)
    print(connections.connections[username])

    for client in connections.connections[username]["clients"]:
        # client
        server_address = client["ip"]
        server_port = client["port"]
        c = Client(username, server_address, server_port)
        lst_clients.append(c)

    table_log = file_transfer.TableLog()
    table_log.file_number = "f0"
    table_log.chunk_number = "c1"
    table_log.ip = "10.0.0.2"
    table_log.port = "10001"
    table_log.log_index = -1
    table_log.operation = file_transfer.Add

    for client in lst_clients:
        client._AddFileLog(table_log)

    # cycle += 1
    # j = 0
    # for i in range(10):        
    #     table_log = file_transfer.TableLog()
    #     table_log.file_number = "f" + str(j)
    #     table_log.chunk_number = "c" + str(i)
    #     table_log.ip = "10.0.0.1"
    #     table_log.port = "10000"
    #     table_log.operation = file_transfer.Add

    #     table = file_transfer.Table()
    #     table.cycle_number = cycle
    #     table.tableLog.extend([table_log])

    #     for client in lst_clients:
    #         client._RaftHeartbeat(table)

    #     time.sleep(1)

    # Server starts in background (another thread) so keep waiting
    while True:
        time.sleep(64 * 64 * 100)


if __name__ == '__main__':
    main(sys.argv[:])
