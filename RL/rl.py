# import os
# import ray
import socketserver
import time
from env_wrapper.railsim import Railsim
from ray.rllib.core.rl_module.marl_module import MultiAgentRLModuleSpec
from ray.rllib.core.rl_module.rl_module import SingleAgentRLModuleSpec

# from ray import tune
# from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.env.wrappers.pettingzoo_env import ParallelPettingZooEnv

# from ray.rllib.models import ModelCatalog
# from ray.rllib.models.torch.torch_modelv2 import TorchModelV2
from ray.tune.registry import get_trainable_cls, register_env
from experiment_script import (
    add_rllib_example_script_args,
    run_rllib_example_script_experiment,
)
import multiprocessing as mp
from env_wrapper2.my_queue import MyQueue as Queue
from grpc_comm.grpc_server import GrpcServer, serve
from env_wrapper2.railsim2 import Railsim2
from grpc_comm.railsim_factory_client import request_environment
# from my_queue import MyQueue as Queues


# def env_creator(args):
#     env = ParallelPettingZooEnv(
#         Railsim(           
#             jar_path="DummyEnv/target/DummyEnv-1.0-SNAPSHOT.jar",
#             num_agents=3,
#             depth_obs_tree=2,
#         )
#     )

#     return env


def create_env2(args):
    next_state_queue: Queue = Queue()
    action_queue: Queue = Queue()
    print("orig() -> id next_state_queue: ", id(next_state_queue))

    with socketserver.TCPServer(("localhost", 0), None) as s:
        free_port = s.server_address[1]

    grpc_server = GrpcServer(
        action_queue=action_queue, next_state_queue=next_state_queue
    )
    print(f"RL listening on port {free_port}")
    process_server: mp.Process = mp.Process(
        target=serve,
        args=(
            grpc_server,
            free_port,
        ),
    )
    process_server.start()

    # Instantiate a new java environment
    request_environment(free_port=free_port)

    wait_time = 10
    print(f"Waiting for the server to start for {wait_time} seconds before the environment simulation")
    time.sleep(wait_time)

    # Create the railsim env wrapper 
    railsim_env = Railsim2(
        port=free_port,
        num_agents=2,
        depth_obs_tree=2,
        next_state_queue=next_state_queue,
        action_queue=action_queue,
    )
    
    return ParallelPettingZooEnv(railsim_env)


parser = add_rllib_example_script_args(
    default_iters=200,
    default_timesteps=1000000,
    default_reward=0.0,
)

if __name__ == "__main__":
    args = parser.parse_args()
    assert args.num_agents > 0, "Must set --num-agents > 0 when running this script!"
    assert (
        args.enable_new_api_stack
    ), "Must set --enable-new-api-stack when running this script!"

    # register_env("env", lambda config: env_creator(config))
    register_env("env", lambda config: create_env2(config))

    base_config = (
        get_trainable_cls(args.algo)
        .get_default_config()
        .environment("env", disable_env_checking=True)
        .multi_agent(
            policies={"p0"},
            # All agents map to the exact same policy.
            policy_mapping_fn=(lambda aid, *args, **kwargs: "p0"),
        )
        .training(
            model={
                "vf_share_layers": True,
            },
            vf_loss_coeff=0.005,
            train_batch_size=512,
        )
        .rl_module(
            rl_module_spec=MultiAgentRLModuleSpec(
                module_specs={"p0": SingleAgentRLModuleSpec()},
            ),
        )
    )

    run_rllib_example_script_experiment(base_config, args)
    # request_environment(50053)
