import os
import math
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "utils"))

from constants import SEQUENCE_SIZE
from constants import CHUNK_SIZE


def get_max_file_seqs(filename):
    return math.ceil(get_file_size(filename) / SEQUENCE_SIZE)


def get_max_file_seqs_per_chunk(filename, chunk_num):
    return math.ceil(get_file_size(filename) / (SEQUENCE_SIZE * get_max_file_chunks(filename)))


def get_max_file_chunks(filename):
    return math.ceil(get_file_size(filename) / CHUNK_SIZE)


def get_file_size(filename):
    return os.path.getsize(filename)


def get_file_seqs(filename):
    with open(filename, 'rb') as f:
        while True:
            piece = f.read(SEQUENCE_SIZE)
            if not piece:
                break
            yield piece


def get_file_seqs_per_chunk(filename, chunk_num):
    with open(filename, 'rb') as f:
        # seek file pointer to start position for chunk before reading file
        f.seek(chunk_num * CHUNK_SIZE)
        while True:
            piece = f.read(SEQUENCE_SIZE)
            if not piece:
                break
            yield piece


def write_file_chunks(message):
    os.mkdir(message.fileName)
    file_name = message.fileName + "/" + str(message.chunkId)
    with open(file_name, "ab") as myfile:
        myfile.write(message.data)
