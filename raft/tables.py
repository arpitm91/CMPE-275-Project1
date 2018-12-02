import sys
import os
from collections import defaultdict
import pprint
import grpc
import functools

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
from utils.input_output_util import log_info
from utils.common_utils import get_rand_hashing_node


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
            proxy_client = ProxyClient("", ip, port)
            Globals.add_proxy_client(proxy_client)
            Tables.TABLE_PROXY_INFO[(ip, port)] = True
            # TODO: Set False by default

    @staticmethod
    def register_proxy(proxy_ip, proxy_port):
        log = raft_proto.TableLog()
        log.ip = proxy_ip
        log.port = proxy_port
        log.log_index = Globals.get_next_log_index()
        log.operation = raft_proto.Available
        log.logType = raft_proto.ProxyLog
        Tables.add_proxy_log(log)

    @staticmethod
    def un_register_proxy(proxy_ip, proxy_port):
        log = raft_proto.TableLog()
        log.ip = proxy_ip
        log.port = proxy_port
        log.log_index = Globals.get_next_log_index()
        log.operation = raft_proto.Unavailable
        log.logType = raft_proto.ProxyLog
        Tables.add_proxy_log(log)

    @staticmethod
    def get_all_available_proxies():
        lst_proxies = set()
        for ip, port in Tables.TABLE_PROXY_INFO.keys():
            if Tables.TABLE_PROXY_INFO[(ip, port)]:
                lst_proxies.add((ip, port))
        return lst_proxies

    @staticmethod
    def is_proxy_available(proxy_ip, proxy_port):
        return (proxy_ip, proxy_port) in Tables.TABLE_DC_INFO and Tables.TABLE_DC_INFO[(proxy_ip, proxy_port)]

    @staticmethod
    def init_dc(lst_data_centers):
        for ip, port in lst_data_centers:
            dc_client = DatacenterClient("", ip, port)
            Globals.add_dc_client(dc_client)

            Tables.TABLE_DC_INFO[(ip, port)] = True
            # TODO: Set False by default

    @staticmethod
    def register_dc(dc_ip, dc_port):
        log = raft_proto.TableLog()
        log.ip = dc_ip
        log.port = dc_port
        log.log_index = Globals.get_next_log_index()
        log.operation = raft_proto.Available
        log.logType = raft_proto.DatacenterLog
        Tables.add_dc_log(log)

    @staticmethod
    def un_register_dc(dc_ip, dc_port):
        log = raft_proto.TableLog()
        log.ip = dc_ip
        log.port = dc_port
        log.log_index = Globals.get_next_log_index()
        log.operation = raft_proto.Unavailable
        log.logType = raft_proto.DatacenterLog
        Tables.add_dc_log(log)

    @staticmethod
    def is_dc_available(dc_ip, dc_port):
        return (dc_ip, dc_port) in Tables.TABLE_DC_INFO and Tables.TABLE_DC_INFO[(dc_ip, dc_port)]

    @staticmethod
    def get_all_available_dc():
        lst_dc = []
        for ip, port in sorted(Tables.TABLE_DC_INFO.keys()):
            if Tables.TABLE_DC_INFO[(ip, port)]:
                lst_dc.append((ip, port))
        return lst_dc

    @staticmethod
    def get_random_available_dc(count):
        available_dcs = Tables.get_all_available_dc()
        random_list = get_random_numbers(len(available_dcs), min(count, len(available_dcs)))
        random_dcs = []
        log_info(len(available_dcs), count, min(count, len(available_dcs)))
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
            log.logType = raft_proto.FileLog
            Tables.add_file_log(log)

    @staticmethod
    def add_dc_log(dc_log):
        Tables.FILE_LOGS.append(dc_log)
        dc_client = DatacenterClient("", dc_log.ip, dc_log.port)
        Globals.add_dc_client(dc_client)
        Tables.TABLE_DC_INFO[(dc_log.ip, dc_log.port)] = True if dc_log.operation == raft_proto.Available else False

    @staticmethod
    def add_proxy_log(proxy_log):
        Tables.FILE_LOGS.append(proxy_log)
        proxy_client = ProxyClient("", proxy_log.ip, proxy_log.port)
        Globals.add_proxy_client(proxy_client)
        Tables.TABLE_PROXY_INFO[
            (proxy_log.ip, proxy_log.port)] = True if proxy_log.operation == raft_proto.Available else False

    @staticmethod
    def add_file_log(table_log):
        Tables.FILE_LOGS.append(table_log)
        Tables.create_default_dictionary_for_file_info_table(table_log.fileName, table_log.chunkId)
        # Possible Value raft.UploadRequested, raft.Uploaded, raft.UploadFailed, raft.Deleted, raft.TemporaryUnavailable
        Tables.TABLE_FILE_INFO[table_log.fileName][table_log.chunkId][
            (table_log.ip, table_log.port)] = table_log.operation

    # set_file_log traverse through the table logs and update the FILE_INFO_TABLE, TABLE_DC_INFO, TABLE_PROXY_INFO
    # used when we get all logs with heartbeat request from leader on client(follower) side
    @staticmethod
    def set_table_log(table_logs):
        Tables.FILE_LOGS = []
        for tl in table_logs:
            Globals.CURRENT_LOG_INDEX = tl.log_index
            if tl.logType == raft_proto.FileLog:
                Tables.add_file_log(tl)
            elif tl.logType == raft_proto.DatacenterLog:
                Tables.add_dc_log(tl)
            elif tl.logType == raft_proto.ProxyLog:
                Tables.add_proxy_log(tl)

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
                    if Tables.TABLE_FILE_INFO[file_name][chunk_id][dc] == raft_proto.Uploaded:
                        uploaded_chunks += 1
                        break
            if total_chunks == uploaded_chunks:
                file_list.append(file_name)
        return file_list

    @staticmethod
    def mark_all_file_chunks_in_dc_unavailable(dc_ip, dc_port):
        for file_name in Tables.TABLE_FILE_INFO.keys():
            for chunk_id in Tables.TABLE_FILE_INFO[file_name].keys():
                for ip, port in Tables.TABLE_FILE_INFO[file_name][chunk_id]:
                    if ip == dc_ip and port == dc_port:
                        log = raft_proto.TableLog()
                        log.fileName = file_name
                        log.chunkId = chunk_id
                        log.ip = ip
                        log.port = port
                        log.log_index = Globals.get_next_log_index()
                        upload_status = Tables.TABLE_FILE_INFO[file_name][chunk_id][(ip, port)]

                        if upload_status == raft_proto.Uploaded:
                            log.operation = raft_proto.TemporaryUnavailable
                            Tables.add_file_log(log)
                        elif upload_status == raft_proto.UploadRequested:
                            log.operation = raft_proto.UploadFaied
                            Tables.add_file_log(log)

    @staticmethod
    def mark_all_file_chunks_in_dc_available(dc_ip, dc_port):
        for file_name in Tables.TABLE_FILE_INFO.keys():
            for chunk_id in Tables.TABLE_FILE_INFO[file_name].keys():
                for ip, port in Tables.TABLE_FILE_INFO[file_name][chunk_id]:
                    if ip == dc_ip and port == dc_port:
                        log = raft_proto.TableLog()
                        log.fileName = file_name
                        log.chunkId = chunk_id
                        log.ip = ip
                        log.port = port
                        log.log_index = Globals.get_next_log_index()
                        upload_status = Tables.TABLE_FILE_INFO[file_name][chunk_id][(ip, port)]

                        if upload_status == raft_proto.TemporaryUnavailable:
                            log.operation = raft_proto.Uploaded
                            Tables.add_file_log(log)

    @staticmethod
    def get_file_chunks_to_be_replicated_with_dc_info():
        replication_list = []
        for file_name in Tables.TABLE_FILE_INFO.keys():
            for chunk_id in Tables.TABLE_FILE_INFO[file_name].keys():
                total_replication = 0
                requested_replication = 0
                requested_replication_dc = []
                chunk_already_available_dc = []
                for ip, port in Tables.TABLE_FILE_INFO[file_name][chunk_id]:
                    if Tables.TABLE_FILE_INFO[file_name][chunk_id][(ip, port)] == raft_proto.Uploaded:
                        total_replication += 1
                        chunk_already_available_dc.append((ip, port))
                    elif Tables.TABLE_FILE_INFO[file_name][chunk_id][(ip, port)] == raft_proto.UploadRequested:
                        requested_replication += 1
                        requested_replication_dc.append((ip, port))

                if total_replication > 0 and (total_replication + requested_replication) < Globals.REPLICATION_FACTOR:

                    non_replicated_dc = list(set(Tables.get_all_available_dc()) - set(chunk_already_available_dc) - set(
                        requested_replication_dc))

                    if len(non_replicated_dc) == 0:
                        continue

                    selected_dc_for_replication = get_rand_hashing_node(non_replicated_dc, file_name, chunk_id)

                    random_id = get_random_numbers(len(chunk_already_available_dc), 1)[0]
                    replication_list.append(
                        (file_name, chunk_id, selected_dc_for_replication, chunk_already_available_dc[random_id]))

        return replication_list


