#!/bin/bash
echo "Generating proto grpc files..."
python3 -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. file_transfer.proto
python3 -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. raft.proto
protoc -I . file_transfer.proto --go_out=plugins=grpc:../go/src/grpc
protoc -I . raft.proto --go_out=plugins=grpc:../go/src/raft
echo "DONE"
