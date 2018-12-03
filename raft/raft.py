import threading
from concurrent import futures
from multiprocessing.dummy import Pool as ThreadPool
import pprint
import grpc
import functools
import time
import sys
import os
import math

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "protos"))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "utils"))

import raft_pb2 as raft_proto
import raft_pb2_grpc as raft_proto_rpc
import file_transfer_pb2 as file_transfer_proto
import file_transfer_pb2_grpc as file_transfer_proto_rpc

from constants import CHUNK_SIZE
from constants import HEARTBEAT_PORT_INCREMENT

from connections.connections import raft_connections as raft_connections
from connections.connections import other_raft_nodes as other_raft_nodes
from connections.connections import MAX_RAFT_NODES as MAX_RAFT_NODES

from globals import Globals
from globals import NodeState
from globals import ThreadPoolExecutorStackTraced
from tables import Tables
from tables import dc_heartbeat_timer
from tables import proxy_heartbeat_timer
from tables import Check_and_send_replication_request
from utils.input_output_util import log_info
from utils.timer_utils import TimerUtil
from utils.common_utils import get_rand_hashing_node


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
        print("Leader !!")
        _send_heartbeat()
    elif Globals.NODE_STATE == NodeState.CANDIDATE:
        log_info("_heartbeat_timeout: ", Globals.NODE_STATE, Globals.CURRENT_CYCLE)
        _ask_for_vote()
        _send_heartbeat()
    raft_heartbeat_timer.reset()


def _dc_replication_timeout():
    if Globals.NODE_STATE == NodeState.LEADER:
        Check_and_send_replication_request()
    dc_replication_timer.reset()


random_timer = TimerUtil(_random_timeout)
raft_heartbeat_timer = TimerUtil(_raft_heartbeat_timeout, Globals.RAFT_HEARTBEAT_TIMEOUT)
dc_replication_timer = TimerUtil(_dc_replication_timeout, Globals.DC_REPLICATION_TIMEOUT)


def _process_heartbeat(client, table, heartbeat_counter, call_future):
    with ThreadPoolExecutorStackTraced(max_workers=10) as executor:
        try:
            call_future.result()
            Globals.RAFT_HEARTBEAT_ACK_DICT[(client.server_address, client.server_port)] = (heartbeat_counter, True)
        except:
            Globals.RAFT_HEARTBEAT_ACK_DICT[(client.server_address, client.server_port)] = (heartbeat_counter, False)
            log_info("Raft node not available!!", client.server_address, client.server_port)


def _send_heartbeat_to_check_majority_consensus():
    heartbeat_counter = _send_heartbeat()
    start_time = time.time()
    while True:
        if (time.time() - start_time) > (2 * Globals.RAFT_HEARTBEAT_TIMEOUT):
            return False

        available_raft_nodes = 1
        total_response = 0
        for raft_node, hb_info in Globals.RAFT_HEARTBEAT_ACK_DICT.items():
            if hb_info[0] >= heartbeat_counter:
                total_response += 1
                if hb_info[1] is True:
                    available_raft_nodes += 1

        if available_raft_nodes > (len(Globals.LST_RAFT_CLIENTS) + 1) / 2:
            return True

        if total_response == len(Globals.LST_RAFT_CLIENTS):
            return False

        time.sleep(0.01)

    return False


def _send_heartbeat():
    table = raft_proto.Table()
    table.cycle_number = Globals.CURRENT_CYCLE
    table.leader_ip = Globals.MY_IP
    table.leader_port = Globals.MY_PORT

    Globals.RAFT_HEARTBEAT_COUNTER += 1

    Globals.LAST_SENT_TABLE_LOG = len(Tables.FILE_LOGS)
    table.tableLog.extend(Tables.FILE_LOGS)

    for client in Globals.LST_RAFT_CLIENTS:
        client._RaftHeartbeat(table, Globals.RAFT_HEARTBEAT_COUNTER)

    return Globals.RAFT_HEARTBEAT_COUNTER


