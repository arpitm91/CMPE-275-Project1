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

import sys
import traceback
from concurrent.futures import ThreadPoolExecutor

class ThreadPoolExecutorStackTraced(ThreadPoolExecutor):

    def submit(self, fn, *args, **kwargs):
        """Submits the wrapped function instead of `fn`"""

        return super(ThreadPoolExecutorStackTraced, self).submit(
            self._function_wrapper, fn, *args, **kwargs)

    def _function_wrapper(self, fn, *args, **kwargs):
        """Wraps `fn` in order to preserve the traceback of any kind of
        raised exception

        """
        try:
            return fn(*args, **kwargs)
        except Exception:
            raise sys.exc_info()[0](traceback.format_exc())  # Creates an
                                                             # exception of the
                                                             # same type with the
                                                             # traceback as
                                                             # message

class NodeState(Enum):
    CANDIDATE   = 0
    FOLLOWER    = 1
    LEADER      = 2

class Globals:
    LST_CLIENTS = []
    FILE_LOGS = []
    FILE_INFO_TABLE = {}

    NODE_STATE = NodeState.FOLLOWER
    CURRENT_CYCLE = 0
    HAS_CURRENT_VOTED = False
    MY_PORT = ""
    MY_IP = ""
    NUMBER_OF_VOTES = 0
    LEADER_PORT = ""
    LEADER_IP = ""
    HEARTBEAT_TIMEOUT = 2

    LAST_SENT_TABLE_LOG = 0

    CURRENT_LOG_INDEX = 0

def _increment_cycle_and_reset():
    Globals.CURRENT_CYCLE += 1
    Globals.HAS_CURRENT_VOTED = True
    Globals.NUMBER_OF_VOTES = 1
    Globals.LEADER_PORT = ""
    Globals.LEADER_IP = ""


def _random_timeout():
    log_info("_random_timeout: ", Globals.NODE_STATE, Globals.CURRENT_CYCLE)
    if Globals.NODE_STATE == NodeState.FOLLOWER:
        log_info("Standing for Election: ", Globals.MY_PORT)
        Globals.NODE_STATE = NodeState.CANDIDATE
        _increment_cycle_and_reset()
        _ask_for_vote()
    elif Globals.NODE_STATE == NodeState.LEADER:
        pass
    elif Globals.NODE_STATE == NodeState.CANDIDATE:
        _increment_cycle_and_reset()
        _ask_for_vote()

    random_timer.reset()

def _heartbeat_timeout():
    if Globals.NODE_STATE == NodeState.FOLLOWER:
        pass
    elif Globals.NODE_STATE == NodeState.LEADER:
        log_info("_heartbeat_timeout: ", Globals.NODE_STATE, Globals.CURRENT_CYCLE)
        log_info("Leader !!")
        _send_heartbeat()
    elif Globals.NODE_STATE == NodeState.CANDIDATE:
        log_info("_heartbeat_timeout: ", Globals.NODE_STATE, Globals.CURRENT_CYCLE)
        _ask_for_vote()
        _send_heartbeat()
    heartbeat_timer.reset()

random_timer = TimerUtil(_random_timeout)
heartbeat_timer = TimerUtil(_heartbeat_timeout, Globals.HEARTBEAT_TIMEOUT)

def _process_heartbeat(client,table, call_future):
    log_info("_process_heartbeat:",client.server_port)
    # log_info(client.server_port)
    # log_info(call_future.result())

def _process_request_for_vote(client,Candidacy, call_future):
    with ThreadPoolExecutorStackTraced(max_workers=10) as executor:
        try:
            candidacy_response = call_future.result()
        except:
            log_info("Exception Error !!", client.server_port)
            return


    if candidacy_response.voted == file_transfer.YES and candidacy_response.cycle_number == Globals.CURRENT_CYCLE:
        Globals.NUMBER_OF_VOTES += 1
        log_info("Got Vote:", Globals.NUMBER_OF_VOTES)
        if Globals.NUMBER_OF_VOTES / MAX_RAFT_NODES > 0.5 and Globals.NODE_STATE == NodeState.CANDIDATE:
            Globals.NODE_STATE = NodeState.LEADER
            Globals.LEADER_PORT = Globals.MY_PORT
            Globals.LEADER_IP = Globals.MY_IP
            _send_heartbeat()
            random_timer.reset()

