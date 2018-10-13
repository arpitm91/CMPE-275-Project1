import threading
from tkinter import *
from tkinter import simpledialog
import time

import grpc

import chat_pb2 as chat
import chat_pb2_grpc as rpc

address = 'localhost'
port = 11912

class Client:

    def __init__(self, u: str, window):
        # the frame to put ui components on
        self.window = window
        self.username = u

        # create a gRPC channel + stub
        channel = grpc.insecure_channel(address + ':' + str(port))
        self.conn = rpc.DataTransferServiceStub(channel)
        # self._ping()
        # create new listening thread for when new message streams come in
        threading.Thread(target=self._ping, daemon=True).start()
        self.__setup_ui()
        self.window.mainloop()


    def _ping(self):
        user = chat.User()
        user.name = self.username

        for message in self.conn.Ping(user):
            print("R[{}] {} {} {} {} {} {}".format(message.id, message.type, message.data.decode(), message.destination,
                                                   message.origin, message.timestamp, message.hops))
            self.chat_list.insert(END, "[{}] {}\n".format(message.origin, message.data.decode()))


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


if __name__ == '__main__':
    root = Tk()
    frame = Frame(root, width=300, height=300)
    frame.pack()
    root.withdraw()
    username = None
    while username is None:
        username = simpledialog.askstring("Username", "What's your username?", parent=root)
    root.deiconify()
    c = Client(username, frame)
