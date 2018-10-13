from concurrent import futures

import grpc
import time
import sys

import chat_pb2 as chat
import chat_pb2_grpc as rpc


class ChatServer(rpc.DataTransferServiceServicer):

    def __init__(self):
        # List with all the chat history
        self.chats = []

    def Ping(self, request: chat.User, context):
        print("[{}] from Ping in server".format(request.name))
        lastindex = 0
        while True:
            # Check if there are any new messages
            while len(self.chats) > lastindex:
                n = self.chats[lastindex]
                print("sending messages ", n.data.decode())
                lastindex += 1
                yield n

    def Send(self, request: chat.Message, context):
        print("[{}] {} {} {} {} {} {}".format(request.id, request.type, request.data.decode(), request.destination, request.origin, request.timestamp, request.hops))
        # Add it to the chat history
        ack = chat.Ack()
        ack.id = request.id
        self.chats.append(request)
        return ack


def main(argv):
    port = argv[1]
    # create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc.add_DataTransferServiceServicer_to_server(ChatServer(), server)

    print('Starting server. Listening...')
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    # Server starts in background (another thread) so keep waiting
    while True:
        time.sleep(64 * 64 * 100)

if __name__ == '__main__':
    main(sys.argv[:])
    