def _process_request_for_vote(client, Candidacy, call_future):
    with ThreadPoolExecutorStackTraced(max_workers=10) as executor:
        try:
            candidacy_response = call_future.result()
        except:
            log_info("Exception Error !!", client.server_port)
            return

    if candidacy_response.voted == raft_proto.YES and candidacy_response.cycle_number == Globals.CURRENT_CYCLE:
        Globals.NUMBER_OF_VOTES += 1
        log_info("Got Vote:", Globals.NUMBER_OF_VOTES)
        if Globals.NUMBER_OF_VOTES / MAX_RAFT_NODES > 0.5 and Globals.NODE_STATE == NodeState.CANDIDATE:
            Globals.NODE_STATE = NodeState.LEADER
            Globals.LEADER_PORT = Globals.MY_PORT
            Globals.LEADER_IP = Globals.MY_IP
            _send_heartbeat()
            random_timer.reset()


def _ask_for_vote():
    log_info("Asking for vote...", Globals.CURRENT_CYCLE)
    candidacy = raft_proto.Candidacy()
    candidacy.cycle_number = Globals.CURRENT_CYCLE
    candidacy.port = Globals.MY_PORT
    candidacy.ip = Globals.MY_IP
    candidacy.log_length = len(Tables.FILE_LOGS)

    for client in Globals.LST_RAFT_CLIENTS:
        client._RequestVote(candidacy)


def get_leader_client():
    client = None
    for c in Globals.LST_RAFT_CLIENTS:
        if c.server_address == Globals.LEADER_IP and c.server_port == Globals.LEADER_PORT:
            client = c
            break
    return client


def request_file_info_from_other_raft_nodes(request):
    cur_time = time.time()
    for node in other_raft_nodes:
        availability = Tables.NOT_AVAILABLE_OTHER_RAFT_NODES[(node["ip"], node["port"])]
        if availability[0]:
            if (cur_time - availability[1]) < Globals.CACHE_DIRTY_TIME:
                continue
            else:
                Tables.NOT_AVAILABLE_OTHER_RAFT_NODES[(node["ip"], node["port"])] = (False, 0)

        try:
            stub = file_transfer_proto_rpc.DataTransferServiceStub(
                grpc.insecure_channel(node["ip"] + ':' + node["port"]))
            file_location_info = stub.GetFileLocation(request)
            log_info("Response received From other Raft: ")
            # pprint.pprint(file_location_info)
            log_info(file_location_info.maxChunks)
            log_info("is file found in other Raft:", file_location_info.isFileFound)
            if file_location_info.isFileFound:
                return file_location_info
        except:
            log_info("Fail to connect to: ", node["ip"], node["port"])
            Tables.NOT_AVAILABLE_OTHER_RAFT_NODES[(node["ip"], node["port"])] = (True, time.time())
    file_location_info = file_transfer_proto.FileLocationInfo()
    file_location_info.isFileFound = False
    return file_location_info


def request_file_list_from_other_raft_nodes(request):
    request.isClient = False
    set_files = set()
    # thread_pool_size = 4
    # pool = ThreadPool(thread_pool_size)


    threads = []

    def send_request_to_other_raft_nodes(other_node, return_set):

        try:
            stub = file_transfer_proto_rpc.DataTransferServiceStub(
                grpc.insecure_channel(other_node["ip"] + ':' + other_node["port"]))
            files = stub.ListFiles(request, timeout=1)
            for file_name in files.lstFileNames:
                return_set.add(file_name)
        except:
            log_info("Fail to connect to: ", other_node["ip"], other_node["port"])
            Tables.NOT_AVAILABLE_OTHER_RAFT_NODES[(other_node["ip"], other_node["port"])] = (True, time.time())

    cur_time = time.time()

    for node in other_raft_nodes:

        availability = Tables.NOT_AVAILABLE_OTHER_RAFT_NODES[(node["ip"], node["port"])]
        if availability[0]:
            if (cur_time - availability[1]) < Globals.CACHE_DIRTY_TIME:
                continue
            else:
                Tables.NOT_AVAILABLE_OTHER_RAFT_NODES[(node["ip"], node["port"])] = (False, 0)

        threads.append(
            threading.Thread(target=send_request_to_other_raft_nodes, args=(node, set_files)))
        threads[-1].start()

    for t in threads:
        t.join()
    threads.clear()

    return list(set_files)


