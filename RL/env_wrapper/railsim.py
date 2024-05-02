import math
from typing import Any, Optional

import jpype
import jpype.imports
import numpy as np
from gymnasium.spaces import Box, Discrete


class Railsim:

    def __init__(self, jar_path: str, num_agents: int, depth_obs_tree: int) -> None:
        """Observation space:
        For each agent i
        Observation[i][0] = obs_tree
        Observation[i][1] = train_state
        Observation[i][2] = position_next_node

        default(obs_tree.depth) = 2
        len(obs_tree) = 17*(pow(2, obs_tree.depth) - 1)
        len(train_state) = 4
        len(position_next_node) = 2

        Possible Actions:
        0: Noop
        1: Change direction
        2: Stop
        """

        # Launch the JVM
        jpype.startJVM(classpath=[jar_path])

        self.depth_obs_tree: int = depth_obs_tree
        self.num_agents = num_agents

        # Create environment
        from railsim_dummy import Env

        random = True
        self.env = Env(num_agents, self.depth_obs_tree, random)
        self.agent_ids = list(self.env.getAgents())
        self.agent_ids = [str(ele) for ele in self.agent_ids]
        # Observation space of single agent
        # obs_space_single_agent = Tuple(
        #     (
        #         Box(
        #             shape=(17 * int(math.pow(2, self.depth_obs_tree + 1) - 1),),
        #             low=-math.inf,
        #             high=math.inf,
        #             dtype=np.float32,
        #         ),
        #         Box(shape=(4,), low=-math.inf, high=math.inf, dtype=np.float32),
        #         Box(
        #             shape=(2,),
        #             low=-math.inf,
        #             high=math.inf,
        #             dtype=np.float32,
        #         ),
        #     )
        # )
        obs_space_single_agent = Box(
            shape=(17 * int(math.pow(2, self.depth_obs_tree + 1) - 1) + 4 + 2,),
            low=-math.inf,
            high=math.inf,
            dtype=np.float32,
        )
        self.obs_space = {aid: obs_space_single_agent for aid in self.agent_ids}

        # Create a dict storing action_space corresponding to each agent
        self.act_space = {aid: Discrete(3) for aid in self.agent_ids}

    def action_space(self, aid: Any):
        return self.act_space[aid]

    def observation_space(self, aid: Any):
        return self.obs_space[aid]

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
        multi_agent_obs: dict = {}
        multi_agent_info: dict = {}
        resetOutput = self.env.reset()
        for aid in self.agent_ids:
            obs = resetOutput[aid].getObs()
            multi_agent_obs[aid] = np.concatenate(
                (
                    np.array(list(obs.getObsTree()), dtype=np.float32),
                    np.array(list(obs.getTrainState()), dtype=np.float32),
                    np.array(list(obs.getPositionNextNode()), dtype=np.float32),
                )
            )
            multi_agent_info[aid] = dict(resetOutput[aid].getInfo())

        return multi_agent_obs, multi_agent_info

    # TODO: Define reward function
    def _calc_reward(self, obs=None):
        return 1.0

    # TODO: Check how the dict from python looks like in JAVA environment
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
        multi_agent_obs: dict = {}
        multi_agent_rewards: dict = {}
        multi_agent_terminated: dict = {}
        multi_agent_truncated: dict = {}
        multi_agent_info: dict = {}

        stepOutputDict = self.env.step(action_dict)
        for aid in self.agent_ids:
            stepOutput = stepOutputDict[aid]
            obs = stepOutput.getObservation()
            multi_agent_obs[aid] = np.concatenate(
                (
                    np.array(list(obs.getObsTree()), dtype=np.float32),
                    np.array(list(obs.getTrainState()), dtype=np.float32),
                    np.array(list(obs.getPositionNextNode()), dtype=np.float32),
                )
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

    def close(self):
        # TODO: What should be done here?
        pass


if __name__ == "__main__":
    railsim_env = Railsim(
        jar_path="/Users/akashsinha/Documents/railsim_rl/DummyEnv/"
        "target/DummyEnv-1.0-SNAPSHOT.jar",
        num_agents=3,
        depth_obs_tree=2,
    )
    multi_agent_obs, multi_agent_info = railsim_env.reset()
    x = railsim_env.step(action_dict={})
    print("testing over")
