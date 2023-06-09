import logging
from concurrent import futures
from time import sleep

import grpc

import helloworld_pb2
import helloworld_pb2_grpc


class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        message = request.name
        if message.startswith("[delay]"):
            sleep(5)
        return helloworld_pb2.HelloReply(message=message)

    def SayHelloAgain(self, request, context):
        return helloworld_pb2.HelloReply(message=f'Hello again, {request.name}!')


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
