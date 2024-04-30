import os

import ray
from ray import tune
from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.env.wrappers.pettingzoo_env import ParallelPettingZooEnv
# from ray.rllib.models import ModelCatalog
# from ray.rllib.models.torch.torch_modelv2 import TorchModelV2
from ray.tune.registry import register_env
from torch import nn
from env_wrapper.railsim import Railsim


def env_creator(args):
    env = ParallelPettingZooEnv(Railsim(
        jar_path="/Users/akashsinha/Documents/railsim_rl/DummyEnv/target/DummyEnv-1.0-SNAPSHOT.jar",
        num_agents=3,
        depth_obs_tree=2,
    ))

    return env


if __name__ == "__main__":
    ray.init()

    env_name = "railsim"

    register_env(env_name, lambda config: env_creator(config))

    config = (
        PPOConfig()
        .environment(env=env_name, clip_actions=True)
        .rollouts(num_rollout_workers=0, rollout_fragment_length=128)
        .training(
            train_batch_size=512,
            lr=2e-5,
            gamma=0.99,
            lambda_=0.9,
            use_gae=True,
            clip_param=0.4,
            grad_clip=None,
            entropy_coeff=0.1,
            vf_loss_coeff=0.25,
            sgd_minibatch_size=64,
            num_sgd_iter=10,
        )
        .debugging(log_level="ERROR")
        .framework(framework="torch")
        .resources(num_gpus=int(os.environ.get("RLLIB_NUM_GPUS", "0")))
    )


    tune.run(
        "PPO",
        name="PPO",
        stop={"timesteps_total": 5000000 if not os.environ.get("CI") else 50000},
        checkpoint_freq=100,
        local_dir="~/ray_results/" + env_name,
        config=config.to_dict(),
    )
