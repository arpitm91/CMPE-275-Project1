MAX_RAFT_NODES = 3
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
	}		
}