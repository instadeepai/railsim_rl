from __future__ import print_function
import grpc
from grpc_comm import railsim_pb2
from grpc_comm import railsim_pb2_grpc


# Factory Environment server always runs on 50051. 
# free_port is used for communication between the Environment and RL
# This request would start instantiate the env and create a RLClient &
# reset the environment
def request_environment(free_port):
    print("Connecting with the EnvironmentFactoryServer ...")
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = railsim_pb2_grpc.RailsimFactoryStub(channel)
        response = stub.getEnvironment(railsim_pb2.GrpcPort(grpcPort=free_port))

        print("Create Env response: " + response.ack)


# TODO: The intial observation can be returned as a respone to this function. 
def reset_env(free_port):
    print(f"Resetting the env with port {free_port} ...")
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = railsim_pb2_grpc.RailsimFactoryStub(channel)
        response = stub.resetEnv(railsim_pb2.GrpcPort(grpcPort=free_port))
        print("Reset Env response: " + response.ack)

