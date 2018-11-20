import random
from connections.connections import raft_connections as raft_connections

def get_random_numbers(upper_limit, random_count):
    random_numbers = []
    while len(random_numbers) < random_count:
        number = random.randint(0, upper_limit-1)
        if number not in random_numbers:
            random_numbers.append(number)
    return random_numbers

def get_raft_node():
    available_raft_nodes = []
    for key in raft_connections.keys():
        available_raft_nodes.append((raft_connections[key]))

    random_raft_index = random.randint(0, len(available_raft_nodes) - 1)

    return available_raft_nodes[random_raft_index]["own"]