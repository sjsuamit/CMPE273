FROM ubuntu-python3.6-rocksdb-grpc:1.0

COPY . /Assignment1
WORKDIR /Assignment1

RUN pip install Flask

ENTRYPOINT ["python3.6"]
CMD ["program.py"]