import math
from typing import Any, Optional
import multiprocessing as mp
from grpc_comm.railsim_factory_client import reset_env
from semi_mdp_env_wrapper.my_queue import MyQueue as Queue
import numpy as np
from gymnasium.spaces import Box, Discrete
from grpc_comm.grpc_server import GrpcServer, serve
from ray.rllib.env.multi_agent_env import MultiAgentEnv
from grpc_comm import StepOutput


class RailsimSemiMdp(MultiAgentEnv):

    def __init__(
        self,
        port: int,
        agent_ids: list,
        depth_obs_tree: int,
        step_output_queue: Queue,
        action_queue: Queue,
        train_state_size: int = 4,
        query_node_position_size: int = 2,
        observation_tree_node_size: int = 6,
    ) -> None:

        self.port = port
        print("RailsimSemiMdp() -> id step_output_queue: ", id(step_output_queue))
        self.depth_obs_tree: int = depth_obs_tree
        self.num_agents = len(agent_ids)
        self.agent_ids = agent_ids

        obs_space_single_agent = Box(
            shape=(
                observation_tree_node_size
                * int((math.pow(2, self.depth_obs_tree + 1) - 1) / 1)
                + train_state_size
                + query_node_position_size,
            ),
            low=-math.inf,
            high=math.inf,
            dtype=np.float32,
        )
        self.observation_space = {aid: obs_space_single_agent for aid in self.agent_ids}
        self.action_space = {aid: Discrete(3) for aid in self.agent_ids}

        self.step_output_queue = step_output_queue
        self.action_queue = action_queue

        # A list to track all terminated agents
        self.terminated_agents = []

    def observation_space_sample(self, agent_ids: list = None):
        sample = self.observation_space.sample()
        if agent_ids is None:
            return sample
        return {aid: sample[aid] for aid in agent_ids}

    def action_space_sample(self, agent_ids: list = None):
        sample = self.action_space.sample()
        if agent_ids is None:
            return sample
        return {aid: sample[aid] for aid in agent_ids}

    def _concat_and_pad_observation(self, observation):
        obs_tree = list(observation.obsTree)
        train_state = list(observation.trainState)
        position_next_node = list(observation.positionNextNode)

        #  pad obs_tree
        ideal_obs_tree_len = self.observation_tree_node_size * (
            math.pow(2, self.depth_obs_tree + 1) - 1
        )

        if len(obs_tree) != ideal_obs_tree_len:
            # pad the observation tree
            obs_tree = obs_tree + [0] * (ideal_obs_tree_len - len(obs_tree))

        observation_processed = np.concatenate(
            (
                np.array(obs_tree, dtype=np.float32),
                np.array(train_state, dtype=np.float32),
                np.array(position_next_node, dtype=np.float32),
            )
        )

        return observation_processed

    def reset(
        self, *, seed: Optional[int] = None, options: Optional[dict] = None
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """
        Args:
            seed (Optional[int], optional): Defaults to None.
            options (Optional[dict], optional): Defaults to None.

        Returns:
            tuple[dict[str, Any], dict[str, Any]]: Observation and infos corresponding to each agent
        """
        multi_agent_info: dict = {}
        print("reset() -> reset the railsim environment")

        # send reset signal to railsim
        reset_env(self.port)

        print("reset() -> wait to get next state from queue")
        step_out: StepOutput = self.step_output_queue.get()

        # extract observation from step_output and pad the observation tree
        obs_d = {}
        for aid, observation in step_out.observation_d.items():
            obs_d[aid] = self._concat_and_pad_observation(observation=observation)

        print("reset() -> Got the next state")

        # reset the terminated_list
        self.terminated_agents = []

        return obs_d, multi_agent_info

    def step(self, action_dict: dict[str, int]) -> tuple[
        dict[str, tuple],
        dict[str, float],
        dict[str, bool],
        dict[str, bool],
        dict[str, Any],
    ]:
        """
        Args:
            action_dict (dict[str, int]): A dictionary containing action corresponding to each agent

        Returns:
            tuple[ dict[str, tuple], dict[str, float], dict[str, bool], dict[str, bool], dict[str, Any], ]:
            obs, reward, terminated, truncated, info
        """
        # Put the action in the action queue
        print("step() -> push the action in the queue")
        self.action_queue.put(action_dict)

        # keep polling the next state queue
        print("step() -> waiting for next state")
        step_output: StepOutput = self.step_output_queue.get()

        print("step() -> got the next state")

        # Update the terminated_agents tracker
        for aid, terminated in step_output.terminated_d.items():
            if terminated:
                self.terminated_agents.append(aid)

        # Handle the case when all the agents are terminated
        terminated_d: dict = step_output.terminated_d
        truncated_d: dict = step_output.truncated_d

        all_terminated: bool = set(self.agent_ids) == set(self.terminated_agents)

        terminated_d["__all__"] = all_terminated
        truncated_d["__all__"] = all_terminated

        # extract observation from step_output and pad the observation tree
        obs_d = {}
        for aid, observation in step_output.observation_d.items():
            obs_d[aid] = self._concat_and_pad_observation(observation=observation)

        return (
            obs_d,
            step_output.reward_d,
            terminated_d,
            truncated_d,
            step_output.info_d,
        )

    def close(self):
        # TODO: What should be done here?
        pass
