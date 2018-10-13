import threading
from tkinter import *
from tkinter import simpledialog
import time
import sys
import grpc

import chat_pb2 as chat
import chat_pb2_grpc as rpc

class Client:

    def __init__(self, u: str, window, server_address, server_port):
        # the frame to put ui components on
        self.window = window
        self.username = u

        # create a gRPC channel + stub
        channel = grpc.insecure_channel(server_address + ':' + str(server_port))
        self.conn = rpc.DataTransferServiceStub(channel)
        # self._ping()
        # create new listening thread for when new message streams come in
        threading.Thread(target=self._ping, daemon=True).start()
        self.__setup_ui()
        self.window.mainloop()


    def _ping(self):
        user = chat.User()
        user.name = self.username

        while True:
            try:
                for message in self.conn.Ping(user):
                    print("R[{}] {} {} {} {} {} {}".format(message.id, message.type, message.data.decode(), message.destination,
                                                        message.origin, message.timestamp, message.hops))
                    self.chat_list.insert(END, "[{}] {}\n".format(message.origin, message.data.decode()))
            except grpc.RpcError as e:
                print("Fail to connect ...")
                time.sleep(3)



    def _send_message(self, msg, destination):
        message = chat.Message()
        message.id = 1
        message.type = 1
        message.data = str.encode(msg)
        message.destination = destination
        message.origin = self.username
        message.timestamp = int(time.time())
        message.hops = 0
        self.conn.Send(message)

    def _send(self, event=None):
        message = self.entry_message.get()
        if message is not '':
            self._send_message(message, "anuj")


    def __setup_ui(self):
        self.chat_list = Text()
        self.chat_list.pack(side=TOP)
        self.lbl_username = Label(self.window, text=self.username)
        self.lbl_username.pack(side=LEFT)
        self.entry_message = Entry(self.window, bd=5)
        self.entry_message.bind('<Return>', self._send)
        self.entry_message.focus()
        self.entry_message.pack(side=BOTTOM)

def main(argv):
    root = Tk()
    frame = Frame(root, width=300, height=300)
    frame.pack()
    root.withdraw()
    username = None
    while username is None:
        username = simpledialog.askstring("Username", "What's your username?", parent=root)
    root.deiconify()
    server_address = argv[1]
    server_port = argv[2]

    c = Client(username, frame, server_address, server_port)

if __name__ == '__main__':
    main(sys.argv[:])