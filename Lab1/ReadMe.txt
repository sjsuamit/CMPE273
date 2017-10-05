#Generate stub for client and server

docker run -it --rm --name grpc-tools -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 -m grpc.tools.protoc -I. --python_out=. --grpc_python_out=. datastore.proto

#server.py

docker run -it --rm --name server-script -p 3000:3000 
-v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 
python3.6 server.py

#Output:

Server started at...3000
put
get

#client.py

docker run -it --rm --name client-script 
-v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 
python3.6 client.py 172.17.0.2

#Output:

Client is connecting to Server at 172.17.0.2:3000...
## PUT Request: value = foo
## PUT Response: key = 8422efc4e5ce45d9a53f1c95c3400a06
## GET Request: key = 8422efc4e5ce45d9a53f1c95c3400a06
## GET Response: value = foo