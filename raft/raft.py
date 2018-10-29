import threading
from concurrent import futures
from collections import defaultdict
from random import random
from enum import Enum

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

from utils.timer_utils import TimerUtil
import configs.connections as connections

from configs.connections import MAX_RAFT_NODES

lst_clients = []

file_logs = []
file_info_table = {}

class NodeState(Enum):
    CANDIDATE   = 0
    FOLLOWER    = 1
    LEADER      = 2

NODE_STATE = NodeState.FOLLOWER
CURRENT_CYCLE = 0
HAS_CURRENT_VOTED = False
MY_PORT = ""
MY_IP = ""
NUMBER_OF_VOTES = 0
LEADER_PORT = ""
LEADER_IP = ""
HEARTBEAT_TIMEOUT = 0.5

def _increment_cycle_and_reset():
    CURRENT_CYCLE += 1
    HAS_CURRENT_VOTED = True
    NUMBER_OF_VOTES = 1
    LEADER_PORT = ""
    LEADER_IP = ""


def _random_timeout():
    print("Timeout !!!")
    global NODE_STATE
    if NODE_STATE == NodeState.FOLLOWER:
        NODE_STATE = NodeState.CANDIDATE
        _increment_cycle_and_reset()
        _ask_for_vote()
    elif NODE_STATE == NodeState.LEADER:
        pass
    elif NODE_STATE == NodeState.CANDIDATE:
        _increment_cycle_and_reset()
        _ask_for_vote()

    random_timer.reset()

def _heartbeat_timeout():
    global NODE_STATE
    if NODE_STATE == NodeState.FOLLOWER:
        pass
    elif NODE_STATE == NodeState.LEADER:
        _send_heartbeat()
    elif NODE_STATE == NodeState.CANDIDATE:
        _ask_for_vote()
    heartbeat_timer.reset()

random_timer = TimerUtil(_random_timeout)
heartbeat_timer = TimerUtil(_heartbeat_timeout, HEARTBEAT_TIMEOUT)

def _process_heartbeat(client, call_future):
    print(client.server_port)
    print(call_future.result())

def _process_request_for_vote(client, call_future):
    global NUMBER_OF_VOTES, NODE_STATE, LEADER_PORT, LEADER_IP
    NUMBER_OF_VOTES += 1
    if NUMBER_OF_VOTES / MAX_RAFT_NODES > 0.5 and NODE_STATE == NodeState.CANDIDATE:
        NODE_STATE = NodeState.LEADER
        LEADER_PORT = MY_PORT
        LEADER_IP = MY_IP
        _send_heartbeat()
        random_timer.start()

    print(client.server_port)
    print(call_future.result())

def _send_heartbeat():
    table = file_transfer.Table()
    table.cycle_number = CURRENT_CYCLE
    table.leader_ip = MY_IP
    table.leader_port = MY_PORT
    table.tableLog.extend([])

    for client in lst_clients:
        client._RaftHeartbit(table)

def _ask_for_vote():
    candidacy = file_transfer.Candidacy()
    candidacy.cycle_number = CURRENT_CYCLE
    candidacy.port = MY_PORT
    candidacy.ip = MY_IP
    candidacy.log_length = len(file_logs)

    for client in lst_clients:
        client._RequestVote(candidacy)

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
        call_future.add_done_callback(functools.partial(_process_heartbeat, self))

    def _RequestVote(self, Candidacy):
        call_future = self.conn.RequestVote.future(Candidacy)
        call_future.add_done_callback(functools.partial(_process_request_for_vote, self))

# server
class ChatServer(rpc.DataTransferServiceServicer):
    def __init__(self, username):
        self.username = username

    def RaftHeartbit(self, request: file_transfer.Table, context):
        global CURRENT_CYCLE, LEADER_IP, LEADER_PORT
        ack = file_transfer.Ack()

        if request.cycle_number > CURRENT_CYCLE:
            NODE_STATE = NodeState.FOLLOWER
            CURRENT_CYCLE = request.cycle_number
            HAS_CURRENT_VOTED = False
            NUMBER_OF_VOTES = 0
            LEADER_PORT = request.leader_port
            LEADER_IP = request.leader_ip

        elif request.leader_ip != LEADER_IP or request.leader_port != LEADER_PORT:
            ack.id = -1
            return ack

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
        

        ack.id = len(file_logs)

        print("##############################")        
        pprint.pprint(file_info_table)

        return ack


    def RequestVote(self, request: file_transfer.Candidacy, context):
        global CURRENT_CYCLE, HAS_CURRENT_VOTED
        candidacy_response = file_transfer.CandidacyResponse()

        if request.log_length < len(file_logs):
            candidacy_response.voted = file_transfer.NO
        elif CURRENT_CYCLE < request.cycle_number and not HAS_CURRENT_VOTED:
            CURRENT_CYCLE = request.cycle_number
            HAS_CURRENT_VOTED = True
            NUMBER_OF_VOTES = 0
            LEADER_IP = request.ip
            LEADER_PORT = request.port
            candidacy_response.voted = file_transfer.YES
            NODE_STATE = NodeState.FOLLOWER
            random_timer.reset()
        else:
            candidacy_response.voted = file_transfer.NO

        return candidacy_response


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
    MY_PORT = connections.connections[username]["own"]["port"]
    MY_IP = connections.connections[username]["own"]["ip"]

    threading.Thread(target=start_server, args=(username, MY_PORT), daemon=True).start()

    for client in connections.connections[username]["clients"]:
        # client
        server_address = client["ip"]
        server_port = client["port"]
        c = Client(username, server_address, server_port)
        lst_clients.append(c)

        # threading.Thread(target=start_client, args=(username, server_address, server_port), daemon=True).start()
    random_timer.start()
    heartbeat_timer.start()

    # cycle = 0
    #
    # while True:
    #     cycle += 1
    #     table_log = file_transfer.TableLog()
    #     table_log.file_number = "f1"
    #     table_log.chunk_number = "c1"
    #     table_log.ip = "10.0.0.1"
    #     table_log.port = "10000"
    #     table_log.operation = file_transfer.Add
    #
    #     table = file_transfer.Table()
    #     table.cycle_number = cycle
    #     table.tableLog.extend([table_log])
    #
    #     for client in lst_clients:
    #         client._RaftHeartbit(table)
    #
    #     time.sleep(5)

    # Server starts in background (another thread) so keep waiting
    while True:
        time.sleep(64 * 64 * 100)


if __name__ == '__main__':
    main(sys.argv[:])
