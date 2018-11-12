import threading
from concurrent import futures

import pprint
import grpc, functools
import time
import sys
import os
import math

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "protos"))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "utils"))

import raft_pb2 as raft
import raft_pb2_grpc as rpc

from input_output_util import log_info
from timer_utils import TimerUtil

from constants import CHUNK_SIZE

import configs.connections as connections
from configs.connections import MAX_RAFT_NODES

import traceback
from concurrent.futures import ThreadPoolExecutor

from globals import Globals
from globals import NodeState
from tables import Tables


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


def _raft_heartbeat_timeout():
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
    raft_heartbeat_timer.reset()


def _dc_heartbeat_timeout():
    if Globals.NODE_STATE == NodeState.LEADER:
        pass
    dc_heartbeat_timer.reset()


random_timer = TimerUtil(_random_timeout)
raft_heartbeat_timer = TimerUtil(_raft_heartbeat_timeout, Globals.RAFT_HEARTBEAT_TIMEOUT)
dc_heartbeat_timer = TimerUtil(_dc_heartbeat_timeout, Globals.DC_HEARTBEAT_TIMEOUT)


def _process_heartbeat(client, table, call_future):
    log_info("_process_heartbeat:", client.server_port)
    # log_info(client.server_port)
    # log_info(call_future.result())


def _process_request_for_vote(client, Candidacy, call_future):
    with ThreadPoolExecutorStackTraced(max_workers=10) as executor:
        try:
            candidacy_response = call_future.result()
        except:
            log_info("Exception Error !!", client.server_port)
            return

    if candidacy_response.voted == raft.YES and candidacy_response.cycle_number == Globals.CURRENT_CYCLE:
        Globals.NUMBER_OF_VOTES += 1
        log_info("Got Vote:", Globals.NUMBER_OF_VOTES)
        if Globals.NUMBER_OF_VOTES / MAX_RAFT_NODES > 0.5 and Globals.NODE_STATE == NodeState.CANDIDATE:
            Globals.NODE_STATE = NodeState.LEADER
            Globals.LEADER_PORT = Globals.MY_PORT
            Globals.LEADER_IP = Globals.MY_IP
            _send_heartbeat()
            random_timer.reset()


def _send_heartbeat():
    table = raft.Table()
    table.cycle_number = Globals.CURRENT_CYCLE
    table.leader_ip = Globals.MY_IP
    table.leader_port = Globals.MY_PORT

    # added_logs = Tables.FILE_LOGS[Globals.LAST_SENT_TABLE_LOG:]
    Globals.LAST_SENT_TABLE_LOG = len(Tables.FILE_LOGS)
    table.tableLog.extend(Tables.FILE_LOGS)

    for client in Globals.LST_CLIENTS:
        client._RaftHeartbit(table)


def _ask_for_vote():
    log_info("Asking for vote...", Globals.CURRENT_CYCLE)
    candidacy = raft.Candidacy()
    candidacy.cycle_number = Globals.CURRENT_CYCLE
    candidacy.port = Globals.MY_PORT
    candidacy.ip = Globals.MY_IP
    candidacy.log_length = len(Tables.FILE_LOGS)

    for client in Globals.LST_CLIENTS:
        client._RequestVote(candidacy)


def get_leader_client():
    client = None
    for c in Globals.LST_CLIENTS:
        if c.server_address == Globals.LEADER_IP and c.server_port == Globals.LEADER_PORT:
            client = c
            break
    return client


class Client:
    def __init__(self, username, server_address, server_port):
        self.username = username
        self.server_address = server_address
        self.server_port = server_port
        # create a gRPC channel + stub
        channel = grpc.insecure_channel(server_address + ':' + str(server_port))
        self.conn = rpc.DataTransferServiceStub(channel)
        # create new listening thread for when new message streams come in
        # threading.Thread(target=self._RaftHeartbit, daemon=True).start()

    def _RaftHeartbit(self, table):
        try:
            call_future = self.conn.RaftHeartbit.future(table, timeout=Globals.RAFT_HEARTBEAT_TIMEOUT * 0.9)
            call_future.add_done_callback(functools.partial(_process_heartbeat, self, table))
        except:
            log_info("Exeption: _RaftHeartbit")

    def _RequestVote(self, Candidacy):
        call_future = self.conn.RequestVote.future(Candidacy, timeout=Globals.RAFT_HEARTBEAT_TIMEOUT * 0.9)
        call_future.add_done_callback(functools.partial(_process_request_for_vote, self, Candidacy))

    def _RequestFileUpload(self, FileUploadInfo):
        return self.conn.RequestFileUpload(FileUploadInfo)

    def _ListFile(self, RequestFileList):
        return self.conn.ListFiles(RequestFileList)