def get_file_lists(request):
    lst_files = []
    if request.isClient:
        lst_files = request_file_list_from_other_raft_nodes(request)

    lst_files = lst_files + Tables.get_all_available_file_list()
    my_reply = file_transfer_proto.FileList()
    # pprint.pprint("lst_files")
    # pprint.pprint(lst_files)
    if len(lst_files) > 0:
        my_reply.lstFileNames.extend(lst_files)
    return my_reply


class Client:
    def __init__(self, username, server_address, server_port):
        self.username = username
        self.server_address = server_address
        self.server_port = server_port
        # create a gRPC channel + stub
        channel = grpc.insecure_channel(server_address + ':' + str(server_port))
        self.raft_stub = raft_proto_rpc.RaftServiceStub(channel)
        self.file_transfer_stub = file_transfer_proto_rpc.DataTransferServiceStub(channel)

        heartbeat_channel = grpc.insecure_channel(server_address + ':' + str(server_port + HEARTBEAT_PORT_INCREMENT))
        self.raft_heartbeat_stub = raft_proto_rpc.RaftServiceStub(heartbeat_channel)

        # create new listening thread for when new message streams come in
        # threading.Thread(target=self._RaftHeartbeat, daemon=True).start()

    def _RaftHeartbeat(self, table, heartbeat_counter):
        try:
            call_future = self.raft_heartbeat_stub.RaftHeartbeat.future(table,
                                                                        timeout=Globals.RAFT_HEARTBEAT_TIMEOUT * 0.9)
            call_future.add_done_callback(functools.partial(_process_heartbeat, self, table, heartbeat_counter))
        except:
            log_info("Exception: _RaftHeartbeat")

    def _RequestVote(self, Candidacy):
        call_future = self.raft_heartbeat_stub.RequestVote.future(Candidacy,
                                                                  timeout=Globals.RAFT_HEARTBEAT_TIMEOUT * 0.9)
        call_future.add_done_callback(functools.partial(_process_request_for_vote, self, Candidacy))

    def _RequestFileUpload(self, FileUploadInfo):
        return self.file_transfer_stub.RequestFileUpload(FileUploadInfo)

    def _ListFile(self, RequestFileList):
        return self.file_transfer_stub.ListFiles(RequestFileList)

    def _FileUploadCompleted(self, UploadCompleteFileInfo):
        return self.raft_stub.FileUploadCompleted(UploadCompleteFileInfo)

    def _AddDataCenter(self, DataCenterInfo):
        return self.raft_stub.AddDataCenter(DataCenterInfo)

    def _AddProxy(self, ProxyInfo):
        return self.raft_stub.AddProxy(ProxyInfo)

    def _GetChunkUploadInfo(self, RequestChunkInfo):
        return self.raft_stub.GetChunkUploadInfo(RequestChunkInfo)


