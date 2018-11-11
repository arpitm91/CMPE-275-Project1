import sys
import os
from collections import defaultdict

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "protos"))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "utils"))

from input_output_util import log_info
from common_utils import get_random_numbers
from globals import Globals

import raft_pb2 as raft


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

    # Key: (ip1, port1), Value: True/False (DC Available or Not)
    TABLE_PROXY_INFO = {}

    @staticmethod
    def init_proxies(lst_proxies):
        for ip, port in lst_proxies:
            Tables.TABLE_PROXY_INFO[(ip, port)] = True
            # TODO: Set False by default

    @staticmethod
    def register_dc(proxy_ip, proxy_port):
        Tables.TABLE_PROXY_INFO[(proxy_ip, proxy_port)] = True

    @staticmethod
    def un_register_dc(proxy_ip, proxy_port):
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
            Tables.TABLE_DC_INFO[(ip, port)] = True
            # TODO: Set False by default

    @staticmethod
    def register_dc(dc_ip, dc_port):
        Tables.TABLE_DC_INFO[(dc_ip, dc_port)] = True

    @staticmethod
    def un_register_dc(dc_ip, dc_port):
        Tables.TABLE_DC_INFO[(dc_ip, dc_port)] = False

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
            log = raft.TableLog()
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
