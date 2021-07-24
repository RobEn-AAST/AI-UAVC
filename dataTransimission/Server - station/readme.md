<h1 align="center"> UAV Server module</h1>


## Over View :
A Module for data exchange between with the client

#### prequsites :-
- open cv
- numpy

## usage :-
- create a client object.
  - object paramters are : 
    - port : the port number used to communicate with clients <b>5000</b> during testing

```bash
myclientname = myserver = UAV_SERVER(Port=5000)
```
## features :-
1. attributes
    - conn : socket established
    - initialized : boolean representing the status of the connection
    - From : The IP address of the client ( PI ) 
2. methods
    - receiveMissions()
      - Receives mission object from the client and Handles it acccording to the object content

    - missionHandling(conn, Mission)
      - Static function used for handling Mission objects
