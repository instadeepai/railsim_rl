from gymnasium.spaces import Box, Discrete, Tuple
import numpy as np
import math
from collections import namedtuple
import jpype
import jpype.imports

# Pull in types
from jpype.types import *

class Railsim:

    def __init__(self, jar_path: str, num_agents: int, depth_obs_tree: int) -> None:
        # Launch the JVM
        jpype.startJVM(classpath=[jar_path])

        self.depth_obs_tree: int = depth_obs_tree
        self.num_agents = num_agents

        # Create environment
        from railsim_dummy import Env

        random = True
        self.env = Env(num_agents, self.depth_obs_tree, random)
        self.agent_ids = self.env.getAgents()

        """
        For each agent i
        Observation[i][0]: list[float] = obs_tree
        Observation[i][1]: list[float] = train_state
        Observation[i][2]: list[float] = position_next_node

        default(obs_tree.depth) = 2
        len(obs_tree) = 17*(pow(2, obs_tree.depth) - 1)
        len(train_state) = 4
        len(position_next_node) = 2
        """

        # Observation space of single agent
        obs_space_single_agent = Tuple(
            (
                Box(
                    shape=(int(math.pow(2, self.depth_obs_tree + 1)),),
                    low=-math.inf,
                    high=math.inf,
                    dtype=np.float32,
                ),
                Box(shape=(4,), low=-math.inf, high=math.inf, dtype=np.float32),
                Box(
                    shape=(2,),
                    low=-math.inf,
                    high=math.inf,
                    dtype=np.float32,
                ),
            )
        )
        self.observation_space = {aid: obs_space_single_agent for aid in self.agent_ids}

        # Create a dict storing action_space corresponding to each agent
        """
        Possible Actions:
        0: Noop
        1: Change direction
        2: Stop
        """
        self.action_space = {aid: Discrete(3) for aid in self.agent_ids}

        self.ObservationTuple = namedtuple(
            "ObservationTuple", ["obs_tree", "train_state", "position_next_node"]
        )

    def agent_space(self, aid: any):
        return self.action_space[aid]

    def observation_space(self, aid: any):
        return self.observation_space[aid]

    def reset(self) -> tuple[dict[str, any], dict[str, any]]:
        """
        Return observations: dict[int, list[int | list]] and infos: dict[int, dict[str, bool | list | float]]
        """
        multi_agent_obs: dict = {}
        multi_agent_info: dict = {}
        resetOutput = self.env.reset()
        for aid in resetOutput.keys():
            obs = resetOutput[aid].getObs()
            multi_agent_obs[aid] = self.ObservationTuple(
                obs_tree=list(obs.getObsTree()),
                train_state=list(obs.getTrainState()),
                position_next_node=list(obs.getPositionNextNode()),
            )
            multi_agent_info[aid] = dict(resetOutput[aid].getInfo())

        return multi_agent_obs, multi_agent_info
    
    # TODO: Define reward function
    def _calc_reward(self, obs=None):
        return 0.0

    # TODO: Check how the dict from python looks like in JAVA environment
    def step(
        self, action_dict: dict[str, int]
    ) -> tuple[
        dict[str, tuple], dict[str, float], dict[str, bool], dict[str, bool], dict[str, any]
    ]:
        multi_agent_obs: dict = {}
        multi_agent_rewards: dict = {}
        multi_agent_terminated: dict = {}
        multi_agent_truncated: dict = {}
        multi_agent_info: dict = {}

        stepOutputDict = self.env.step(action_dict)
        for aid, stepOutput in stepOutputDict.items():
            obs = stepOutput.getObservation()
            multi_agent_obs[aid] = self.ObservationTuple(
                obs_tree=list(obs.getObsTree()),
                train_state=list(obs.getTrainState()),
                position_next_node=list(obs.getPositionNextNode()),
            )
            multi_agent_info[aid] = dict(stepOutput.getInfo())
            multi_agent_terminated[aid] = bool(stepOutput.isTerminated())
            multi_agent_truncated[aid] = bool(stepOutput.isTruncated())
            multi_agent_rewards[aid] = self._calc_reward(multi_agent_obs[aid])

        return (
            multi_agent_obs,
            multi_agent_rewards,
            multi_agent_terminated,
            multi_agent_truncated,
            multi_agent_info,
        )

    @property
    def agents(self):
        """
        Return the list of agents IDs of all the agents
        """
        return self.agent_ids


if __name__ == "__main__":
    railsim_env = Railsim(
        jar_path="/Users/akashsinha/Documents/railsim_rl/DummyEnv/target/DummyEnv-1.0-SNAPSHOT.jar",
        num_agents=3,
        depth_obs_tree=2,
    )
    multi_agent_obs, multi_agent_info = railsim_env.reset()
    x = railsim_env.step(action_dict={})
