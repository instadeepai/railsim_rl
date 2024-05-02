# import os

# import ray
from env_wrapper.railsim import Railsim
from ray.rllib.core.rl_module.marl_module import MultiAgentRLModuleSpec
from ray.rllib.core.rl_module.rl_module import SingleAgentRLModuleSpec

# from ray import tune
# from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.env.wrappers.pettingzoo_env import ParallelPettingZooEnv

# from ray.rllib.models import ModelCatalog
# from ray.rllib.models.torch.torch_modelv2 import TorchModelV2
from ray.tune.registry import get_trainable_cls, register_env

from RL.experiment_script import (
    add_rllib_example_script_args,
    run_rllib_example_script_experiment,
)


def env_creator(args):
    env = ParallelPettingZooEnv(
        Railsim(
            jar_path="/Users/akashsinha/Documents/railsim_rl/DummyEnv/"
            "target/DummyEnv-1.0-SNAPSHOT.jar",
            num_agents=3,
            depth_obs_tree=2,
        )
    )

    return env


# if __name__ == "__main__":
#     ray.init()

#     env_name = "railsim"

#     register_env(env_name, lambda config: env_creator(config))

#     config = (
#         PPOConfig()
#         .environment(env=env_name, clip_actions=True)
#         .rollouts(num_rollout_workers=0, rollout_fragment_length=128)
#         .training(
#             train_batch_size=512,
#             lr=2e-5,
#             gamma=0.99,
#             lambda_=0.9,
#             use_gae=True,
#             clip_param=0.4,
#             grad_clip=None,
#             entropy_coeff=0.1,
#             vf_loss_coeff=0.25,
#             sgd_minibatch_size=64,
#             num_sgd_iter=10,
#         )
#         .debugging(log_level="ERROR")
#         .framework(framework="torch")
#         .resources(num_gpus=int(os.environ.get("RLLIB_NUM_GPUS", "0")))
#         .multi_agent(
#             policies={"p0"},
#             # All agents map to the exact same policy.
#             policy_mapping_fn=(lambda aid, *args, **kwargs: "p0"),
#         )
#         .rl_module(
#             rl_module_spec=MultiAgentRLModuleSpec(
#                 module_specs={"p0": SingleAgentRLModuleSpec()},
#             ),
#         )
#     )

#     tune.run(
#         "PPO",
#         name="PPO",
#         stop={"timesteps_total": 5000000 if not os.environ.get("CI") else 50000},
#         checkpoint_freq=2,
#         local_dir="~/Documents/ray_results/" + env_name,
#         config=config.to_dict(),
#     )


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

    register_env("env", lambda config: env_creator(config))

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
        )
        .rl_module(
            rl_module_spec=MultiAgentRLModuleSpec(
                module_specs={"p0": SingleAgentRLModuleSpec()},
            ),
        )
    )

    run_rllib_example_script_experiment(base_config, args)
