import logging
from concurrent import futures

import grpc
from grpc_comm import StepOutput, railsim_pb2
from grpc_comm.railsim_pb2_grpc import (
    RailsimConnecterServicer,
    add_RailsimConnecterServicer_to_server,
)
from semi_mdp_env_wrapper.my_queue import MyQueue as Queue


class GrpcServer(RailsimConnecterServicer):

    def __init__(self, action_queue: Queue, step_output_queue: Queue) -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.debug(
            f"GrpcServer() -> id step_output_queue: {id(step_output_queue)}"
        )

        self.action_q = action_queue
        self.step_output_q = step_output_queue

    # Called by Railsim using GRPC
    def getAction(self, request, context):
        self.logger.debug("getAction Call received")

        temp_action_map = {}

        #  waiting for the action
        self.logger.debug("getAction() -> waiting for action $$")
        temp_action_map = self.action_q.get()
        self.logger.debug("getAction() -> got the action")

        # Process the request and convert to a python object
        action_map = railsim_pb2.ProtoActionMap(dictAction=temp_action_map)
        return action_map

    # Called by Railsim using GRPC
    def updateState(self, request, context):
        self.logger.debug("updateState() Call received")

        # extract the StepOutput from request
        terminated_d = {}
        truncated_d = {}
        observation_d = {}
        reward_d = {}
        info_d = {}

        for aid, step_output in request.dictStepOutput.items():
            terminated_d[aid] = step_output.terminated
            truncated_d[aid] = step_output.truncated
            reward_d[aid] = step_output.reward
            converted_obs_d = {}
            converted_obs_d["obs_tree"] = list(step_output.observation.obsTree)
            converted_obs_d["train_state"] = list(step_output.observation.trainState)
            converted_obs_d["position_next_node"] = list(
                step_output.observation.positionNextNode
            )
            observation_d[aid] = converted_obs_d

        processed_step_output = StepOutput(
            observation_d=observation_d,
            reward_d=reward_d,
            terminated_d=terminated_d,
            truncated_d=truncated_d,
            info_d=info_d,
        )

        # Push the step_output in the queue
        self.step_output_q.put(processed_step_output)

        return railsim_pb2.ProtoConfirmationResponse(ack="OK")


def serve(grpc_server: GrpcServer, free_port: int) -> None:

    logger = logging.getLogger(__name__)
    logger.debug("Starting the grpc server")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    add_RailsimConnecterServicer_to_server(grpc_server, server)
    server.add_insecure_port(f"[::]:{free_port}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    step_output_queue: Queue = Queue()
    action_queue: Queue = Queue()
    grpc_server = GrpcServer(
        action_queue=action_queue, step_output_queue=step_output_queue
    )
    serve(grpc_server)
