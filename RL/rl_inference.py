"""
1. Read data from grpc sent by Dummy Env
2. Forward propagate the observation
3. Return the actions
"""

from concurrent import futures
from railsim_pb2_grpc import (
    add_RailsimConnecterServicer_to_server,
    RailsimConnecterServicer,
)
import railsim_pb2
import grpc


class RailsimConnecter(RailsimConnecterServicer):

    def getAction(self, request, context):
        print("got a call")
        print(request)

        # Process the request and convert to a python object
        observation_tuple = []
        for key, observation in request.dictObservation.items():
            obs_tree = list(observation.obsTree)
            train_state = list(observation.trainState)
            position_next_node = list(observation.positionNextNode)
            observation_tuple.append((key, obs_tree, train_state,
                                      position_next_node))

        action_map = railsim_pb2.ActionMap()
        action_map.dictAction["train1"] = 0
        return action_map


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_RailsimConnecterServicer_to_server(RailsimConnecter(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    print(f"listenig to port: {50051}")
    serve()
