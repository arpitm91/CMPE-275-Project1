import sys
import os
from collections import defaultdict
import pprint
import grpc, functools

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "protos"))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "utils"))

from timer_utils import TimerUtil

from input_output_util import log_info
from common_utils import get_random_numbers
from globals import Globals
from globals import ThreadPoolExecutorStackTraced
from globals import NodeState

import raft_pb2 as raft_proto
import raft_pb2_grpc as raft_proto_rpc
import file_transfer_pb2 as file_transfer_proto
import file_transfer_pb2_grpc as file_transfer_proto_rpc

class Tables:
    FILE_LOGS = []

    #
    # "fileName" : {
    #           "chunkId1" : {
    #                           (ip1, port1) : raft.UploadRequested
    #                           (ip2, port2) : raft.Uploaded
    #                        }
    #           "chunkId2" : {
    #                           (ip1, port1) : raft.UploadFailed
    #                           (ip2, port2) : raft.Deleted
    #                        }
    # }
    #
    TABLE_FILE_INFO = defaultdict(dict)

    # Key: (ip1, port1), Value: True/False (DC Available or Not)
    TABLE_DC_INFO = {}

    # Key: (ip1, port1), Value: True/False (Proxy Available or Not)
    TABLE_PROXY_INFO = {}

    @staticmethod
    def init_proxies(lst_proxies):
        for ip, port in lst_proxies:
            Tables.TABLE_PROXY_INFO[(ip, port)] = True
            # TODO: Set False by default

    @staticmethod
    def register_proxy(proxy_ip, proxy_port):
        Tables.TABLE_PROXY_INFO[(proxy_ip, proxy_port)] = True

    @staticmethod
    def un_register_proxy(proxy_ip, proxy_port):
        Tables.TABLE_PROXY_INFO[(proxy_ip, proxy_port)] = False

    @staticmethod
    def get_all_available_proxies():
        lst_proxies = set()
        for ip, port in Tables.TABLE_PROXY_INFO.keys():
            if Tables.TABLE_PROXY_INFO[(ip, port)]:
                lst_proxies.add((ip, port))
        return lst_proxies

    @staticmethod
    def init_dc(lst_data_centers):
        for ip, port in lst_data_centers:
            dc_client = DatacenterClient("", ip, port)
            Globals.add_dc_client(dc_client)

            Tables.TABLE_DC_INFO[(ip, port)] = True
            # TODO: Set False by default

    @staticmethod
    def register_dc(dc_ip, dc_port):
        dc_client = DatacenterClient("", dc_ip, dc_port)
        Globals.add_dc_client(dc_client)
        Tables.TABLE_DC_INFO[(dc_ip, dc_port)] = True

    @staticmethod
    def un_register_dc(dc_ip, dc_port):
        Tables.TABLE_DC_INFO[(dc_ip, dc_port)] = False

    @staticmethod
    def is_dc_available(dc_ip, dc_port):
        return (dc_ip, dc_port) in Tables.TABLE_DC_INFO and Tables.TABLE_DC_INFO[(dc_ip, dc_port)]

    @staticmethod
    def get_all_available_dc():
        lst_dc = []
        for ip, port in Tables.TABLE_DC_INFO.keys():
            if Tables.TABLE_DC_INFO[(ip, port)]:
                lst_dc.append((ip, port))
        return lst_dc

    @staticmethod
    def get_random_available_dc(count):
        available_dcs = Tables.get_all_available_dc()
        random_list = get_random_numbers(len(available_dcs), min(count, len(available_dcs)))
        random_dcs = []
        print(len(available_dcs), count, min(count, len(available_dcs)))
        for x in random_list:
            random_dcs.append(available_dcs[x])
        return random_dcs

    @staticmethod
    def add_dc(data_center):
        ip = data_center[0]
        port = data_center[1]
        Tables.TABLE_DC_INFO[(ip, port)] = True

    @staticmethod
    def remove_dc(data_center):
        ip = data_center[0]
        port = data_center[1]
        Tables.TABLE_DC_INFO[(ip, port)] = False

    @staticmethod
    def is_file_exists(file_name):
        if file_name in Tables.TABLE_FILE_INFO.keys():
            return True
        return False

    @staticmethod
    def insert_file_chunk_info_to_file_log(file_name, chunk_id, lst_dc, log_operation):
        for dc in lst_dc:
            log = raft_proto.TableLog()
            log.fileName = file_name
            log.chunkId = chunk_id
            log.ip = dc[0]
            log.port = dc[1]
            log.log_index = Globals.get_next_log_index()
            log.operation = log_operation
            Tables.add_file_log(log)

    @staticmethod
    def add_file_log(table_log):
        Tables.FILE_LOGS.append(table_log)
        Tables.create_default_dictionary_for_file_info_table(table_log.fileName, table_log.chunkId)
        # Possible Values: raft.UploadRequested, raft.Uploaded, raft.UploadFailed, raft.Deleted
        Tables.TABLE_FILE_INFO[table_log.fileName][table_log.chunkId][
            (table_log.ip, table_log.port)] = table_log.operation

    # set_file_log traverse through the file logs and update the FILE_INFO_TABLE
    # used when we get all file_logs with heartbeat request from leader on client(follower) side
    @staticmethod
    def set_file_log(table_logs):
        Tables.FILE_LOGS = []
        for tl in table_logs:
            Tables.add_file_log(tl)
            log_info("LOG Arrived: ")

    @staticmethod
    def create_default_dictionary_for_file_info_table(file_name, chunk_id):
        if file_name not in Tables.TABLE_FILE_INFO:
            Tables.TABLE_FILE_INFO[file_name] = {}

        if chunk_id not in Tables.TABLE_FILE_INFO[file_name]:
            Tables.TABLE_FILE_INFO[file_name][chunk_id] = {}

    @staticmethod
    def get_all_available_file_list():
        file_list = []
        for file_name in Tables.TABLE_FILE_INFO.keys():
            total_chunks = len(Tables.TABLE_FILE_INFO[file_name].keys())
            uploaded_chunks = 0
            for chunk_id in Tables.TABLE_FILE_INFO[file_name].keys():
                for dc in Tables.TABLE_FILE_INFO[file_name][chunk_id].keys():
                    # TODO: Add below condition before returning file list, after we mark file/chunk status to uploaded
                    # if Tables.TABLE_FILE_INFO[file_name][chunk_id][dc] == raft.Uploaded:
                    uploaded_chunks += 1
                    break
            if total_chunks == uploaded_chunks:
                file_list.append(file_name)
        return file_list

    @staticmethod
    def mark_all_file_chunks_in_dc_available_unavailable(dc_ip, dc_port, upload_state):
        for file_name in Tables.TABLE_FILE_INFO.keys():
            for chunk_id in Tables.TABLE_FILE_INFO[file_name].keys():
                for ip, port in Tables.TABLE_FILE_INFO[file_name][chunk_id]:
                    if ip == dc_ip and port == dc_port and Tables.TABLE_FILE_INFO[file_name][chunk_id][(ip, port)] == raft_proto.Uploaded:
                        Tables.TABLE_FILE_INFO[file_name][chunk_id][(ip, port)] = upload_state

    @staticmethod
    def get_file_chunks_to_be_replicated_with_dc_info():
        replication_list = []
        for file_name in Tables.TABLE_FILE_INFO.keys():
            for chunk_id in Tables.TABLE_FILE_INFO[file_name].keys():
                total_replication = 0
                not_replicated_dc = []
                chunk_already_available_dc = []
                for ip, port in Tables.TABLE_FILE_INFO[file_name][chunk_id]:
                    if Tables.TABLE_FILE_INFO[file_name][chunk_id][(ip, port)] == raft_proto.Uploaded:
                        total_replication += 1
                        chunk_already_available_dc.append((ip, port))
                    else:
                        not_replicated_dc.append((ip, port))

                if total_replication > 0 and total_replication < Globals.REPLICATION_FACTOR:
                    lst_dc = Tables.get_all_available_dc()
                    i = 0
                    while total_replication < Globals.REPLICATION_FACTOR and i < len(lst_dc):
                        if lst_dc[i] not in chunk_already_available_dc:
                            random_id = get_random_numbers(len(chunk_already_available_dc), 1)[0]
                            replication_list.append((file_name, chunk_id, lst_dc[i], chunk_already_available_dc[random_id]))
                            Tables.TABLE_FILE_INFO[file_name][chunk_id][lst_dc[i]] = raft_proto.UploadRequested
                            total_replication += 1
                        i += 1

        return replication_list











