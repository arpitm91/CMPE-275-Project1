# raft ports : 10xxx
# proxy ports : 12xxx
# data_center_ports = 11xxxx

arpit_ip = "10.0.10.1"
anuj_ip = "10.0.10.2"
aartee_ip = "10.0.10.3"

raft_port_0 = "10000"
raft_port_1 = "10001"

dc_port_0 = "11000"
dc_port_1 = "11001"

proxy_port_0 = "12000"

raft_connections = {
    "raft_arpit_0": {
        "own": {
            "ip": arpit_ip,
            "port": raft_port_0
        }
    },
    "raft_anuj_0": {
        "own": {
            "ip": anuj_ip,
            "port": raft_port_0
        }
    },
    "raft_aartee_0": {
        "own": {
            "ip": aartee_ip,
            "port": raft_port_0
        }
    },
    "raft_anuj_1": {
        "own": {
            "ip": anuj_ip,
            "port": raft_port_1
        }
    },
    "raft_aartee_1": {
        "own": {
            "ip": aartee_ip,
            "port": raft_port_1
        }
    }
}

other_raft_nodes = [
    {
        "ip": "localhost",
        "port": "13010"
    }
]

proxy = {
    "proxy_arpit_0": {
        "ip": arpit_ip,
        "port": proxy_port_0
    },
    "proxy_anuj_0": {
        "ip": anuj_ip,
        "port": proxy_port_0
    },
    "proxy_aartee_0": {
        "ip": aartee_ip,
        "port": proxy_port_0
    }
}

data_center = {
    "dc_arpit_0": {
        "ip": arpit_ip,
        "port": dc_port_0,
        "folder": "/Users/arpit/Desktop/DataCenter/0"
    },
    "dc_anuj_0": {
        "ip": anuj_ip,
        "port": dc_port_0,
        "folder": "/Users/anujchaudhari/Desktop/CMPE275/DataCenter/0"
    },
    "dc_aartee_0": {
        "ip": aartee_ip,
        "port": dc_port_0,
        "folder": "/Users/aarteekasliwal/Desktop/DataCenter/0"
    },
    "dc_arpit_1": {
        "ip": arpit_ip,
        "port": dc_port_1,
        "folder": "/Users/arpit/Desktop/DataCenter/1"
    },
    "dc_anuj_1": {
        "ip": anuj_ip,
        "port": dc_port_1,
        "folder": "/Users/anujchaudhari/Desktop/CMPE275/DataCenter/1"
    },
    "dc_aartee_1": {
        "ip": aartee_ip,
        "port": dc_port_1,
        "folder": "/Users/aarteekasliwal/Desktop/DataCenter/1"
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

