import os
import math
import glob
import shutil

import time

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


def write_file_chunks(message, folder):
    try:
        os.mkdir(os.path.join(folder, message.fileName))
    except OSError as e:
        if e.errno != os.errno.EEXIST:
            raise
        pass
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