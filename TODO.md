
1. DataCenter
    Heartbeat Receiver                                                                  DONE        -Arpit
    Register dc                                                                         DONE        -Arpit
    Replication initiation request handling                                             DONE        -Arpit
    Replication execution (Download from other dc)                                      DONE        -Arpit

    UploadCompleted Failed Upload Handling                                              PENDING     -Arpit

2. Client
    Download - Thread fail checking                                                     DONE        -Aartee
    Upload - Thread fail checking                                                       DONE        -Aartee
    Ask for catalogue                                                                   DONE        -Aartee
    Optimize merge delete chunks once read for merge if file size                       DONE        -Aartee
    Use temp folder                                                                     REMOVED     (Permission issues on different OS)

3. Raft
    3.1 Create proper tables                
        3.1.1 File_log                                                                  DONE        -Anuj
        3.1.2 File_info_table                                                           DONE        -Anuj
        3.1.3 DC_available_table                                                        DONE        -Anuj
        3.1.4 Proxy_available_table                                                     DONE        -Anuj
    3.2 Handle upload file request          
        - Check file exists or not                                                      DONE        -Anuj
        - Create entry in table                                                         DONE        -Anuj
        - return list of proxy                                                          DONE        -Anuj
    3.3 Upload complete raft updates(Update raft tables on completion)                  DONE        -Anuj
    3.4 Handle get file location info (returns proxy list)                              DONE        -Anuj
        - If not found send request to other team to other team 
          to get proxy and return back to client

    3.5 Consider as proxy and download from DC and return back to client                REMOVED     (saperate proxy now)
    3.6 Datacenter heartbeat sender                                                     DONE        -Anuj        
    3.7 Datacenter registration request handling                                        DONE        -Anuj                
    3.8 Replication initiator for dc sending                                            DONE        -Anuj                    
    3.9 Catalogue request receiver                                                      DONE        -Aartee
        - Ask from other teams                                                          DONE        -Aartee
    3.10 Raft add to logs after confirmation from other raft nodes                      PENDING     -Anuj

4. Proxy
    

## Optimizations

1. Use cache on datacenter to improve performance 
2. Queueing mechanism on proxy
3. Random number proxy selection
4. Research about Async behaviour (using queue)

5. Client file: threading vs futures