#Generate stub for client and server

docker run -it --rm --name grpc-tools -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 -m grpc.tools.protoc -I. --python_out=. --grpc_python_out=. datastore.proto

#server.py

docker run -it --rm --name server-script -p 3000:3000 -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 server.py

#client.py

docker run -it --rm --name client-script -p 4000:4000 -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 client.py 172.17.0.2

#client2.py

docker run -it --rm --name client2-script -p 5000:5000 -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-pytho.6-rocksdb-grpc:1.0 python3.6 client2.py 172.17.0.2

#Instructions 
1. Run the new client in a separate container
2. Assign a new port to this client
3. Create a new rocksdb instance in this client 