def _proxy_heartbeat_timeout():
    if Globals.NODE_STATE == NodeState.LEADER:
        _send_proxy_heartbeat()
    proxy_heartbeat_timer.reset()


def _send_proxy_heartbeat():
    table = raft_proto.Table()
    table.tableLog.extend(Tables.FILE_LOGS)
    for proxy_client in Globals.LST_PROXY_CLIENTS:
        proxy_client._SendProxyHeartbeat(table)


def _process_proxy_heartbeat(proxy_client, call_future):
    with ThreadPoolExecutorStackTraced(max_workers=10) as executor:
        try:
            call_future.result()
            proxy_client.heartbeat_fail_count = 0
            _mark_proxy_available(proxy_client)
        except:
            proxy_client.heartbeat_fail_count += 1
            log_info("Proxy Exception Error !!", proxy_client.server_port, "COUNT:", proxy_client.heartbeat_fail_count)
            if proxy_client.heartbeat_fail_count > Globals.MAX_ALLOWED_FAILED_HEARTBEAT_COUNT_BEFORE_REPLICATION:
                _mark_proxy_failed(proxy_client)


def _mark_proxy_failed(dc_client):
    Tables.un_register_proxy(dc_client.server_address, dc_client.server_port)


def _mark_proxy_available(proxy_client):
    if not Tables.is_proxy_available(proxy_client.server_address, proxy_client.server_port):
        Tables.register_proxy(proxy_client.server_address, proxy_client.server_port)


