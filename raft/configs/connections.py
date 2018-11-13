MAX_RAFT_NODES = 5
connections = {
    "arpit_0": {
        "own": {
            "ip": "10.0.10.1",
            "port": "10000"
        },
        "clients": [{
            "ip": "10.0.10.2",
            "port": "10000"
        },
            {
                "ip": "10.0.10.2",
                "port": "10001"
            },
            {
                "ip": "10.0.10.3",
                "port": "10000"
            },
            {
                "ip": "10.0.10.3",
                "port": "10001"
            }
        ]
    },
    "anuj_0": {
        "own": {
            "ip": "10.0.10.2",
            "port": "10000"
        },
        "clients": [{
            "ip": "10.0.10.1",
            "port": "10000"
        },
            {
                "ip": "10.0.10.2",
                "port": "10001"
            },
            {
                "ip": "10.0.10.3",
                "port": "10000"
            },
            {
                "ip": "10.0.10.3",
                "port": "10001"
            }
        ]
    },
    "aartee_0": {
        "own": {
            "ip": "10.0.10.3",
            "port": "10000"
        },
        "clients": [{
            "ip": "10.0.10.1",
            "port": "10000"
        },
            {
                "ip": "10.0.10.2",
                "port": "10000"
            },
            {
                "ip": "10.0.10.2",
                "port": "10001"
            },
            {
                "ip": "10.0.10.3",
                "port": "10001"
            }
        ]
    },
    "anuj_1": {
        "own": {
            "ip": "10.0.10.2",
            "port": "10001"
        },
        "clients": [{
            "ip": "10.0.10.1",
            "port": "10000"
        },
            {
                "ip": "10.0.10.3",
                "port": "10000"
            },
            {
                "ip": "10.0.10.3",
                "port": "10001"
            },
            {
                "ip": "10.0.10.2",
                "port": "10000"
            }
        ]
    },
    "aartee_1": {
        "own": {
            "ip": "10.0.10.3",
            "port": "10001"
        },
        "clients": [{
            "ip": "10.0.10.1",
            "port": "10000"
        },
            {
                "ip": "10.0.10.2",
                "port": "10000"
            },
            {
                "ip": "10.0.10.3",
                "port": "10000"
            },
            {
                "ip": "10.0.10.2",
                "port": "10001"
            }
        ]
    },
    "test_1": {
        "own": {
            "ip": "localhost",
            "port": "10000"
        },
        "clients": [
            {
                "ip": "localhost",
                "port": "10001"
            },
            {
                "ip": "localhost",
                "port": "10002"
            }
        ]
    },
    "test_2": {
        "own": {
            "ip": "localhost",
            "port": "10001"
        },
        "clients": [
            {
                "ip": "localhost",
                "port": "10000"
            },
            {
                "ip": "localhost",
                "port": "10002"
            }
        ]
    },
    "test_3": {
        "own": {
            "ip": "localhost",
            "port": "10002"
        },
        "clients": [
            {
                "ip": "localhost",
                "port": "10000"
            },
            {
                "ip": "localhost",
                "port": "10001"
            }
        ]
    },
    "client": {
        "own": {
            "ip": "10.0.10.2",
            "port": "10003"
        },
        "clients": [{
            "ip": "10.0.10.1",
            "port": "10000"
        },
            {
                "ip": "10.0.10.2",
                "port": "10000"
            },
            {
                "ip": "10.0.10.2",
                "port": "10001"
            },
            {
                "ip": "10.0.10.3",
                "port": "10000"
            },
            {
                "ip": "10.0.10.3",
                "port": "10001"
            }
        ]
    },
    "client_2": {
        "own": {
            "ip": "localhost",
            "port": "10003"
        },
        "clients": [{
            "ip": "localhost",
            "port": "10000"
        },
            {
                "ip": "localhost",
                "port": "10001"
            },
            {
                "ip": "localhost",
                "port": "10002"
            }
        ]
    },
    "raft_1_1": {
        "own": {
            "ip": "localhost",
            "port": "10010"
        },
        "clients": [
            {
                "ip": "localhost",
                "port": "10011"
            }
        ]
    },
    "raft_1_2": {
        "own": {
            "ip": "localhost",
            "port": "10011"
        },
        "clients": [
            {
                "ip": "localhost",
                "port": "10010"
            }
        ]
    },
    "raft_2_1": {
        "own": {
            "ip": "localhost",
            "port": "13010"
        },
        "clients": [
            {
                "ip": "localhost",
                "port": "13011"
            }
        ]
    },
    "raft_2_2": {
        "own": {
            "ip": "localhost",
            "port": "13011"
        },
        "clients": [
            {
                "ip": "localhost",
                "port": "13010"
            }
        ]
    }
}

# data_centers = [("localhost", "12000"), ("localhost", "12001")]
# lst_proxies = [("localhost", "12000")]
data_centers = [("10.0.10.3", "11001"), ("10.0.10.3", "11002"), ("10.0.10.3", "11003"), ("10.0.10.3", "11004")]
lst_proxies = [("10.0.10.3", "11001"), ("10.0.10.3", "11002"), ("10.0.10.3", "11003"), ("10.0.10.3", "11004")]
#
# data_centers = [("localhost", "11000"),("localhost", "11001"),("localhost", "11002")]
# lst_proxies = [("localhost", "12000")]
# lst_proxies = [("localhost", "12000"),("localhost", "12001"),("localhost", "12002")]

other_raft_nodes = [
    {
        "ip": "localhost",
        "port": "13010"
    }
]