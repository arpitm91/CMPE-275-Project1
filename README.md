# CMPE-275-Project1

## System Architecture
![System Architecture](/images/System_architecture.png)

## Installation Guide:

Install python3.

Install dependencies.
```
pip3 install requirements.txt
```

## Setup Guide

Setup raft, datacenter and proxy configurations in `connections/connections.py`

1. Run Raft:
```
python3 raft/raft.py <raft node name>
```
2. Run Datacenter:
```
python3 data_center/datacenter.py <datacenter node name>
```
3. Run Proxy:
```
python3 proxy/proxy.py <proxy node name>
```


4. Upload File:
```
python3 client/client_upload.py <path to file>
```

5. Get file catalogue:
```
python3 client/client_file_list.py
```

6. Download File:
```
python3 client/client_download.py <file name>
```