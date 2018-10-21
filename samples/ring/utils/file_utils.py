import os
import math

CHUNK_SIZE = 100  # 1MB


def get_total_file_chunks(filename):
    return math.ceil(os.path.getsize(filename) / CHUNK_SIZE)
    
def get_file_chunks(filename):    
    with open(filename, 'rb') as f:
        while True:        
            piece = f.read(CHUNK_SIZE);
            if not piece:
                break
            yield piece

def write_file_chunks(message):
    file_name = message.origin + "_" + str(message.id)
    with open(file_name, "a") as myfile:
        myfile.write(message.data.decode())