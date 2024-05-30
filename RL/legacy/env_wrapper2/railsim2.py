import math
from typing import Any, Optional
import multiprocessing as mp
from grpc_comm.railsim_factory_client import reset_env
from env_wrapper2.my_queue import MyQueue as Queue
import numpy as np
from gymnasium.spaces import Box, Discrete
from grpc_comm.grpc_server import GrpcServer, serve


class Railsim2:

    def __init__(
        self,
        port: int,
        num_agents: int,
        depth_obs_tree: int,
        next_state_queue: Queue,
        action_queue: Queue,
    ) -> None:
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
        self.port = port
        print("Railsim2() -> id next_state_queue: ", id(next_state_queue))
        self.depth_obs_tree: int = depth_obs_tree
        self.num_agents = num_agents

        # TODO: Get AgentIDs in the reset call
        self.agent_ids = ["train0"]
        obs_space_single_agent = Box(
            shape=(17 * int(math.pow(2, self.depth_obs_tree + 1) - 1) + 4 + 2,),
            low=-math.inf,
            high=math.inf,
            dtype=np.float32,
        )
        self.obs_space = {aid: obs_space_single_agent for aid in self.agent_ids}

        # Create a dict storing action_space corresponding to each agent
        self.act_space = {aid: Discrete(3) for aid in self.agent_ids}

        self.next_state_queue = next_state_queue
        self.action_queue = action_queue

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
        multi_agent_info: dict = {}

        print("reset() -> reset the railsim environment")
        reset_env(self.port)
        # Request Environment factory server to instantiate railsim environment
        # This environment would talk to client on free_port
        print("reset() -> wait to get next state from queue")
        multi_agent_obs = self.next_state_queue.get()
        print("reset() -> Got the next state")

        return multi_agent_obs, multi_agent_info

    def _calc_reward(self, obs=None):
        return 1.0

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

        # Put the action in the action queue
        print("step() -> push the action in the queue")
        self.action_queue.put(action_dict)

        # keep polling the next state queue
        print("step() -> waiting for next state")
        multi_agent_obs = self.next_state_queue.get()
        print("step() -> got the next state")

        for aid in self.agent_ids:
            multi_agent_rewards[aid] = self._calc_reward()
            multi_agent_terminated[aid] = False
            multi_agent_truncated[aid] = False

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


def _simulation_loop(railsim_env):
    print("Simulation loop")
    ob, info = railsim_env.reset()
    for i in range(10):
        print(f"simulation  loop step: {i}")
        railsim_env.step({"a0": i})


if __name__ == "__main__":

    next_state_queue: Queue = Queue()
    action_queue: Queue = Queue()
    print("orig() -> id next_state_queue: ", id(next_state_queue))

    grpc_server = GrpcServer(
        action_queue=action_queue, next_state_queue=next_state_queue
    )

    process_server: mp.Process = mp.Process(target=serve, args=(grpc_server,))

    railsim_env = Railsim2(
        jar_path="/Users/akashsinha/Documents/railsim_rl/DummyEnv/target/DummyEnv-1.0-SNAPSHOT-jar-with-dependencies.jar",
        num_agents=2,
        depth_obs_tree=2,
        next_state_queue=next_state_queue,
        action_queue=action_queue,
    )

    process_sim_loop: mp.Process = mp.Process(
        target=_simulation_loop, args=(railsim_env,)
    )

    process_server.start()
    process_sim_loop.start()

    process_sim_loop.join()
    process_server.join()
