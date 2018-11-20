# raft ports : 10xxx
# proxy ports : 12xxx
# data_center_ports = 11xxx

arpit_ip = "localhost"

raft_port_0 = "10000"
raft_port_1 = "10001"
raft_port_2 = "10002"

dc_port_0 = "11000"
dc_port_1 = "11001"

proxy_port_0 = "12000"
proxy_port_1 = "12001"

raft_connections = {
    "raft_arpit_0": {
        "own": {
            "ip": arpit_ip,
            "port": raft_port_0
        }
    },
    "raft_arpit_1": {
        "own": {
            "ip": arpit_ip,
            "port": raft_port_1
        }
    },
    "raft_arpit_2": {
        "own": {
            "ip": arpit_ip,
            "port": raft_port_2
        }
    }
}

other_raft_nodes = [
    {
        "ip": "10.0.40.1",
        "port": "10000"
    },
    {
        "ip": "10.0.40.2",
        "port": "10000"
    },
    {
        "ip": "10.0.40.2",
        "port": "10001"
    },
    {
        "ip": "10.0.40.3",
        "port": "10000"
    },
    {
        "ip": "10.0.40.4",
        "port": "10000"
    },

    {
        "ip": "10.0.30.1",
        "port": "10000"
    },
    {
        "ip": "10.0.30.2",
        "port": "10000"
    },
    {
        "ip": "10.0.30.3",
        "port": "10000"
    },
    {
        "ip": "10.0.30.3",
        "port": "10001"
    },
    {
        "ip": "10.0.30.4",
        "port": "10000"
    }

]

proxy = {
    "proxy_arpit_0": {
        "ip": arpit_ip,
        "port": proxy_port_0
    },
    "proxy_arpit_1": {
        "ip": arpit_ip,
        "port": proxy_port_1
    }
}

data_center = {
    "dc_arpit_0": {
        "ip": arpit_ip,
        "port": dc_port_0,
        "folder": "/Users/arpit/Desktop/DataCenter/0"
    },
    "dc_arpit_1": {
        "ip": arpit_ip,
        "port": dc_port_1,
        "folder": "/Users/arpit/Desktop/DataCenter/1"
    }
}

MAX_RAFT_NODES = len(raft_connections)

for elem in raft_connections.keys():
    client_array = []

    for client in raft_connections.keys():
        if raft_connections[client]["own"] == raft_connections[elem]["own"]:
            continue
        client_array.append(raft_connections[client]["own"])

        raft_connections[elem]["clients"] = client_array