class DCGlobals:
    LST_REPLICATION_IN_PROGRESS = {}
    DC_HEARTBEAT_TIMEOUT = 2
    DC_REPLICATION_TIMEOUT = 10

    @staticmethod
    def replication_process_pending(dc_client):
        DCGlobals.LST_REPLICATION_IN_PROGRESS[
            (dc_client.server_address, dc_client.server_port)] = raft_proto.ReplicationPending

    @staticmethod
    def replication_process_requested(dc_client):
        DCGlobals.LST_REPLICATION_IN_PROGRESS[
            (dc_client.server_address, dc_client.server_port)] = raft_proto.ReplicationRequested

    @staticmethod
    def replication_process_started(dc_client):
        DCGlobals.LST_REPLICATION_IN_PROGRESS[
            (dc_client.server_address, dc_client.server_port)] = raft_proto.ReplicationStarted

    @staticmethod
    def replication_process_completed(dc_client):
        DCGlobals.LST_REPLICATION_IN_PROGRESS[
            (dc_client.server_address, dc_client.server_port)] = raft_proto.ReplicationCompleted


def _dc_heartbeat_timeout():
    if Globals.NODE_STATE == NodeState.LEADER:
        _send_dc_heartbeat()
    dc_heartbeat_timer.reset()


def _send_dc_heartbeat():
    empty = raft_proto.Empty()
    for dc_client in Globals.LST_DC_CLIENTS:
        dc_client._SendDataCenterHeartbeat(empty)


