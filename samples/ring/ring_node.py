import threading
from concurrent import futures

import grpc
import time
import sys

import chat_pb2 as chat
import chat_pb2_grpc as rpc

from utils.input_output_util import get_input
from utils.input_output_util import print_msg
from utils.input_output_util import log_error
from utils.input_output_util import log_info
from utils.input_output_util import print_take_input_msg

chats = []


class Client:
    def __init__(self, username, server_address, server_port):

        self.username = username

        # create a gRPC channel + stub
        channel = grpc.insecure_channel(server_address + ':' + str(server_port))
        self.conn = rpc.DataTransferServiceStub(channel)
        # self._ping()
        # create new listening thread for when new message streams come in
        threading.Thread(target=self._ping, daemon=True).start()

        for msg in get_input():
            self._send_message(msg)

    def _ping(self):
        user = chat.User()
        user.name = self.username

        while True:
            try:
                print_take_input_msg()
                for message in self.conn.Ping(user):
                    if message.destination == self.username:
                        print_msg(message)
                        print_take_input_msg()
                    elif message.origin == self.username:
                        log_info("destination " + message.destination + " not found..")
                    else:
                        log_info(
                            "forwarding message \"" + message.data.decode() + "\" from " + message.origin + " to " + message.destination + "....")
                        time.sleep(1)
                        chats.append(message)

            except grpc.RpcError as e:
                log_error("Fail to connect...")
                time.sleep(1)

    def _send_message(self, msg):
        msg = msg.split()
        if len(msg) <= 1:
            log_error("invalid message format: <destination> <msg>")
            return
        message = chat.Message()
        message.id = 1
        message.type = 1
        message.data = str.encode(" ".join(msg[1:]))
        message.destination = msg[0]
        message.origin = self.username
        message.timestamp = int(time.time())
        message.hops = 0

        chats.append(message)


def start_client(username, server_address, server_port):
    c = Client(username, server_address, server_port)


# server

class ChatServer(rpc.DataTransferServiceServicer):
    def __init__(self):
        pass

    def Ping(self, request: chat.User, context):
        print("[{}] from Ping in server".format(request.name))
        lastindex = 0
        while True:
            # Check if there are any new messages
            while len(chats) > lastindex:
                n = chats[lastindex]
                lastindex += 1

                yield n

    def Send(self, request: chat.Message, context):
        # print_msg(request)

        # Add it to the chat history
        ack = chat.Ack()
        ack.id = request.id
        chats.append(request)
        return ack


def main(argv):
    my_port = argv[1]
    # create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc.add_DataTransferServiceServicer_to_server(ChatServer(), server)

    print('Starting server. Listening...')
    server.add_insecure_port('[::]:' + str(my_port))
    server.start()

    # client
    server_address = argv[2]
    server_port = argv[3]
    username = argv[4]

    threading.Thread(target=start_client, args=(username, server_address, server_port), daemon=True).start()

    # Server starts in background (another thread) so keep waiting
    while True:
        time.sleep(64 * 64 * 100)


if __name__ == '__main__':
    main(sys.argv[:])

