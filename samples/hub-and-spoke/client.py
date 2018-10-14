import threading
from tkinter import *
from tkinter import simpledialog
import time
import sys
import grpc

import chat_pb2 as chat
import chat_pb2_grpc as rpc

from utils.input_output_util import get_input
from utils.input_output_util import print_msg
from utils.input_output_util import log_error
from utils.input_output_util import print_take_input_msg

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
            self._send_message(msg, "XXX")


    def _ping(self):
        user = chat.User()
        user.name = self.username

        while True:
            try:
                for message in self.conn.Ping(user):                    
                    print_msg(message)
                    print_take_input_msg()
                
            except grpc.RpcError as e:
                log_error("Fail to connect...")                
                time.sleep(1)



    def _send_message(self, msg, destination):
        message = chat.Message()
        message.id = 1
        message.type = 1
        message.data = str.encode(msg)
        message.destination = destination
        message.origin = self.username
        message.timestamp = int(time.time())
        message.hops = 0
        
        try:
            self.conn.Send(message)
        except grpc.RpcError as e:
            log_error("Unable to send msg: " + msg)


    def _send(self, event=None):
        message = self.entry_message.get()
        if message is not '':
            self._send_message(message, "anuj")

def start_client(username, server_address, server_port):
    c = Client(username, server_address, server_port)

def main(argv):
  
    server_address = argv[1]
    server_port = argv[2]
    username = argv[3]

    threading.Thread(target=start_client, args=(username, server_address, server_port), daemon=True).start()

    # Server starts in background (another thread) so keep waiting
    while True:
        time.sleep(64 * 64 * 100)


if __name__ == '__main__':
    main(sys.argv[:])