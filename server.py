'''
################################## server.py #############################
# Lab1 gRPC RocksDB Server 
################################## server.py #############################
'''
from concurrent import futures
import time
import grpc
import asyncio
import datastore_pb2
import datastore_pb2_grpc
import get_operation_pb2
import get_operation_pb2_grpc
import uuid
import rocksdb
import registerClients
import shutil

SERVER_PORT = 3000
CLIENT_PORT = 4000
_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class MyDatastoreServicer(datastore_pb2.DatastoreServicer):
    def RegisterClient(self, request, context):
        clientList = []
        #store the received data from client in 'receivedClientInfo'
        receivedClientInfo = request.data
        #extract client IP and client port from 'receivedClientInfo'
        clientIP, clientPort = receivedClientInfo.split(":")
        #create a 'Response' type variable
        clientInfo = datastore_pb2.Response()
        #store received data into clientInfo
        clientInfo.data = receivedClientInfo
        #call the 'registerThisClient method of the package 'registerClients' to add this to 'clientlist' file
        with open("clientlist.txt", "a") as myFile:
            myFile.write(clientIP + ":" + clientPort + "\n")
        #create a 'Response' type variable 'status' to send the status
        status = datastore_pb2.Response()
        status.data = "client " + str(clientIP+":"+clientPort) + " registered"
        print(status)
        return status

#Clear dependencies
#deleting the server.db directory before the first run
shutil.rmtree('server.db')
#clearing the contents of file clientlist.txt
open('clientlist.txt', 'w').close()


#run the server
db = rocksdb.DB("server.db", rocksdb.Options(create_if_missing=True))
server = grpc.server (futures.ThreadPoolExecutor (max_workers=5))
datastore_pb2_grpc.add_DatastoreServicer_to_server(MyDatastoreServicer(), server)
server.add_insecure_port('%s:%d' % ('0.0.0.0', SERVER_PORT))
server.start()
print("Server started at...%d" % SERVER_PORT)

#handle async rpc calls to multiple clients (future work)
async def rpcCall(operation):
    #read registered clients from file 
    with open('clientlist.txt') as fp:
        for clientInfo in fp:
            clientIP, clientPort = clientInfo.split(":")
            channel = grpc.insecure_channel('%s:%d' % (clientIP, int(clientPort)))
            stub = get_operation_pb2.GetOperationStub(channel)
            operationInfo = get_operation_pb2.RequestOperation(data=operation)
            z = stub.addToClientDB(operationInfo)
            print(z)
    await asyncio.sleep(0.01)

#handle async replication to multiple clients (future work)
async def replicateOperation(operation):
        await asyncio.wait([
            rpcCall(operation)
        ])

#decorator function for insert() and delete()
def decorator_function(original_function):
    def wrapper_function(*args, **kwargs):
        operation = args[0]     
        data = args[0].split(":")
        #perform operations on master DD
        if data[0].lower() == "insert".lower():
            db.put(data[1].encode(), data[2].encode())
        elif data[0].lower() == "delete".lower():
            db.delete(data[1].encode())
        it = db.iteritems()
        it.seek_to_first()
        # prints [(b'key1', b'v1'), (b'key2, b'v2'), (b'key3', b'v3')]
        print (list(it))

        #asyncio implementation to call the replicateOperation() function
        loop = asyncio.get_event_loop()
        #'loop' is waiting for all rpc calls to complete
        loop.run_until_complete(replicateOperation(operation))
        return original_function(*args, **kwargs)
    return wrapper_function

@decorator_function
def insert(operation):
    pass

@decorator_function
def delete(operation):
    pass

#change this delay to accept commands as soon as client(s) register
time.sleep(15)

while True:   
    operation = input('Enter Operation(command:key:value): ')

    if operation.strip() == "exit":
        exit()

    data = operation.split(":")

    if data[0].lower() == "insert".lower():
        insert(operation)
    elif data[0].lower() == "delete".lower():
        delete(operation)
    else:
        print("Invalid operation")
            #exit();

try:
  while True:
    #print("Server started at...%d" % SERVER_PORT)
    time.sleep (_ONE_DAY_IN_SECONDS)
except KeyboardInterrupt:
  server.stop(0) 

