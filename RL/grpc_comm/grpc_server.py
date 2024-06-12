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

    def __init__(self, action_queue: Queue, step_output_queue: Queue, action_cache: dict) -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.debug(
            f"GrpcServer() -> id step_output_queue: {id(step_output_queue)}"
        )

        self.action_q = action_queue
        self.step_output_q = step_output_queue

        #TODO: Find a way to reset the cache after each reset
        self.action_cache: dict = action_cache

    def _processStepOutputMap(self, request):

        # extract the StepOutput from request
        terminated_d = {}
        truncated_d = {}
        observation_d = {}
        reward_d = {}
        info_d = {}
        alive_agent_timestamp = None
        for aid, step_output in request.dictStepOutput.items():
            if not step_output.terminated:
                alive_agent_timestamp = step_output.observation.timestamp
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
            timestamp=alive_agent_timestamp,
            observation_d=observation_d,
            reward_d=reward_d,
            terminated_d=terminated_d,
            truncated_d=truncated_d,
            info_d=info_d,
        )

        return processed_step_output

    # Called by Railsim using GRPC
    def getAction(self, request, context):
        # Push the step_output in the queue
        self.logger.info(
            f"getAction() -> get action for train {request.trainId} at timestamp {request.timestamp}"
        )
        query_key = str(request.timestamp) + request.trainId

        if query_key in self.action_cache.keys():
            # If the query_key found in cache, then return the value and 
            # TODO: remove the entry from the cache
            action_map = railsim_pb2.ProtoActionMap(
                dictAction=self.action_cache[query_key]
            )
            return action_map

        while 1:
            #  Polling action from the queue
            self.logger.debug("getAction() -> waiting for action")
            timestamp, trainId, action_dict = self.action_q.get()
            if query_key == str(timestamp) + trainId:
                # Process the request and convert to a python object
                self.action_cache[query_key] = action_dict
                action_map = railsim_pb2.ProtoActionMap(dictAction=action_dict)
                return action_map
            else:
                self.action_cache[str(timestamp) + trainId] = action_dict

    # Called by Railsim using GRPC
    def updateState(self, request, context):
        self.logger.debug("updateState() -> Call received")
        processed_step_output = self._processStepOutputMap(request=request)

        # Push the step_output in the queue
        self.step_output_q.put(processed_step_output)

        return railsim_pb2.ProtoConfirmationResponse(ack="OK")


def serve(grpc_server: GrpcServer, free_port: int) -> None:

    logger = logging.getLogger(__name__)
    logger.debug("Starting the grpc server")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
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
