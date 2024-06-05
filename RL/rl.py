import logging
import multiprocessing as mp
import socketserver
import time
from experiment_script import (
    add_rllib_example_script_args,
    run_rllib_example_script_experiment,
)
from grpc_comm.grpc_server import GrpcServer, serve
from grpc_comm.railsim_factory_client import request_environment
from ray.rllib.core.rl_module.marl_module import MultiAgentRLModuleSpec
from ray.rllib.core.rl_module.rl_module import SingleAgentRLModuleSpec
from ray.tune.registry import get_trainable_cls, register_env
from semi_mdp_env_wrapper.my_queue import MyQueue as Queue
from semi_mdp_env_wrapper.railsim_semi_mdp import RailsimSemiMdp


def create_env(args):
    logger = logging.getLogger(__name__)
    step_output_queue: Queue = Queue()
    action_queue: Queue = Queue()
    logger.debug(f"orig() -> id step_output_queue: {id(step_output_queue)}")

    with socketserver.TCPServer(("localhost", 0), None) as s:
        free_port = s.server_address[1]

    grpc_server = GrpcServer(
        action_queue=action_queue, step_output_queue=step_output_queue
    )
    logger.debug(f"RL listening on port {free_port}")
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
    logger.debug(
        f"Waiting for the server to start for {wait_time} seconds before the environment simulation"
    )
    time.sleep(wait_time)

    # Create the railsim env wrapper -> reset() is also called at this point
    railsim_env = RailsimSemiMdp(
        port=free_port,
        depth_obs_tree=2,
        step_output_queue=step_output_queue,
        action_queue=action_queue,
    )

    return railsim_env


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

    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

    register_env("env", lambda config: create_env(config))

    base_config = (
        get_trainable_cls(args.algo)
        .get_default_config()
        .environment("env")
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
