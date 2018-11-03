import os
import math
import sys
import glob
import shutil

import time


sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "utils"))

from constants import SEQUENCE_SIZE
from constants import CHUNK_SIZE


def get_max_file_seqs(filename):
    return math.ceil(get_file_size(filename) / SEQUENCE_SIZE)


def get_max_file_seqs_per_chunk(filename):
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
        total_seq = CHUNK_SIZE / SEQUENCE_SIZE
        while total_seq >= 0:
            total_seq -= 1
            piece = f.read(SEQUENCE_SIZE)
            if not piece:
                break
            yield piece


def write_file_chunks(message, folder):
    path = os.path.join(folder, message.fileName)
    if not os.path.exists(path):
        os.makedirs(path)
    file_name = os.path.join(folder, message.fileName, str(message.chunkId))
    with open(file_name, "ab") as myfile:
        myfile.write(message.data)

#
def merge_chunks(file_name_folder, folder, maxChunks):
    merged_file_name = os.path.join(folder, "merged_file" + str(math.ceil(time.time())))
    download_folder = os.path.join(folder, file_name_folder)
    with open(merged_file_name, "ab") as merged_file:
        for chunks in range(maxChunks):
            with open(os.path.join(download_folder, str(chunks)), "rb") as chunk_file:
                merged_file.write(chunk_file.read())

    shutil.rmtree(download_folder)
    os.rename(merged_file_name, download_folder)