# server
class ChatServer(rpc.DataTransferServiceServicer):
    def __init__(self, username):
        self.username = username

    '''
    request: raft.Table
    context:
    '''

    def RaftHeartbit(self, request, context):

        log_info("heartbit arrived: ", len(Tables.FILE_LOGS))

        ack = raft.Ack()

        if len(request.tableLog) > len(Tables.FILE_LOGS):

            Globals.NODE_STATE = NodeState.FOLLOWER
            Globals.CURRENT_CYCLE = request.cycle_number
            Globals.HAS_CURRENT_VOTED = False
            Globals.NUMBER_OF_VOTES = 0
            Globals.LEADER_PORT = request.leader_port
            Globals.LEADER_IP = request.leader_ip

        elif len(request.tableLog) == len(Tables.FILE_LOGS) and request.cycle_number > Globals.CURRENT_CYCLE:

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
        log_info("MY Leader: ", Globals.LEADER_PORT, len(Tables.FILE_LOGS))

        # Update Table_log and File_info_table
        Tables.set_file_log(request.tableLog)

        ack.id = len(Tables.FILE_LOGS)

        pprint.pprint(Tables.TABLE_FILE_INFO)

        return ack

    '''
    request: raft.Candidacy
    context:
    '''

    def RequestVote(self, request, context):
        candidacy_response = raft.CandidacyResponse()

        if request.log_length < len(Tables.FILE_LOGS):
            candidacy_response.voted = raft.NO
        elif request.cycle_number > Globals.CURRENT_CYCLE or (
                        request.cycle_number == Globals.CURRENT_CYCLE and not Globals.HAS_CURRENT_VOTED):
            Globals.CURRENT_CYCLE = request.cycle_number
            Globals.HAS_CURRENT_VOTED = True
            Globals.NUMBER_OF_VOTES = 0
            Globals.LEADER_IP = request.ip
            Globals.LEADER_PORT = request.port
            candidacy_response.voted = raft.YES
            candidacy_response.cycle_number = request.cycle_number
            Globals.NODE_STATE = NodeState.FOLLOWER
            random_timer.reset()
            pprint.pprint("###")
            pprint.pprint(request)
        else:
            candidacy_response.voted = raft.NO

        return candidacy_response

    '''
    request: raft.TableLog
    context:
    '''

    def AddFileLog(self, request, context):
        if Globals.NODE_STATE == NodeState.LEADER:
            request.log_index = Globals.get_next_log_index()
            Tables.FILE_LOGS.append(request)
            log_info("LOG ADDED")

            # Update Table_log and File_info_table
            Tables.set_file_log(Tables.FILE_LOGS)

        ack = raft.Ack()
        ack.id = 1
        return ack

    '''
    request: raft.FileUploadInfo
    context:
    '''

    def RequestFileUpload(self, request, context):

        if Globals.NODE_STATE == NodeState.LEADER:
            my_reply = raft.ProxyList()

            file_name = request.fileName
            file_size = request.fileSize
            total_chunks = math.ceil(file_size / CHUNK_SIZE)

            if Tables.is_file_exists(file_name):
                return my_reply

            for chunk_id in range(total_chunks):
                random_dcs = Tables.get_random_available_dc(Globals.REPLICATION_FACTOR)
                Tables.insert_file_chunk_info_to_file_log(file_name, chunk_id, random_dcs, raft.UploadRequested)

            pprint.pprint("TABLE_FILE_INFO")
            pprint.pprint(Tables.TABLE_FILE_INFO)

            lst_proxies = Tables.get_all_available_proxies()
            lst_proxy_info = []
            for ip, port in lst_proxies:
                proxy_info = raft.ProxyInfo()
                proxy_info.ip = ip
                proxy_info.port = port
                lst_proxy_info.append(proxy_info)

            my_reply.lstProxy.extend(lst_proxy_info)

            print("Replied to :")
            pprint.pprint(request)
            pprint.pprint(my_reply)
            print("############################")
            return my_reply

        else:
            client = get_leader_client()
            if client:
                my_reply = client._RequestFileUpload(request)
                return my_reply
            else:
                return raft.ProxyList()

    '''
    request: raft.RequestFileList
    context:
    '''

    def ListFiles(self, request, context):

        if Globals.NODE_STATE == NodeState.LEADER:
            my_reply = raft.FileList()
            my_reply.lstFileNames.extend(Tables.get_all_available_file_list())
            return my_reply
        else:
            client = get_leader_client()
            if client:
                my_reply = client._ListFile(request)
                return my_reply
            else:
                return raft.FileList()

    '''
    request: raft.FileInfo
    context:
    '''

    def RequestFileInfo(self, request, context):
        my_reply = raft.FileLocationInfo()
        file_name = request.fileName
        is_file_found = True
        if file_name not in Tables.TABLE_FILE_INFO.keys():
            is_file_found = False

        max_chunks = len(Tables.TABLE_FILE_INFO[file_name].keys())

        lst_proxies = Tables.get_all_available_proxies()
        lst_proxy_info = []
        for ip, port in lst_proxies:
            proxy_info = raft.ProxyInfo()
            proxy_info.ip = ip
            proxy_info.port = port
            lst_proxy_info.append(proxy_info)

        my_reply.fileName = file_name
        my_reply.maxChunks = max_chunks
        my_reply.lstProxy.extend(lst_proxy_info)
        my_reply.isFileFound = is_file_found
        return my_reply

    '''
    request: raft.DataCenterInfo
    context:
    '''

    def AddDataCenter(self, request, context):
        Tables.register_dc(request.ip, request.port)
        return raft.Empty()


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

    # Init Data-center Table
    Tables.init_dc(connections.data_centers)
    # Init Proxies Table
    Tables.init_proxies(connections.lst_proxies)

    for client in connections.connections[username]["clients"]:
        # client
        server_address = client["ip"]
        server_port = client["port"]
        c = Client(username, server_address, server_port)
        Globals.LST_CLIENTS.append(c)

        # threading.Thread(target=start_client, args=(username, server_address, server_port), daemon=True).start()
    random_timer.start()
    raft_heartbeat_timer.start()

    # Server starts in background (another thread) so keep waiting
    while True:
        time.sleep(64 * 64 * 100)


if __name__ == '__main__':
    main(sys.argv[:])

    # TODO:
    # 1. Make TABLE_LOG a set
    # 2. Node should have map for last_log_index sent to each other node (last_log_index is updated on ack)
    # 3. Should only sent TABLE_LOG to other node starting from last_log_index for that node
    #
    # 4. Should not commit log before acknowledged from more than half of the nodes
    # 5. Instead of using MAX_RAFT_NODES, MAX_RAFT_NODES should be calculated from array
