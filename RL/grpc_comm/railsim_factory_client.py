from __future__ import print_function

import logging

import grpc
from grpc_comm import railsim_pb2, railsim_pb2_grpc

logger = logging.getLogger(__name__)


# Factory Environment server always runs on 50051.
# free_port is used for communication between the Environment and RL
# This request would start instantiate the env and create a RLClient &
# reset the environment
def request_environment(free_port: int) -> None:
    logger.debug("Connecting with the EnvironmentFactoryServer ...")
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = railsim_pb2_grpc.RailsimFactoryStub(channel)
        response = stub.getEnvironment(railsim_pb2.ProtoGrpcPort(grpcPort=free_port))

        logger.debug(f"Create Env response: {response.ack}")


def reset_env(free_port) -> list[str]:
    logger.debug(f"Resetting the env on port {free_port} ...")
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = railsim_pb2_grpc.RailsimFactoryStub(channel)
        response: railsim_pb2.ProtoAgentIDs = stub.resetEnv(
            railsim_pb2.ProtoGrpcPort(grpcPort=free_port)
        )
        return response.agentId

def get_agent_ids(free_port) -> list[str]:
    logger.debug(f"getting the agentIds for env on port {free_port} ...")
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = railsim_pb2_grpc.RailsimFactoryStub(channel)
        response: railsim_pb2.ProtoAgentIDs = stub.getAgentIds(
            railsim_pb2.ProtoGrpcPort(grpcPort=free_port)
        )
        return response.agentId
