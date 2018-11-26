package main

import (
	"context"
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

// server is used to implement helloworld.GreeterServer.
type proxyServer struct{}

// SayHello implements helloworld.GreeterServer
func (s *proxyServer) ProxyHeartbeat(ctx context.Context, request *ourProto.Empty) (*ourProto.Empty, error) {
	return &ourProto.Empty{}, nil
}

func startServer(username string, port string) {
	lis, err := net.Listen("tcp", ":"+port)
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	server := grpc.NewServer()
	ourProto.RegisterProxyServiceServer(server, &proxyServer{})
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
			log.Printf("A Could not register with raft ip :" + randomRaft["Ip"] + ",port :" + randomRaft["Port"])
		} else {
			defer conn.Close()
			stub := ourProto.NewRaftServiceClient(conn)

			ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
			defer cancel()
			r, err := stub.AddProxy(ctx, &ourProto.ProxyInfoRaft{Ip: myIP, Port: myPort})
			if err != nil {
				log.Printf("B Could not register with raft ip :" + randomRaft["Ip"] + ",port :" + randomRaft["Port"])
				log.Printf("failed to serve: %v", err)
			} else if r.Id == 1 {
				log.Printf("Registered with raft ip :" + randomRaft["Ip"] + ",port :" + randomRaft["Port"])
				break
			}
		}
		time.Sleep(time.Second / 10.0)
	}
}

func main() {
	go startServer("arpit", myPort)
	go registerProxy()
	for {
		time.Sleep(oneDay)
	}
}
