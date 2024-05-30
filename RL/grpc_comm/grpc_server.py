import numpy as np
from concurrent import futures
from grpc_comm.railsim_pb2_grpc import (
    add_RailsimConnecterServicer_to_server,
    RailsimConnecterServicer,
)
from grpc_comm import StepOutput, railsim_pb2
import grpc
from semi_mdp_env_wrapper.my_queue import MyQueue as Queue


class GrpcServer(RailsimConnecterServicer):

    def __init__(self, action_queue: Queue, step_output_queue: Queue) -> None:
        super().__init__()
        print("GrpcServer() -> id step_output_queue: ", id(step_output_queue))

        self.action_q = action_queue
        self.step_output_q = step_output_queue

    # Called by Railsim using GRPC
    def getAction(self, request, context):
        print("getAction Call received")
        # print(request)

        # action_map = railsim_pb2.ActionMap()
        temp_action_map = {}

        #  waiting for the action
        print("getAction() -> waiting for action $$")
        temp_action_map = self.action_q.get()
        print("getAction() -> got the action")

        # Process the request and convert to a python object
        action_map = railsim_pb2.ActionMap(dictAction=temp_action_map)
        return action_map

    # Called by Railsim using GRPC
    def updateState(self, request, context):
        print("updateState() Call received")

        # extract the StepOutput from request
        terminated_d = {}
        truncated_d = {}
        observation_d = {}
        reward_d = {}
        info_d = {}

        for aid, step_output in request.dictStepOutput.items():
            terminated_d[aid] = step_output.terminated
            truncated_d[aid] = step_output.truncated

            # observation = step_output.observation
            # obs_tree = list(observation.obsTree)
            # train_state = list(observation.trainState)
            # position_next_node = list(observation.positionNextNode)
            # observation_d[aid] = np.concatenate(
            #     (
            #         np.array(obs_tree, dtype=np.float32),
            #         np.array(train_state, dtype=np.float32),
            #         np.array(position_next_node, dtype=np.float32),
            #     )
            # )
            observation_d[aid] = step_output.observation
            reward_d[aid] = step_output.reward

        processed_step_output = StepOutput(
            observation_d=observation_d,
            reward_d=reward_d,
            terminated_d=terminated_d,
            truncated_d=truncated_d,
            info_d=info_d,
        )

        # Push the step_output in the queye
        self.step_output_q.put(processed_step_output)

        return railsim_pb2.ConfirmationResponse(ack="OK")


def serve(grpc_server: GrpcServer, free_port: int) -> None:

    print("Starting the grpc server")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    add_RailsimConnecterServicer_to_server(grpc_server, server)
    server.add_insecure_port(f"[::]:{free_port}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    step_output_queue: Queue = Queue()
    action_queue: Queue = Queue()
    print(id(step_output_queue))
    grpc_server = GrpcServer(
        action_queue=action_queue, step_output_queue=step_output_queue
    )
    serve(grpc_server)
