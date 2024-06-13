from pettingzoo import AECEnv
from gymnasium.utils import EzPickle
import logging
import math
from typing import Any, Optional, TypeVar
import gymnasium as gym
import numpy as np
from grpc_comm.grpc_server import GrpcServer
from grpc_comm import StepOutput
from grpc_comm.railsim_factory_client import reset_env, get_agent_ids
from gymnasium.spaces import Box, Discrete
from ray.rllib.env.multi_agent_env import MultiAgentEnv
from semi_mdp_env_wrapper.my_queue import MyQueue as Queue

ObsType = TypeVar("ObsType")
ActionType = TypeVar("ActionType")
AgentID = TypeVar("AgentID")


class railsim_aec(AECEnv, EzPickle):

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
        *args,
        **kwargs,
    ):
        EzPickle.__init__(self, *args, **kwargs)
        AECEnv.__init__(self)

        self.port = port
        self.logger = logging.getLogger(__name__)
        self.logger.debug(
            f"RailsimSemiMdp() -> id step_output_queue: {id(step_output_queue)}"
        )
        # comms with the grpc_server
        self.step_output_queue = step_output_queue
        self.action_queue = action_queue

        # define the spaces
        self.depth_obs_tree = depth_obs_tree
        self.train_state_size = train_state_size
        self.query_node_position_size = query_node_position_size
        self.observation_tree_node_size = observation_tree_node_size
        self._define_obs_act_spaces()

        # A dictionary to track all terminated and truncated agents
        self.terminations: dict[AgentID, bool] = {}
        self.truncations: dict[AgentID, bool] = {}

        # All agents that may appear in the environment
        self.possible_agents = set(get_agent_ids(self.port))
        # Agents active at any given time
        self.agents = []
        # Reward from the last step for each agent
        self.rewards: dict[AgentID, float] = {}
        # Cumulative rewards for each agent
        self._cumulative_rewards: dict[AgentID, float] = {}
        # Additional information from the last step for each agent
        self.infos: dict[AgentID, dict[str, Any]] = {}
        # The agent currently being stepped

        self.agent_selection: AgentID = None
        self.timestamp = None
        self.grpc_server = grpc_server

        self._observation_lookup_dict: dict[AgentID, StepOutput] = {}

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
        self.observation_spaces = gym.spaces.Dict(
            {aid: obs_space_single_agent for aid in self._agent_ids}
        )
        self.action_spaces = gym.spaces.Dict(
            {aid: Discrete(3) for aid in self._agent_ids}
        )

    def observation_space(self, agent):
        return self.observation_spaces[agent]

    def action_space(self, agent):
        return self.action_spaces[agent]

    def convert_to_dict(self, list_of_list):
        return dict(zip(self.agents, list_of_list))

    def _query_step_output_queue(self) -> None:
        # wait to get next state from queue
        self.logger.debug("reset() -> wait to get next state from queue")
        step_out: StepOutput = self.step_output_queue.get()

        # push the obs correponding to the agent and timestamp in the loopup map
        query_key = self._get_query_key(
            timestamp=self.timestamp, agent_id=self.agent_selection
        )
        self._observation_lookup_dict[query_key] = step_out

        # Update the global variables: timestamp and agent_selection
        self.timestamp = step_out.timestamp
        for key, value in step_out.terminated_d.items():
            if not value:
                self.agent_selection = key

    def _push_action_in_queue(self, action_dict: dict) -> None:
        self.logger.debug(
            f"step() -> push the action in the queue. Actions: {action_dict}. Timestamp: {self.timestamp}"
        )
        self.action_queue.put((self.timestamp, self.agent_selection, action_dict))

    def reset(self, seed=None, options=None):
        if seed is not None:
            self.env._seed(seed=seed)

        # send reset signal to railsim
        self.possible_agents = reset_env(self.port)
        self.agents = self.possible_agents[:]

        # define the observation space and action space based on the agent list
        self._define_obs_act_spaces()

        # get the first event
        self._query_step_output_queue()

        self.rewards = dict(zip(self.agents, [(0) for _ in self.agents]))
        self._cumulative_rewards = dict(zip(self.agents, [(0) for _ in self.agents]))

        self.terminations = dict(zip(self.agents, [False for _ in self.agents]))
        self.truncations = dict(zip(self.agents, [False for _ in self.agents]))
        self.infos = dict(zip(self.agents, [{} for _ in self.agents]))

    def close(self):
        # if self.has_reset:
        #     self.env.close()
        pass

    def render(self):
        pass

    def _get_query_key(self, timestamp, agent_id):
        return str(timestamp) + agent_id

    def step(self, action):
        if (
            self.terminations[self.agent_selection]
            or self.truncations[self.agent_selection]
        ):
            self._was_dead_step(action)
            return

        # Put the action in the action queue
        self._push_action_in_queue(action_dict=action)

        # Poll the next state queue. Also, update the timestamp and agent_selection
        self._query_step_output_queue()

        # update the rewards
        query_key = self._get_query_key(
            timestamp=self.timestamp, agent_id=self.agent_selection
        )
        for aid, reward in self._observation_lookup_dict[query_key].reward_d.items():
            self.rewards[aid] = reward

        # update terminated and truncated dictionaries
        for aid, termination in self._observation_lookup_dict[query_key].terminated_d.items():
            self.terminations[aid] = termination

        for aid, truncation in self._observation_lookup_dict[query_key].truncated_d.items():
            self.truncations[aid] = truncation

        # TODO: What is is_last flag doing?

        for r in self.rewards:
            self.rewards[r] = self.env.control_rewards[self.agent_name_mapping[r]]
        
        if is_last:
            for r in self.rewards:
                self.rewards[r] += self.env.last_rewards[self.agent_name_mapping[r]]

        # self._cumulative_rewards[self.agent_selection] = 0
        self.agent_selection = self._agent_selector.next()
        self._accumulate_rewards()

    def observe(self, agent):
        # extract observation from step_output and pad the observation tree
        obs_d = {}
        query_key = str(self.timestamp) + self.agent_selection
        for aid, observation in self._observation_lookup_dict[
            query_key
        ].observation_d.items():
            if agent == aid:
                obs_d[aid] = self._concat_and_pad_observation(observation=observation)

        assert len(obs_d) > 0, f"No observations present for the agent {agent}"
        return self.env.observe()