def _dc_heartbeat_timeout():
    if Globals.NODE_STATE == NodeState.LEADER:
        _send_dc_heartbeat()
    dc_heartbeat_timer.reset()


def _send_dc_heartbeat():
    empty = raft_proto.Empty()
    for dc_client in Globals.LST_DC_CLIENTS:
        dc_client._SendDataCenterHeartbeat(empty)


def _mark_dc_failed(dc_client):
    Tables.mark_all_file_chunks_in_dc_unavailable(dc_client.server_address, dc_client.server_port)
    Tables.un_register_dc(dc_client.server_address, dc_client.server_port)


def _mark_dc_available(dc_client):
    if not Tables.is_dc_available(dc_client.server_address, dc_client.server_port):
        Tables.register_dc(dc_client.server_address, dc_client.server_port)
        Tables.mark_all_file_chunks_in_dc_available(dc_client.server_address, dc_client.server_port)


def Check_and_send_replication_request():
    replication_list = Tables.get_file_chunks_to_be_replicated_with_dc_info()
    pprint.pprint("$$$$$$$$$$$$$$$ REPLICATION LIST ########################")
    pprint.pprint(replication_list)

    for replication_info in replication_list:
        file_name = replication_info[0]
        chunk_id = replication_info[1]
        to_dc = replication_info[2]
        from_dc = replication_info[3]
        for dc_client in Globals.LST_DC_CLIENTS:
            if dc_client.server_address == to_dc[0] and dc_client.server_port == to_dc[1]:
                log_info("REQUESTING REPLICATION FOR FILE:", file_name, "CHUNK:", chunk_id, "TO:", to_dc, "FROM:",
                         from_dc)

                replication_info_request = raft_proto.ReplicationInfo()
                replication_info_request.fileName = file_name
                replication_info_request.chunkId = chunk_id
                replication_info_request.fromDatacenter.ip = from_dc[0]
                replication_info_request.fromDatacenter.port = from_dc[1]
                dc_client._ReplicationInitiate(replication_info_request)


