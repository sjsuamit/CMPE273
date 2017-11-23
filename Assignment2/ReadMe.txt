Assuming we have the docker image built and running -

#Generate stub for client and server

docker run -it --rm --name grpc-tools -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 -m grpc.tools.protoc -I. --python_out=. --grpc_python_out=. datastore.proto

#Generate stub for client and server

docker run -it --rm --name grpc-tools -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 -m grpc.tools.protoc -I. --python_out=. --grpc_python_out=. get_operation.proto

#server.py

docker run -it --rm --name server-script -p 3000:3000 -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 server.py

#client.py

docker run -it --rm --name client-script -p 4000:4000 -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 client.py 172.17.0.2
