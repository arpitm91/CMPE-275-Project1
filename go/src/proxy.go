package main

import (
	"context"
	commonProto "grpc"
	"log"
	"net"
	ourProto "raft"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"
)

const (
	myIP   = "10.0.10.1"
	myPort = "12000"
	oneDay = 60 * 60 * 24 * time.Second
)

type proxyServer struct{}

func (s *proxyServer) ProxyHeartbeat(ctx context.Context, request *ourProto.Empty) (*ourProto.Empty, error) {
	return &ourProto.Empty{}, nil
}

type dataCenterServer struct{}

func (s *dataCenterServer) RequestFileInfo(ctx context.Context, request *commonProto.FileInfo) (*commonProto.FileLocationInfo, error) {
	return nil, nil
}
func (s *dataCenterServer) GetFileLocation(ctx context.Context, request *commonProto.FileInfo) (*commonProto.FileLocationInfo, error) {
	return nil, nil
}
func (s *dataCenterServer) DownloadChunk(request *commonProto.ChunkInfo, response commonProto.DataTransferService_DownloadChunkServer) error {
	return nil
}
func (s *dataCenterServer) UploadFile(request commonProto.DataTransferService_UploadFileServer) error {
	return nil
}
func (s *dataCenterServer) ListFiles(ctx context.Context, request *commonProto.RequestFileList) (*commonProto.FileList, error) {
	return nil, nil
}
func (s *dataCenterServer) RequestFileUpload(ctx context.Context, request *commonProto.FileUploadInfo) (*commonProto.ProxyList, error) {
	return nil, nil
}

func startServer(username string, port string) {
	lis, err := net.Listen("tcp", ":"+port)
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	server := grpc.NewServer()
	ourProto.RegisterProxyServiceServer(server, &proxyServer{})
	commonProto.RegisterDataTransferServiceServer(server, &dataCenterServer{})
	// Register reflection service on gRPC server.
	reflection.Register(server)
	log.Printf("server starting at port : " + port + "username :" + username)
	if err := server.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}

func registerProxy() {
	for {
		// Hardcoded for now.... TODO get_raft_node() in common utils
		randomRaft := make(map[string]string)
		randomRaft["Ip"] = "10.0.10.2"
		randomRaft["Port"] = "10001"

		// Set up a connection to the server.
		conn, err := grpc.Dial(randomRaft["Ip"]+":"+randomRaft["Port"], grpc.WithInsecure())
		if err != nil {
			log.Printf("Could not register with raft ip :" + randomRaft["Ip"] + ",port :" + randomRaft["Port"])
		} else {
			defer conn.Close()
			stub := ourProto.NewRaftServiceClient(conn)

			ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
			defer cancel()
			r, err := stub.AddProxy(ctx, &ourProto.ProxyInfoRaft{Ip: myIP, Port: myPort})
			if err != nil {
				log.Printf("Could not register with raft ip :" + randomRaft["Ip"] + ",port :" + randomRaft["Port"])
				log.Printf("failed to serve: %v", err)
			} else if r.Id != -1 {
				log.Printf("Registered with raft ip :" + randomRaft["Ip"] + ",port :" + randomRaft["Port"])
				break
			}
		}
		time.Sleep(time.Second)
	}
}

func main() {
	go startServer("arpit", myPort)
	go registerProxy()
	for {
		time.Sleep(oneDay)
	}
}
