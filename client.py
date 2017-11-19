'''
################################## client.py #############################
'''
from concurrent import futures
import grpc
import time
import datastore_pb2
import datastore_pb2_grpc
import get_operation_pb2
import get_operation_pb2_grpc
import argparse
import subprocess
import rocksdb
import shutil

SERVER_PORT = 3000
CLIENT_PORT = 4000
_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class MyGetOperationServicer(get_operation_pb2.GetOperationServicer):
    def __init__(self):
        shutil.rmtree('client.db')
        self.db = rocksdb.DB("client.db", rocksdb.Options(create_if_missing=True))

    #this method makes modifications to the DB based on the received operation
    def addToClientDB(self,request,context):
        #receive <command:key:value>
        #we tokenize the reponse and perform the operation on local rocksdb
        operationInfo = request.data

        data = operationInfo.split(":")

        if data[0].lower() == "insert".lower():
            self.db.put(data[1].encode(), data[2].encode())
        elif data[0].lower() == "delete".lower():
            self.db.delete(data[1].encode())
        
        it = self.db.iteritems()
        it.seek_to_first()
        # prints [(b'key1', b'v1'), (b'key2, b'v2'), (b'key3', b'v3')]
        print (list(it))

        status = datastore_pb2.Response()
        status.data = operationInfo + " replicated at client"
        return status

#we create 'server1' for this client to expose a service 'addToClientDB'
client = grpc.server (futures.ThreadPoolExecutor (max_workers=5))
get_operation_pb2_grpc.add_GetOperationServicer_to_server(MyGetOperationServicer(), client)
client.add_insecure_port('%s:%d' % ('0.0.0.0', CLIENT_PORT))
client.start()

#used for command line arguments. We create the argument parser here.
parser = argparse.ArgumentParser()
#creating an argument "host" to read from command line. Host is the positional (required) argument, 
#hence no - or -- option is used
parser.add_argument("host", help="Specify the IP address of the server to connect to")
#we get the arguments from the parser
args = parser.parse_args()

'''
code to send the the client details - client IP address and client port to the server.
'''
#create channel to connect to server 
channel = grpc.insecure_channel('%s:%d' % (args.host, SERVER_PORT))
#create stub
stub = datastore_pb2.DatastoreStub(channel)
#Get the IP address of this container i.e. the clients container
host1 = subprocess.check_output(['bash', '-c', "/sbin/ip route|awk '/default/ { print $3 }'"]).decode('utf-8').strip()
#creating a string CLIENT_IP_ADDRESS:CLIENT_PORT
clientIPandPort = host1+":"+str(CLIENT_PORT)
#setting up the Request message
clientInfo = datastore_pb2.Request(data = clientIPandPort)
#rpc method 'RegisterClient' is passed the string CLIENT_IP_ADDRESS:CLIENT_PORT to be sent to server
status = stub.RegisterClient(clientInfo)
#response = self.stub.put(no)
print(status)

try:
    while True:
        #print("Client started at...%d" % CLIENT_PORT)
        time.sleep(_ONE_DAY_IN_SECONDS)
except KeyboardInterrupt:
    client.stop(0)




