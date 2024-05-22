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
import numpy as np
from ray.rllib.policy.policy import Policy


class RailsimConnecter(RailsimConnecterServicer):

    def getAction(self, request, context):
        print("got a call")
        print(request)

        # Use the restored policy for serving actions.
        my_restored_policy = Policy.from_checkpoint(
            "RL/checkpoint/p0"
        )

        action_map = railsim_pb2.ActionMap()
        
        # Process the request and convert to a python object
        observation_dict = {}
        for key, observation in request.dictObservation.items():
            obs_tree = list(observation.obsTree)
            train_state = list(observation.trainState)
            position_next_node = list(observation.positionNextNode)
            observation_dict[key] = np.concatenate(
                (
                    np.array(obs_tree, dtype=np.float32),
                    np.array(train_state, dtype=np.float32),
                    np.array(position_next_node, dtype=np.float32),
                )
            )
            action_map.dictAction[key] = np.argmax(my_restored_policy.compute_single_action(observation_dict[key])[2]['action_dist_inputs'])

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
