import jpype

# Enable Java imports
import jpype.imports
from gymnasium.spaces import Box, Discrete, Tuple
import numpy as np
import math

# from typing import *

# Pull in types
# from jpype.types import *


class Railsim:

    def __init__(self, jar_path: str) -> None:
        # Launch the JVM
        jpype.startJVM(classpath=[jar_path])

        # Get a list of agent Ids
        self.agent_ids: list[int] = None

        # Import java class from the classpath

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

        # Get the depth of observation tree
        depth_obs_tree: int = None

        # Observation space of single agent
        obs_space_single_agent = Tuple(
            (
                Box(
                    shape=(math.pow(2, depth_obs_tree + 1),),
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

    def agent_space(self, aid: any):
        return self.action_space[aid]

    def observation_space(self, aid: any):
        return self.observation_space[aid]

    def reset() -> tuple[list[float], list[float]]:
        """
        Return observations: dict[int, list[int | list]] and infos: dict[int, dict[str, bool | list | float]]
        """
        pass

    def step(
        action_dict: dict[str, int]
    ) -> tuple[list[float], list[float], dict[str, bool], dict[str, bool], list[float]]:
        pass

    @property
    def agents():
        """
        Return the list of agents IDs of all the agents
        """
        pass