class HeartbeatServer(raft_proto_rpc.RaftServiceServicer, file_transfer_proto_rpc.DataTransferServiceServicer):
    def __init__(self, username):
        self.username = username

    '''
    request: raft.Table
    context:
    '''

    def RaftHeartbeat(self, request, context):

        log_info("heartbeat arrived: ", len(Tables.FILE_LOGS))

        ack = raft_proto.Ack()

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
        print("MY Leader: ", Globals.LEADER_IP, Globals.LEADER_PORT, len(Tables.FILE_LOGS))

        # Update Table_log and File_info_table
        Tables.set_table_log(request.tableLog)

        ack.id = len(Tables.FILE_LOGS)

        log_info("Tables.TABLE_FILE_INFO")
        pprint.pprint(Tables.TABLE_FILE_INFO)
        log_info("Tables.TABLE_PROXY_INFO")
        pprint.pprint(Tables.TABLE_PROXY_INFO)
        log_info("Tables.TABLE_DC_INFO")
        pprint.pprint(Tables.TABLE_DC_INFO)

        log_info("###########################################################")

        return ack

    '''
    request: raft.Candidacy
    context:
    '''

    def RequestVote(self, request, context):
        candidacy_response = raft_proto.CandidacyResponse()

        if request.log_length < len(Tables.FILE_LOGS):
            candidacy_response.voted = raft_proto.NO
        elif request.cycle_number > Globals.CURRENT_CYCLE or (
                        request.cycle_number == Globals.CURRENT_CYCLE and not Globals.HAS_CURRENT_VOTED):
            Globals.CURRENT_CYCLE = request.cycle_number
            Globals.HAS_CURRENT_VOTED = True
            Globals.NUMBER_OF_VOTES = 0
            Globals.LEADER_IP = request.ip
            Globals.LEADER_PORT = request.port
            candidacy_response.voted = raft_proto.YES
            candidacy_response.cycle_number = request.cycle_number
            Globals.NODE_STATE = NodeState.FOLLOWER
            random_timer.reset()
            # pprint.pprint("###")
            # pprint.pprint(request)
        else:
            candidacy_response.voted = raft_proto.NO

        return candidacy_response