def _process_datacenter_heartbeat(dc_client, call_future):
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


def _process_datacenter_replication_initiate(dc_client, dc_ip, dc_port, ReplicationInfo, call_future):
    with ThreadPoolExecutorStackTraced(max_workers=10) as executor:
        try:
            call_future.result()
            file_name = ReplicationInfo.fileName
            chunk_id = ReplicationInfo.chunkId
            lst_dc = [(dc_ip, dc_port)]
            Tables.insert_file_chunk_info_to_file_log(file_name, chunk_id, lst_dc, raft_proto.UploadRequested)
        except:
            pass


class DatacenterClient:
    def __init__(self, username, server_address, server_port):
        self.username = username
        self.server_address = server_address
        self.server_port = server_port

        self.heartbeat_fail_count = 0

        # create a gRPC channel + stub
        channel = grpc.insecure_channel(server_address + ':' + str(server_port))
        self.data_center_stub = raft_proto_rpc.DataCenterServiceStub(channel)

    def _SendDataCenterHeartbeat(self, Empty):
        try:
            # log_info("Sending heartbeat to:", self.server_port)
            call_future = self.data_center_stub.DataCenterHeartbeat.future(Empty,
                                                                           timeout=Globals.DC_HEARTBEAT_TIMEOUT * 0.9)
            call_future.add_done_callback(functools.partial(_process_datacenter_heartbeat, self))
        except:
            log_info("Exception: _SendDataCenterHeartbeat")

    def _ReplicationInitiate(self, ReplicationInfo):
        try:
            log_info("Sending replication request to:", self.server_address, self.server_port)
            call_future = self.data_center_stub.ReplicationInitiate.future(ReplicationInfo,
                                                                           timeout=Globals.DC_HEARTBEAT_TIMEOUT * 0.9)
            call_future.add_done_callback(
                functools.partial(_process_datacenter_replication_initiate, self, self.server_address, self.server_port,
                                  ReplicationInfo))
        except:
            log_info("Exception: _ReplicationInitiate")


class ProxyClient:
    def __init__(self, username, server_address, server_port):
        self.username = username
        self.server_address = server_address
        self.server_port = server_port

        self.heartbeat_fail_count = 0

        # create a gRPC channel + stub
        channel = grpc.insecure_channel(server_address + ':' + str(server_port))
        self.proxy_stub = raft_proto_rpc.ProxyServiceStub(channel)

    def _SendProxyHeartbeat(self, table):
        try:
            log_info("Sending heartbeat to:", self.server_port)
            call_future = self.proxy_stub.ProxyHeartbeat.future(table, timeout=Globals.PROXY_HEARTBEAT_TIMEOUT * 0.9)
            call_future.add_done_callback(functools.partial(_process_proxy_heartbeat, self))
        except:
            log_info("Exception: _SendProxyHeartbeat")


dc_heartbeat_timer = TimerUtil(_dc_heartbeat_timeout, Globals.DC_HEARTBEAT_TIMEOUT)
proxy_heartbeat_timer = TimerUtil(_proxy_heartbeat_timeout, Globals.PROXY_HEARTBEAT_TIMEOUT)
