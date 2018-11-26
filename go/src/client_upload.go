package main

import (
	"context"
	commonProto "grpc"
	"log"
	"math"
	"os"
	"strconv"
	"time"

	"google.golang.org/grpc"
)

const (
	oneDay   = 60 * 60 * 24 * time.Second
	SEQ_SIZE = 1024 * 1024
)

func main() {
	// Hardcoded for now.... TODO get_raft_node() in common utils

	fileName := "/Users/arpit/Desktop/147mb.mkv"
	fileSize := 0
	randomRaft := make(map[string]string)
	randomRaft["Ip"] = "10.0.10.1"
	randomRaft["Port"] = "10000"

	startTime := time.Now()

	// Set up a connection to the server.
	conn, err := grpc.Dial(randomRaft["Ip"]+":"+randomRaft["Port"], grpc.WithInsecure())
	if err != nil {
		log.Printf("Could not register with raft ip :" + randomRaft["Ip"] + ",port :" + randomRaft["Port"])
	} else {
		defer conn.Close()
		stub := commonProto.NewDataTransferServiceClient(conn)

		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		defer cancel()

		fi, err := os.Stat(fileName)
		if err != nil {
			log.Printf("file error:%v", err)
		}

		fileSize = int(math.Ceil(float64(fi.Size())))
		log.Printf("File Size: %v", fileSize)
		newFileName := strconv.FormatInt(time.Now().Unix(), 10) + "147mb.mkv"
		log.Printf("File Name: %v", newFileName)
		r, err := stub.RequestFileUpload(ctx, &commonProto.FileUploadInfo{FileName: newFileName, FileSize: float32(fileSize)})
		if err != nil {
			log.Printf("Could not register with raft ip :" + randomRaft["Ip"] + ",port :" + randomRaft["Port"])
			log.Printf("failed to serve: %v", err)
		}
		log.Printf("Res: %v", r)
		log.Printf(r.LstProxy[0].Ip)

		proxyConn, err := grpc.Dial(r.LstProxy[0].Ip+":"+r.LstProxy[0].Port, grpc.WithInsecure())
		if err != nil {
			log.Printf("Could not connect to proxy :" + r.LstProxy[0].Ip + ",port :" + r.LstProxy[0].Port)
			return
		}
		defer conn.Close()

		fi1, err := os.Open(fileName)
		if err != nil {
			log.Printf("file not opened :%v", err)
			return
		}
		proxyStub := commonProto.NewDataTransferServiceClient(proxyConn)
		stream, err := proxyStub.UploadFile(context.Background())
		if err != nil {
			log.Printf("stream :%v", err)
		}

		readBytes := SEQ_SIZE
		var curSeqNum int64
		maxSeq := int64(math.Ceil(float64(fileSize / SEQ_SIZE)))

		for readBytes == SEQ_SIZE {
			data := make([]byte, SEQ_SIZE)
			readBytes, err = fi1.Read(data)
			if err != nil {
				log.Printf("could not read :%v", err)
			}
			chunkData := &commonProto.FileUploadData{
				FileName: newFileName,
				ChunkId:  0,
				Data:     data,
				SeqNum:   curSeqNum,
				SeqMax:   maxSeq}

			log.Printf("Sending Sequence: %v", curSeqNum)
			if err := stream.Send(chunkData); err != nil {
				log.Printf("send error :%v", err)
			}

			curSeqNum++
		}

		_, err = stream.CloseAndRecv()
		if err != nil {
			log.Printf("end stream :%v", err)
		}

	}
	log.Printf("Total Time: %v", time.Since(startTime).Seconds())
}