# server
class ChatServer(raft_proto_rpc.RaftServiceServicer, file_transfer_proto_rpc.DataTransferServiceServicer):
    def __init__(self, username):
        self.username = username

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
            Tables.set_table_log(Tables.FILE_LOGS)

        ack = raft_proto.Ack()
        ack.id = 1
        return ack

    '''
    request: raft.FileUploadInfo
    context:
    '''

    def RequestFileUpload(self, request, context):

        if Globals.NODE_STATE == NodeState.LEADER:
            my_reply = file_transfer_proto.ProxyList()

            file_name = request.fileName
            file_size = request.fileSize
            total_chunks = math.ceil(file_size / CHUNK_SIZE)

            if Tables.is_file_exists(file_name):
                return my_reply

            dcs = Tables.get_all_available_dc()

            if len(dcs) == 0:
                return my_reply

            if not _send_heartbeat_to_check_majority_consensus():
                return my_reply

            for chunk_id in range(total_chunks):
                random_dcs = [get_rand_hashing_node(dcs, file_name, chunk_id)]
                Tables.insert_file_chunk_info_to_file_log(file_name, chunk_id, random_dcs, raft_proto.UploadRequested)

            _send_heartbeat()

            # pprint.pprint("TABLE_FILE_INFO")
            # pprint.pprint(Tables.TABLE_FILE_INFO)
            # pprint.pprint(Tables.TABLE_DC_INFO)

            lst_proxies = Tables.get_all_available_proxies()
            lst_proxy_info = []
            for ip, port in lst_proxies:
                proxy_info = file_transfer_proto.ProxyInfo()
                proxy_info.ip = ip
                proxy_info.port = port
                lst_proxy_info.append(proxy_info)

            log_info("LST_PROXIES:")
            log_info(my_reply.lstProxy)
            my_reply.lstProxy.extend(lst_proxy_info)

            log_info("Replied to :")
            # pprint.pprint(request)
            # pprint.pprint(my_reply)
            log_info("############################")
            return my_reply

        else:
            client = get_leader_client()
            if client:
                my_reply = client._RequestFileUpload(request)
                return my_reply
            else:
                return file_transfer_proto.ProxyList()

    '''
    request: raft.RequestFileList
    context:
    '''

    def ListFiles(self, request, context):
        if Globals.NODE_STATE == NodeState.LEADER or request.isClient:
            return get_file_lists(request)
        else:
            return file_transfer_proto.FileList()

    '''
    request: raft.FileInfo
    context:
    '''

    def RequestFileInfo(self, request, context):
        my_reply = file_transfer_proto.FileLocationInfo()
        file_name = request.fileName
        is_file_found = True
        if file_name not in Tables.TABLE_FILE_INFO.keys():
            my_reply = request_file_info_from_other_raft_nodes(request)
            return my_reply
        else:
            max_chunks = len(Tables.TABLE_FILE_INFO[file_name].keys())
            log_info("max_chunks from raft ", max_chunks)
            lst_proxies = Tables.get_all_available_proxies()
            lst_proxy_info = []
            for ip, port in lst_proxies:
                proxy_info = file_transfer_proto.ProxyInfo()
                proxy_info.ip = ip
                proxy_info.port = port
                lst_proxy_info.append(proxy_info)

        my_reply.fileName = file_name
        my_reply.maxChunks = max_chunks
        my_reply.lstProxy.extend(lst_proxy_info)
        my_reply.isFileFound = is_file_found
        return my_reply

    '''
    request: raft.FileInfo
    '''

    def GetFileLocation(self, request, context):
        my_reply = file_transfer_proto.FileLocationInfo()
        file_name = request.fileName
        is_file_found = True
        if file_name not in Tables.TABLE_FILE_INFO.keys():
            # is_file_found = False
            return my_reply

        max_chunks = len(Tables.TABLE_FILE_INFO[file_name].keys())
        log_info("max_chunks from raft ", max_chunks)
        lst_proxies = Tables.get_all_available_proxies()
        lst_proxy_info = []
        for ip, port in lst_proxies:
            proxy_info = file_transfer_proto.ProxyInfo()
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
        if Globals.NODE_STATE == NodeState.LEADER:
            if not _send_heartbeat_to_check_majority_consensus():
                ack = raft_proto.Ack()
                ack.id = -1
                return ack

            Tables.register_dc(request.ip, request.port)
            _send_heartbeat()
            return raft_proto.Ack()
        else:
            client = get_leader_client()
            if client:
                my_reply = client._AddDataCenter(request)
                return my_reply
            else:
                ack = raft_proto.Ack()
                ack.id = -1
                return ack

    '''
    request: raft.ProxyInfo
    context:
    '''

    def AddProxy(self, request, context):
        if Globals.NODE_STATE == NodeState.LEADER:
            if not _send_heartbeat_to_check_majority_consensus():
                ack = raft_proto.Ack()
                ack.id = -1
                return ack

            Tables.register_proxy(request.ip, request.port)
            _send_heartbeat()
            return raft_proto.Ack()
        else:
            client = get_leader_client()
            if client:
                my_reply = client._AddProxy(request)
                return my_reply
            else:
                ack = raft_proto.Ack()
                ack.id = -1
                return ack

    '''
    request: raft.UploadCompleteFileInfo
    '''

    def FileUploadCompleted(self, request, context):

        log_info(
            "################################### FILE_UPLOAD_COMPLETED_ARRIVED!!! #################################")
        # pprint.pprint(request)
        log_info("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

        if Globals.NODE_STATE == NodeState.LEADER:
            chunk_id = request.chunkUploadInfo.chunkId
            lst_dc = [(request.chunkUploadInfo.uploadedDatacenter.ip, request.chunkUploadInfo.uploadedDatacenter.port)]

            if not _send_heartbeat_to_check_majority_consensus():
                response = raft_proto.Ack()
                response.id = -1
                return response

            Tables.insert_file_chunk_info_to_file_log(request.fileName, chunk_id, lst_dc,
                                                      raft_proto.Uploaded if request.isSuccess else raft_proto.UploadFaied)
            _send_heartbeat()

            # pprint.pprint(Tables.TABLE_FILE_INFO)
            log_info("###########################################################################")
            return raft_proto.Ack()
        else:
            client = get_leader_client()
            if client:
                my_reply = client._FileUploadCompleted(request)
                return my_reply
            else:
                response = raft_proto.Ack()
                response.id = -1
                return response

    '''
        request: raft.RequestChunkInfo
    '''

    def GetChunkLocationInfo(self, request, context):
        lst_dc = []
        is_chunk_found = False

        for dc in Tables.TABLE_FILE_INFO[request.fileName][request.chunkId].keys():
            if Tables.TABLE_FILE_INFO[request.fileName][request.chunkId][dc] == raft_proto.Uploaded:
                dc_info = raft_proto.DataCenterInfo()
                dc_info.ip = dc[0]
                dc_info.port = dc[1]
                lst_dc.append(dc_info)
                is_chunk_found = True

        chunk_location_info = raft_proto.ChunkLocationInfo()
        chunk_location_info.fileName = request.fileName
        chunk_location_info.chunkId = request.chunkId
        chunk_location_info.lstDataCenter.extend(lst_dc)
        chunk_location_info.isChunkFound = is_chunk_found

        return chunk_location_info

    '''
        request: raft.RequestChunkInfo
    '''

    def GetChunkUploadInfo(self, request, context):

        if (request.fileName not in Tables.TABLE_FILE_INFO or request.chunkId not in Tables.TABLE_FILE_INFO[
            request.fileName]) and Globals.NODE_STATE != NodeState.LEADER:
            client = get_leader_client()
            if client:
                my_reply = client._GetChunkUploadInfo(request)
                return my_reply
            else:
                return
        else:
            lst_dc = []
            is_chunk_found = False

            for dc in Tables.TABLE_FILE_INFO[request.fileName][request.chunkId].keys():
                if Tables.TABLE_FILE_INFO[request.fileName][request.chunkId][dc] == raft_proto.UploadRequested:
                    dc_info = raft_proto.DataCenterInfo()
                    dc_info.ip = dc[0]
                    dc_info.port = dc[1]
                    lst_dc.append(dc_info)
                    is_chunk_found = True

            chunk_location_info = raft_proto.ChunkLocationInfo()
            chunk_location_info.fileName = request.fileName
            chunk_location_info.chunkId = request.chunkId
            chunk_location_info.lstDataCenter.extend(lst_dc)
            chunk_location_info.isChunkFound = is_chunk_found

            return chunk_location_info


def start_client(username, server_address, server_port):
    c = Client(username, server_address, server_port)


def start_server(username, my_port):
    # create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_object = ChatServer(username)
    raft_proto_rpc.add_RaftServiceServicer_to_server(server_object, server)
    file_transfer_proto_rpc.add_DataTransferServiceServicer_to_server(server_object, server)
    log_info('Starting server. Listening...', my_port)
    server.add_insecure_port('[::]:' + str(my_port))
    server.start()

    server_heartbeat = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_heartbeat_object = HeartbeatServer(username)
    raft_proto_rpc.add_RaftServiceServicer_to_server(server_heartbeat_object, server_heartbeat)
    file_transfer_proto_rpc.add_DataTransferServiceServicer_to_server(server_heartbeat_object, server_heartbeat)
    log_info('Starting server. Listening...', my_port + HEARTBEAT_PORT_INCREMENT)
    server_heartbeat.add_insecure_port('[::]:' + str(int(my_port) + HEARTBEAT_PORT_INCREMENT))
    server_heartbeat.start()

    # Server starts in background (another thread) so keep waiting
    while True:
        time.sleep(64 * 64 * 100)


def start_background_services():
    random_timer.start()
    raft_heartbeat_timer.start()
    dc_heartbeat_timer.start()
    proxy_heartbeat_timer.start()
    dc_replication_timer.start()


def main(argv):
    username = argv[1]
    Globals.MY_PORT = raft_connections[username]["own"]["port"]
    Globals.MY_IP = raft_connections[username]["own"]["ip"]

    threading.Thread(target=start_server, args=(username, Globals.MY_PORT), daemon=True).start()

    # # Init Data-center Table
    # Tables.init_dc(connections.data_centers)
    # # Init Proxies Table
    # Tables.init_proxies(connections.lst_proxies)

    for client in raft_connections[username]["clients"]:
        # client
        server_address = client["ip"]
        server_port = client["port"]
        c = Client(username, server_address, server_port)
        Globals.LST_RAFT_CLIENTS.append(c)

        Globals.RAFT_HEARTBEAT_ACK_DICT[(server_address, server_port)] = (0, False)

        # threading.Thread(target=start_client, args=(username, server_address, server_port), daemon=True).start()

    for node in other_raft_nodes:
        Tables.NOT_AVAILABLE_OTHER_RAFT_NODES[(node["ip"], node["port"])] = (False, 0)

    threading.Thread(target=start_background_services, args=(), daemon=True).start()

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
