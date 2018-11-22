import random
from connections.connections import raft_connections as raft_connections


def get_random_numbers(upper_limit, random_count):
    random_numbers = []
    while len(random_numbers) < random_count:
        number = random.randint(0, upper_limit - 1)
        if number not in random_numbers:
            random_numbers.append(number)
    return random_numbers


def get_raft_node():
    available_raft_nodes = []
    for key in raft_connections.keys():
        available_raft_nodes.append((raft_connections[key]))

    random_raft_index = random.randint(0, len(available_raft_nodes) - 1)

    return available_raft_nodes[random_raft_index]["own"]


def get_rand_hashing_node(lst_nodes, file_name, chunk_id):
    lst_hash = []
    for node in lst_nodes:
        lst_hash.append(hash(node[0] + node[1] + file_name + str(chunk_id)))
    index = lst_hash.index(sorted(lst_hash)[0])
    return lst_nodes[index]


def get_rand_hashing_node_from_node_info_object(lst_nodes, file_name, chunk_id):
    lst_hash = []
    for node in lst_nodes:
        lst_hash.append(hash(node.ip + node.port + file_name + str(chunk_id)))
    index = lst_hash.index(sorted(lst_hash)[0])
    return lst_nodes[index]
