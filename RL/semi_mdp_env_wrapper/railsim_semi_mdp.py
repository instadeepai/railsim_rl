import logging
import math
from typing import Any, Optional
import gymnasium as gym
import numpy as np
from grpc_comm.grpc_server import GrpcServer
from grpc_comm import StepOutput
from grpc_comm.railsim_factory_client import reset_env, get_agent_ids
from gymnasium.spaces import Box, Discrete
from ray.rllib.env.multi_agent_env import MultiAgentEnv
from semi_mdp_env_wrapper.my_queue import MyQueue as Queue


class RailsimSemiMdp(MultiAgentEnv):

    def __init__(
        self,
        port: int,
        depth_obs_tree: int,
        step_output_queue: Queue,
        action_queue: Queue,
        grpc_server: GrpcServer,
        train_state_size: int = 4,
        query_node_position_size: int = 2,
        observation_tree_node_size: int = 6,
    ) -> None:
        super().__init__()
        self.port = port
        self.logger = logging.getLogger(__name__)
        self.logger.debug(
            f"RailsimSemiMdp() -> id step_output_queue: {id(step_output_queue)}"
        )
        self.depth_obs_tree = depth_obs_tree
        self.step_output_queue = step_output_queue
        self.action_queue = action_queue

        self.train_state_size = train_state_size
        self.query_node_position_size = query_node_position_size
        self.observation_tree_node_size = observation_tree_node_size

        # A list to track all terminated agents
        self.terminated_agents = []

        self._agent_ids = set(get_agent_ids(self.port))
        self._define_obs_act_spaces()
        self._obs_space_in_preferred_format = True
        self._action_space_in_preferred_format = True

        self.timestamp = None
        self.selected_trainId = None
        self.grpc_server = grpc_server


    def _define_obs_act_spaces(self):
        # define the observation space and action space
        self.num_agents = len(self._agent_ids)

        # define the observation space and action space based on the agent list
        obs_space_single_agent = Box(
            shape=(
                self.observation_tree_node_size
                * int((math.pow(2, self.depth_obs_tree + 1) - 1) / 1)
                + self.train_state_size
                + self.query_node_position_size,
            ),
            low=-math.inf,
            high=math.inf,
            dtype=np.float32,
        )
        self.observation_space = gym.spaces.Dict(
            {aid: obs_space_single_agent for aid in self._agent_ids}
        )
        self.action_space = gym.spaces.Dict(
            {aid: Discrete(3) for aid in self._agent_ids}
        )

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
        obs_tree = observation["obs_tree"]
        train_state = observation["train_state"]
        position_next_node = observation["position_next_node"]

        #  pad obs_tree
        ideal_obs_tree_len = self.observation_tree_node_size * (
            math.pow(2, self.depth_obs_tree + 1) - 1
        )

        if len(obs_tree) != ideal_obs_tree_len:
            # pad the observation tree
            obs_tree = obs_tree + [0] * int(ideal_obs_tree_len - len(obs_tree))

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
        self.logger.debug("reset() -> reset the railsim environment")

        # send reset signal to railsim
        self._agent_ids = reset_env(self.port)
        self.num_agents = len(self._agent_ids)

        # define the observation space and action space based on the agent list
        self._define_obs_act_spaces()

        # wait to get next state from queue
        self.logger.debug("reset() -> wait to get next state from queue")
        step_out: StepOutput = self.step_output_queue.get()
        
        # Update the global variables: Timestamp and trainId 
        self.selected_trainId = None
        self.timestamp = step_out.timestamp
        for key, value in step_out.terminated_d.items():
            if (not value):
                self.selected_trainId = key 

        # # Reset the action cache
        # self.grpc_server.action_cache = {}

        # If there are no agents in the system, end the training loop
        terminated_agents = []
        for aid, terminated in step_out.terminated_d.items():
            if terminated:
                terminated_agents.append(aid)

        if set(terminated_agents) == set(self._agent_ids):
            raise Exception(
                "There are no active agents in the environment for this scenario"
            )

        # extract observation from step_output and pad the observation tree
        obs_d = {}
        for aid, observation in step_out.observation_d.items():
            obs_d[aid] = self._concat_and_pad_observation(observation=observation)

        self.logger.debug("reset() -> Got the next state")

        # reset the terminated_list
        self.terminated_agents = []
        self.truncated_agents= []

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
        self.logger.debug(f"step() -> push the action in the queue. Actions: {action_dict}. Timestamp: {self.timestamp}")
        self.action_queue.put((self.timestamp, self.selected_trainId, action_dict))

        # keep polling the next state queue
        self.logger.debug("step() -> waiting for observations")
        step_output: StepOutput = self.step_output_queue.get()

        # Update the global variables: Timestamp and trainId 
        self.timestamp = step_output.timestamp
        self.selected_trainId = None
        for key, value in step_output.terminated_d.items():
            if (not value):
                # store the agent id of the train whose observation will be
                #  processed by the rl model
                self.selected_trainId = key 

        self.logger.debug(f"step() -> got observations for trains: {step_output.terminated_d.keys()}. Timestamp: {self.timestamp}")

        # Update the terminated_agents tracker
        for aid, terminated in step_output.terminated_d.items():
            if terminated:
                self.terminated_agents.append(aid)
        
        # Update the truncated_agents tracker
        for aid, truncated in step_output.truncated_d.items():
            if truncated:
                self.truncated_agents.append(aid)

        # Handle the case when all the agents are terminated
        terminated_d: dict = step_output.terminated_d
        truncated_d: dict = step_output.truncated_d

        all_terminated: bool = set(self._agent_ids) == set(self.terminated_agents)
        all_truncated: bool = set(self._agent_ids) == set(self.truncated_agents)

        terminated_d["__all__"] = all_terminated
        truncated_d["__all__"] = all_truncated

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