def _send_heartbeat():
    table = file_transfer.Table()
    table.cycle_number = Globals.CURRENT_CYCLE
    table.leader_ip = Globals.MY_IP
    table.leader_port = Globals.MY_PORT

    # added_logs = Globals.FILE_LOGS[Globals.LAST_SENT_TABLE_LOG:]
    Globals.LAST_SENT_TABLE_LOG = len(Globals.FILE_LOGS)
    table.tableLog.extend(Globals.FILE_LOGS)

    for client in Globals.LST_CLIENTS:
        client._RaftHeartbit(table)

def _ask_for_vote():
    log_info("Asking for vote...", Globals.CURRENT_CYCLE)
    candidacy = file_transfer.Candidacy()
    candidacy.cycle_number = Globals.CURRENT_CYCLE
    candidacy.port = Globals.MY_PORT
    candidacy.ip = Globals.MY_IP
    candidacy.log_length = len(Globals.FILE_LOGS)

    for client in Globals.LST_CLIENTS:
        client._RequestVote(candidacy)

class Client:
    def __init__(self, username, server_address, server_port):
        self.username = username
        self.server_port = server_port
        # create a gRPC channel + stub
        channel = grpc.insecure_channel(server_address + ':' + str(server_port))
        self.conn = rpc.DataTransferServiceStub(channel)
        # create new listening thread for when new message streams come in
        # threading.Thread(target=self._RaftHeartbit, daemon=True).start()

    def _RaftHeartbit(self, table):
        try:
            call_future = self.conn.RaftHeartbit.future(table, timeout = Globals.HEARTBEAT_TIMEOUT * 0.9)
            call_future.add_done_callback(functools.partial(_process_heartbeat, self,table))
        except e:
            log_info("Exeption: _RaftHeartbit")

    def _RequestVote(self, Candidacy):
        call_future = self.conn.RequestVote.future(Candidacy, timeout = Globals.HEARTBEAT_TIMEOUT * 0.9)
        call_future.add_done_callback(functools.partial(_process_request_for_vote, self,Candidacy))