def _mark_dc_failed(dc_client):
    Tables.mark_all_file_chunks_in_dc_available_unavailable(dc_client.server_address, dc_client.server_port,
                                                            raft_proto.TemporaryUnavailable)
    Tables.un_register_dc(dc_client.server_address, dc_client.server_port)
    # DCGlobals.replication_process_pending(dc_client)
    log_info("STARTING DC LOG REPLICATION...", dc_client.server_port)


def _mark_dc_available(dc_client):
    if not Tables.is_dc_available(dc_client.server_address, dc_client.server_port):
        Tables.register_dc(dc_client.server_address, dc_client.server_port)
        Tables.mark_all_file_chunks_in_dc_available_unavailable(dc_client.server_address, dc_client.server_port,
                                                                raft_proto.Uploaded)


def _process_datacenter_heartbeat(dc_client, call_future):
    log_info("_process_datacenter_heartbeat:", dc_client.server_port)
    with ThreadPoolExecutorStackTraced(max_workers=10) as executor:
        try:
            call_future.result()
            dc_client.heartbeat_fail_count = 0
            _mark_dc_available(dc_client)
        except:
            dc_client.heartbeat_fail_count += 1
            log_info("DATACENTER Exception Error !!", dc_client.server_port, "COUNT:", dc_client.heartbeat_fail_count)
            if dc_client.heartbeat_fail_count > Globals.MAX_ALLOWED_FAILED_HEARTBEAT_COUNT_BEFORE_REPLICATION:
                _mark_dc_failed(dc_client)


class DatacenterClient:
    def __init__(self, username, server_address, server_port):
        self.username = username
        self.server_address = server_address
        self.server_port = server_port

        self.heartbeat_fail_count = 0

        # create a gRPC channel + stub
        channel = grpc.insecure_channel(server_address + ':' + str(server_port))
        self.raft_stub = raft_proto_rpc.RaftServiceStub(channel)
        self.file_transfer_stub = file_transfer_proto_rpc.DataTransferServiceStub(channel)

    def _SendDataCenterHeartbeat(self, Empty):
        try:
            log_info("Sending heartbeat to:", self.server_port)
            call_future = self.raft_stub.DataCenterHeartbeat.future(Empty, timeout=DCGlobals.DC_HEARTBEAT_TIMEOUT * 0.9)
            call_future.add_done_callback(functools.partial(_process_datacenter_heartbeat, self))
        except:
            log_info("Exeption: _SendDataCenterHeartbeat")


dc_heartbeat_timer = TimerUtil(_dc_heartbeat_timeout, DCGlobals.DC_HEARTBEAT_TIMEOUT)
