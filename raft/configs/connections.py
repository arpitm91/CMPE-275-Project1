MAX_RAFT_NODES = 2
connections = {
	"arpit_0": {
		"own": {
			"ip": "10.0.0.1",
			"port": "10000"
		},
		"clients": [{
				"ip": "10.0.0.2",
				"port": "10000"
			},
			{
				"ip": "10.0.0.2",
				"port": "10001"
			},
			{
				"ip": "10.0.0.3",
				"port": "10000"
			},
			{
				"ip": "10.0.0.3",
				"port": "10001"
			}
		]
	},
	"anuj_0": {
		"own": {
			"ip": "10.0.0.2",
			"port": "10000"
		},
		"clients": [{
				"ip": "10.0.0.1",
				"port": "10000"
			},
			{
				"ip": "10.0.0.2",
				"port": "10001"
			},
			{
				"ip": "10.0.0.3",
				"port": "10000"
			},
			{
				"ip": "10.0.0.3",
				"port": "10001"
			}
		]
	},
	"aartee_0": {
		"own": {
			"ip": "10.0.0.3",
			"port": "10000"
		},
		"clients": [{
				"ip": "10.0.0.1",
				"port": "10000"
			},
			{
				"ip": "10.0.0.2",
				"port": "10000"
			},
			{
				"ip": "10.0.0.2",
				"port": "10001"
			},
			{
				"ip": "10.0.0.3",
				"port": "10001"
			}
		]
	},
	"anuj_1": {
		"own": {
			"ip": "10.0.0.2",
			"port": "10001"
		},
		"clients": [{
				"ip": "10.0.0.1",
				"port": "10000"
			},
			{
				"ip": "10.0.0.3",
				"port": "10000"
			},
			{
				"ip": "10.0.0.3",
				"port": "10001"
			},
			{
				"ip": "10.0.0.2",
				"port": "10000"
			}
		]
	},
	"aartee_1": {
		"own": {
			"ip": "10.0.0.3",
			"port": "10001"
		},
		"clients": [{
				"ip": "10.0.0.1",
				"port": "10000"
			},
			{
				"ip": "10.0.0.2",
				"port": "10000"
			},
			{
				"ip": "10.0.0.3",
				"port": "10000"
			},
			{
				"ip": "10.0.0.2",
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
			"ip": "10.0.0.2",
			"port": "10003"
		},
		"clients": [{
				"ip": "10.0.0.1",
				"port": "10000"
			},
			{
				"ip": "10.0.0.2",
				"port": "10000"
			},
			{
				"ip": "10.0.0.2",
				"port": "10001"
			},
			{
				"ip": "10.0.0.3",
				"port": "10000"
			},
			{
				"ip": "10.0.0.3",
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
	"test_client_1": {
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
	"test_client_2": {
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
	}
}


data_centers = [("localhost", "11000"),("localhost", "11001"),("localhost", "11002")]
lst_proxies = [("localhost", "12000")]
#lst_proxies = [("localhost", "12000"),("localhost", "12001"),("localhost", "12002")]