# server
class ChatServer(rpc.DataTransferServiceServicer):
    def __init__(self, username):
        self.username = username

    def RaftHeartbit(self, request: file_transfer.Table, context):

        log_info("heartbit arrived: ", len(Globals.FILE_LOGS))
        pprint.pprint(request)

        ack = file_transfer.Ack()

        if len(request.tableLog) > len(Globals.FILE_LOGS):

            Globals.NODE_STATE = NodeState.FOLLOWER
            Globals.CURRENT_CYCLE = request.cycle_number
            Globals.HAS_CURRENT_VOTED = False
            Globals.NUMBER_OF_VOTES = 0
            Globals.LEADER_PORT = request.leader_port
            Globals.LEADER_IP = request.leader_ip

        elif len(request.tableLog) == len(Globals.FILE_LOGS) and request.cycle_number > Globals.CURRENT_CYCLE:

            Globals.NODE_STATE = NodeState.FOLLOWER
            Globals.CURRENT_CYCLE = request.cycle_number
            Globals.HAS_CURRENT_VOTED = False
            Globals.NUMBER_OF_VOTES = 0
            Globals.LEADER_PORT = request.leader_port
            Globals.LEADER_IP = request.leader_ip


        elif request.leader_ip != Globals.LEADER_IP or request.leader_port != Globals.LEADER_PORT:
            ack.id = -1
            return ack

        random_timer.reset()
        log_info("MY Leader: ",Globals.LEADER_PORT, len(Globals.FILE_LOGS))

        Globals.FILE_LOGS = []
        for tl in request.tableLog:
            log_info("LOG Arrived: ")
            Globals.FILE_LOGS.append(tl)          
            if tl.operation == file_transfer.Remove:            
                if tl.file_number in Globals.FILE_INFO_TABLE and tl.chunk_number in Globals.FILE_INFO_TABLE[tl.file_number]:
                    Globals.FILE_INFO_TABLE[tl.file_number][tl.chunk_number].discard((tl.ip, tl.port))

            elif tl.operation == file_transfer.Add:
                if tl.file_number not in Globals.FILE_INFO_TABLE:
                    Globals.FILE_INFO_TABLE[tl.file_number] = {}
                
                if tl.chunk_number not in Globals.FILE_INFO_TABLE[tl.file_number]:
                    Globals.FILE_INFO_TABLE[tl.file_number][tl.chunk_number] = set()
                
                Globals.FILE_INFO_TABLE[tl.file_number][tl.chunk_number].add((tl.ip, tl.port))
        

        ack.id = len(Globals.FILE_LOGS)

        # pprint.pprint(Globals.FILE_INFO_TABLE)

        return ack


    def RequestVote(self, request: file_transfer.Candidacy, context):
        candidacy_response = file_transfer.CandidacyResponse()

        if request.log_length < len(Globals.FILE_LOGS):
            candidacy_response.voted = file_transfer.NO
        elif request.cycle_number > Globals.CURRENT_CYCLE or (request.cycle_number == Globals.CURRENT_CYCLE and not Globals.HAS_CURRENT_VOTED):
            Globals.CURRENT_CYCLE = request.cycle_number
            Globals.HAS_CURRENT_VOTED = True
            Globals.NUMBER_OF_VOTES = 0
            Globals.LEADER_IP = request.ip
            Globals.LEADER_PORT = request.port
            candidacy_response.voted = file_transfer.YES
            candidacy_response.cycle_number = request.cycle_number
            Globals.NODE_STATE = NodeState.FOLLOWER
            random_timer.reset()
            pprint.pprint("###")
            pprint.pprint(request)
        else:
            candidacy_response.voted = file_transfer.NO

        return candidacy_response

    def AddFileLog(self, request: file_transfer.TableLog, context):
        if Globals.NODE_STATE == NodeState.LEADER:
            request.log_index = Globals.CURRENT_LOG_INDEX
            Globals.CURRENT_LOG_INDEX += 1
            Globals.FILE_LOGS.append(request)
            log_info("LOG ADDED")
        ack = file_transfer.Ack()
        ack.id = 1
        return ack

def start_client(username, server_address, server_port):
    c = Client(username, server_address, server_port)


def start_server(username, my_port):
    # create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_object = ChatServer(username)
    rpc.add_DataTransferServiceServicer_to_server(server_object, server)

    log_info('Starting server. Listening...', my_port)
    server.add_insecure_port('[::]:' + str(my_port))
    server.start()

    # Server starts in background (another thread) so keep waiting
    while True:
        time.sleep(64 * 64 * 100)



def main(argv):
    username = argv[1]
    Globals.MY_PORT = connections.connections[username]["own"]["port"]
    Globals.MY_IP = connections.connections[username]["own"]["ip"]

    threading.Thread(target=start_server, args=(username, Globals.MY_PORT), daemon=True).start()

    for client in connections.connections[username]["clients"]:
        # client
        server_address = client["ip"]
        server_port = client["port"]
        c = Client(username, server_address, server_port)
        Globals.LST_CLIENTS.append(c)

        # threading.Thread(target=start_client, args=(username, server_address, server_port), daemon=True).start()
    random_timer.start()
    heartbeat_timer.start()

    # Server starts in background (another thread) so keep waiting
    while True:
        time.sleep(64 * 64 * 100)


if __name__ == '__main__':
    main(sys.argv[:])
