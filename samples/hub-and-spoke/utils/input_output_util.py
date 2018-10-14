import sys
import threading
import time
import queue

WHITE =  '\033[97m'    # User Input color
YELLOW = '\033[93m'    # Log output color
BLUE =   '\033[94m'    # Input prompt color
CYAN =   '\033[96m'    # Input result color
RED  =   '\033[31m'
ERASE_LINE = '\r' + '\033[K'

def add_input(input_queue):
    while True:
        input_queue.put(input())

def get_input():
    input_queue = queue.Queue()

    input_thread = threading.Thread(target=add_input, args=(input_queue,))
    input_thread.daemon = True
    input_thread.start()

    while True:
        if not input_queue.empty():
            yield input_queue.get()          

def print_msg(msg):
        print(ERASE_LINE + CYAN + "[{}] ".format(time.strftime('%X')) + YELLOW + msg.origin + ": " + WHITE + msg.data.decode())
        
def print_take_input_msg():
        print(BLUE + "Enter your input >" + WHITE, end = ' ', flush=True)

def log_error(string):
        print(ERASE_LINE + RED + string + WHITE)

