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
from utils.input_output_util import log_forwarding_info
from utils.input_output_util import print_file_info

from utils.file_utils import get_file_chunks
from utils.file_utils import write_file_chunks
from utils.file_utils import get_total_file_chunks

chats = []
file_buffer = []

class Client:
    def __init__(self, username, server_address, server_port):

        self.username = username
        self.msg_id = 0

        # create a gRPC channel + stub
        channel = grpc.insecure_channel(server_address + ':' + str(server_port))
        self.conn = rpc.DataTransferServiceStub(channel)
        # self._ping()
        # create new listening thread for when new message streams come in
        threading.Thread(target=self._ping, daemon=True).start()

        for msg in get_input():
            msg = msg.split()
            if len(msg) <= 2:
                log_error("invalid message format: <destination> <msg>")
                return

            if msg[0] == "text":
                self._send_message(msg[1], msg[2:])
            elif msg[0] == "file":
                self._tranfer_file(msg[1], msg[2])
            else:
                log_error("invalid message type: supported msg type text, file")

    def _next_msg_id(self):
        self.msg_id = self.msg_id + 1
        return self.msg_id

    def _ping(self):
        user = chat.User()
        user.name = self.username

        while True:
            try:
                print_take_input_msg()
                for message in self.conn.Ping(user):
                    if message.destination == self.username:

                        if message.type == chat.File:
                            write_file_chunks(message)
                            print_file_info(message)

                        if message.type == chat.Text:
                            print_msg(message)

                        print_take_input_msg()
                    elif message.origin == self.username:
                        log_info("destination " + message.destination + " not found..")
                    else:
                        log_forwarding_info(message)
                        # log_info(
                        #     "forwarding message \"" + str(message.id) + "\" from " + message.origin + " to " + message.destination + "....")
                        # time.sleep(1)
                        chats.append(message)

            except grpc.RpcError as e:
                log_error("Fail to connect...")
                time.sleep(1)

    def _send_message(self, destination, msg):

        message = chat.Message()
        message.id = self._next_msg_id()
        message.type = chat.Text
        message.data = str.encode(" ".join(msg))
        message.destination = destination
        message.origin = self.username
        message.timestamp = int(time.time())
        message.hops = 0
        message.seqnum = 1
        message.seqmax = 1

        chats.append(message)

    def _tranfer_file(self, destination, filename):

        print("transferring file... " + filename + " to " + destination)

        try:
            msg_id = self._next_msg_id()

            total_chunk = get_total_file_chunks(filename)
            current_chunk = 1

            for file_buffer in get_file_chunks(filename):
                message = chat.Message()
                message.id = msg_id
                message.type = chat.File
                message.data = file_buffer
                message.destination = destination
                message.origin = self.username
                message.timestamp = int(time.time())
                message.hops = 0
                message.seqnum = current_chunk
                message.seqmax = total_chunk
                current_chunk += 1
                
                chats.append(message)

        except FileNotFoundError as e:
            print("File not found:", e)
        

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

