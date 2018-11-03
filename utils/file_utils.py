import os
import math
import glob

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
def merge_chunks(file_name_folder):
    pass
#     merged_file_name = "merged_file"
#     with open(merged_file_name, "ab") as merged_file:
#         for chunks in glob.glob(file_name_folder):
#             print("chunk: ", chunks)
#             # for chunks in os.listdir(file_name_folder):
#             with open(chunks, "rb") as chunk_file:
#                 merged_file.write(str.encode(chunk_file.read()))
#         print(chunks)
