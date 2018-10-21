# Python gRPC Chat
Chat application created with gRPC for ring sample.

## Running ring node

`python3 ring_node.py <node_port> <server_ip> <server_port> <username>`

### Example
`python3 ring_node.py 11000 localhost 11001 aartee`

`python3 ring_node.py 11001 localhost 11002 anuj`

`python3 ring_node.py 11002 localhost 11000 arpit`

## Message Format

Enter your input > `<msg_type> <destination_username> <message>`
