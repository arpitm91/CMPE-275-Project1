# raft ports : 10xxx
# proxy ports : 12xxx
# data_center_ports = 11xxx

arpit_ip = "10.0.10.1"
anuj_ip = "10.0.10.2"
aartee_ip = "10.0.10.3"

raft_port_0 = "10000"
raft_port_1 = "10001"
raft_port_2 = "10002"

dc_port_0 = "11000"
dc_port_1 = "11001"

proxy_port_0 = "12000"

raft_connections = {
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
    },
    "raft_anuj_2": {
        "own": {
            "ip": anuj_ip,
            "port": raft_port_2
        }
    },
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
