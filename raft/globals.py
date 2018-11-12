from enum import Enum


class NodeState(Enum):
    CANDIDATE = 0
    FOLLOWER = 1
    LEADER = 2


class Globals:
    LST_CLIENTS = []

    REPLICATION_FACTOR = 2

    NODE_STATE = NodeState.FOLLOWER
    CURRENT_CYCLE = 0
    HAS_CURRENT_VOTED = False
    MY_PORT = ""
    MY_IP = ""
    NUMBER_OF_VOTES = 0
    LEADER_PORT = ""
    LEADER_IP = ""

    RAFT_HEARTBEAT_TIMEOUT = 2
    DC_HEARTBEAT_TIMEOUT = 2


    LAST_SENT_TABLE_LOG = 0

    CURRENT_LOG_INDEX = 0

    @staticmethod
    def get_next_log_index():
        Globals.CURRENT_LOG_INDEX += 1
        return Globals.CURRENT_LOG_INDEX
