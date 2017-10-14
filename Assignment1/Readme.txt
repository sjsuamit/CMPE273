Docker run Considering we have the existing image ubuntu-python3.6-rocksdb-grpc:1.0, we create a
Dockerfile with the following contents to install ‘Flask’ on that image

Dockerfile contents - 
	
	FROM ubuntu-python3.6-rocksdb-grpc:1.0
	COPY . /Assignment1 WORKDIR /Assignment1
	RUN pip install Flask
	ENTRYPOINT ["python3.6"] 
	CMD ["program.py"]

Once the Dockerfile is ready. We create a new image which will contain flask. We will
name the image as "ubuntu-python3.6-rocksdb-grpc_flask" and tag "1.0". The command is
as follows -

Amits-iMac:Assignment1 amitchougule$ docker build -t ubuntu-python3.6-rocksdb-grpc_flask:1.0 .

To start the program.py application - 
On one terminal give the following command -

Amits-iMac:Assignment1 amitchougule$ docker run -it --rm --name flask_assignment -p 8000:5000 -v "$PWD":/usr/src/myapp2 -w /usr/src/myapp2 ubuntu-python3.6-rocksdb-grpc_flask:1.0 program.py

To send the file foo.py and hence call the POST method of program.py - 
Open a new terminal and give the command - 

Amits-iMac:Assignment1 amitchougule$ curl -i -X POST -H "Content-Type: multipart/form-data" -F "data=@foo.py" http://localhost:8000/api/v1/scripts

You will see an output like -

	HTTP/1.1 100 Continue

	HTTP/1.0 200 OK
	Content-Type: application/json
	Content-Length: 58
	Server: Werkzeug/0.12.2 Python/3.6.2
	Date: Fri, 06 Oct 2017 01:47:34 GMT

	{
		  "script-id": "5c59c6a7-7ddf-4a2a-98c9-66df4dc2520a"
	}

To execute foo.py at the server end and get the response of the foo.py file - 
We provide the ID at the end of the url.

Amits-iMac:Assignment1 amitchougule$ curl -i http://localhost:8000/api/v1/scripts/5c59c6a7-7ddf-4a2a-98c9-66df4dc2520a

You will see an output as shown below -

	HTTP/1.0 201 CREATED
	Content-Type: text/html; charset=utf-8
	Content-Length: 12
	Server: Werkzeug/0.12.2 Python/3.6.2
	Date: Fri, 06 Oct 2017 02:00:35 GMT

	Hello World
