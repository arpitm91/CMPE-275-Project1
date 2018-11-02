import os
import math

SEQ_SIZE = 1024 * 1024  # 1MB


def get_max_file_seqs(filename):
    return math.ceil(os.path.getsize(filename) / SEQ_SIZE)


def get_file_seqs(filename):
    with open(filename, 'rb') as f:
        while True:
            piece = f.read(SEQ_SIZE)
            if not piece:
                break
            yield piece


def write_file_chunks(message):
    file_name = message.origin + "_" + str(message.id)
    with open(file_name, "ab") as myfile:
        myfile.write(message.data)
