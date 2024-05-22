import time
import numpy as np
from concurrent import futures
from railsim_pb2_grpc import (
    add_RailsimConnecterServicer_to_server,
    RailsimConnecterServicer,
)
import railsim_pb2
import grpc
from my_queue import MyQueue as Queue


class GrpcServer(RailsimConnecterServicer):

    def __init__(self, action_queue: Queue, next_state_queue: Queue) -> None:
        super().__init__()
        print("GrpcServer() -> id next_state_queue: ", id(next_state_queue))

        self.action_q = action_queue
        self.next_state_q = next_state_queue

    # Called by Railsim using GRPC
    def getAction(self, request, context):
        print("getAction Call received")
        # print(request)

        # action_map = railsim_pb2.ActionMap()
        temp_action_map = {}

        # push the observation to the obs queue

        #  waiting for the action
        print("getAction() -> waiting for action $$")
        temp_action_map = self.action_q.get()
        print("getAction() -> got the action")

        # Process the request and convert to a python object
        action_map = railsim_pb2.ActionMap(dictAction=temp_action_map)
        return action_map

    # Called by Railsim using GRPC
    def updateState(self, request, context):
        # update the next_state_dict variable
        print("updateState Call received")
        next_state_dict = {}
        for key, observation in request.dictObservation.items():
            obs_tree = list(observation.obsTree)
            train_state = list(observation.trainState)
            position_next_node = list(observation.positionNextNode)
            next_state_dict[key] = np.concatenate(
                (
                    np.array(obs_tree, dtype=np.float32),
                    np.array(train_state, dtype=np.float32),
                    np.array(position_next_node, dtype=np.float32),
                )
            )
        self.next_state_q.put(next_state_dict)

        # print(f"updateState() -> size of next_state_q after inserting data: {self.next_state_q.qsize()}")
        return railsim_pb2.ConfirmationResponse(ack="OK")


def serve(grpc_server: GrpcServer):

    print("Starting the grpc server")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    add_RailsimConnecterServicer_to_server(grpc_server, server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    next_state_queue: Queue = Queue()
    action_queue: Queue = Queue()
    print(id(next_state_queue))
    grpc_server = GrpcServer(
        action_queue=action_queue, next_state_queue=next_state_queue
    )
    serve(grpc_server)
