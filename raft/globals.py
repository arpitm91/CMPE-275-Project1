from enum import Enum
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor


class NodeState(Enum):
    CANDIDATE = 0
    FOLLOWER = 1
    LEADER = 2


class Globals:
    LST_RAFT_CLIENTS = []

    LST_DC_CLIENTS = []

    LST_PROXY_CLIENTS = []

    REPLICATION_FACTOR = 3
    MAX_ALLOWED_FAILED_HEARTBEAT_COUNT_BEFORE_REPLICATION = 10

    NODE_STATE = NodeState.FOLLOWER
    CURRENT_CYCLE = 0
    HAS_CURRENT_VOTED = False
    MY_PORT = ""
    MY_IP = ""
    NUMBER_OF_VOTES = 0
    LEADER_PORT = ""
    LEADER_IP = ""

    RAFT_HEARTBEAT_TIMEOUT = 0.2
    PROXY_HEARTBEAT_TIMEOUT = 0.2
    DC_HEARTBEAT_TIMEOUT = 0.2
    DC_REPLICATION_TIMEOUT = 10

    LAST_SENT_TABLE_LOG = 0

    CURRENT_LOG_INDEX = 0

    RAFT_HEARTBEAT_ACK_DICT = {}
    RAFT_HEARTBEAT_COUNTER = 1

    @staticmethod
    def get_next_log_index():
        Globals.CURRENT_LOG_INDEX += 1
        return Globals.CURRENT_LOG_INDEX

    @staticmethod
    def add_dc_client(dc_client):
        is_exists = False
        for client in Globals.LST_DC_CLIENTS:
            if client.server_address == dc_client.server_address and client.server_port == dc_client.server_port:
                is_exists = True
                break
        if not is_exists:
            Globals.LST_DC_CLIENTS.append(dc_client)

    @staticmethod
    def add_proxy_client(proxy_client):
        is_exists = False
        for client in Globals.LST_PROXY_CLIENTS:
            if client.server_address == proxy_client.server_address and client.server_port == proxy_client.server_port:
                is_exists = True
                break
        if not is_exists:
            Globals.LST_PROXY_CLIENTS.append(proxy_client)


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
