
1. DataCenter
    Heartbeat Receiver                                  -Arpit
    Register dc                                         -Arpit
    Replication initiation request handling
    Replication execution (Download from other dc)

2. Client
    Download - Thread fail checking                     -Aartee
    Upload - Thread fail checking                       -Aartee
    Ask for catalogue                                   -Aartee
    Optimize merge delete chunks once read for merge if file size    -Aartee
    Use temp folder                                                  -Aartee



3. Raft
    3.1 Create proper tables                -Anuj
    3.2 Handle upload file request          -Anuj
        - Check file exists or not
        - Create entry in table
        - return list of proxy

    3.3 Upload through proxy (Update raft tables) -Anuj

    3.4 Handle get file location info (returns proxy list)
        - If not found send request to other team to other team to get proxy and return back to client

    3.5 Consider as proxy and download from DC and return back to client

    3.6 Datacenter heartbeat sender                     -Arpit
    3.7 Datacenter registration receiver                -Arpit
        - Update DC table in raft

    3.8 Replication initiator for dc sending
    3.9 Catalogue request receiver              -Aartee
        - Ask from other teams                  -Aartee



## Optimizations

1. Use cache on datacenter to improve performance 
2. Queueing mechanism on proxy
3. Random number proxy selection
4. Research about Async behaviour (using queue)

5. Client file: threading vs futures