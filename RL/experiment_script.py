import argparse

# from collections import Counter
# import gymnasium as gym
# from gymnasium.spaces import Box, Discrete, MultiDiscrete, MultiBinary
# from gymnasium.spaces import Dict as GymDict
# from gymnasium.spaces import Tuple as GymTuple
# import inspect
import logging

# import numpy as np
import os
import re
from typing import (
    TYPE_CHECKING,
    Dict,
    Optional,
    Union,
)
import ray
from ray import air, tune
from ray.air.integrations.wandb import WandbLoggerCallback
from ray.rllib.utils.framework import try_import_torch

# from ray.rllib.utils.metrics import (
#     DIFF_NUM_GRAD_UPDATES_VS_SAMPLER_POLICY,
#     NUM_ENV_STEPS_SAMPLED,
#     NUM_ENV_STEPS_TRAINED,
# )
# from ray.rllib.utils.nested_dict import NestedDict
from ray.rllib.utils.typing import ResultDict

# from ray.rllib.utils.error import UnsupportedSpaceException


from ray.tune import CLIReporter


if TYPE_CHECKING:
    from ray.rllib.algorithms import AlgorithmConfig

    # from ray.rllib.offline.dataset_reader import DatasetReader


torch, _ = try_import_torch()

logger = logging.getLogger(__name__)


def add_rllib_example_script_args(
    parser: Optional[argparse.ArgumentParser] = None,
    default_reward: float = 100.0,
    default_iters: int = 200,
    default_timesteps: int = 100000,
) -> argparse.ArgumentParser:
    """Adds RLlib-typical (and common) examples scripts command line args to a parser.

    TODO (sven): This function should be used by most of our examples scripts, which
     already mostly have this logic in them (but written out).

    Args:
        parser: The parser to add the arguments to. If None, create a new one.
        default_reward: The default value for the --stop-reward option.
        default_iters: The default value for the --stop-iters option.
        default_timesteps: The default value for the --stop-timesteps option.

    Returns:
        The altered (or newly created) parser object.
    """
    if parser is None:
        parser = argparse.ArgumentParser()

    # Algo and Algo config options.
    parser.add_argument(
        "--algo", type=str, default="PPO", help="The RLlib-registered algorithm to use."
    )
    parser.add_argument(
        "--enable-new-api-stack",
        action="store_true",
        help="Whether to use the _enable_new_api_stack config setting.",
    )
    parser.add_argument(
        "--framework",
        choices=["tf", "tf2", "torch"],
        default="torch",
        help="The DL framework specifier.",
    )
    parser.add_argument(
        "--num-env-runners",
        type=int,
        default=2,
        help="The number of (remote) EnvRunners to use for the experiment.",
    )
    parser.add_argument(
        "--num-agents",
        type=int,
        default=0,
        help="If 0 (default), will run as single-agent. If > 0, will run as "
        "multi-agent with the environment simply cloned n times and each agent acting "
        "independently at every single timestep. The overall reward for this "
        "experiment is then the sum over all individual agents' rewards.",
    )

    # tune.Tuner options.
    parser.add_argument(
        "--no-tune",
        action="store_true",
        help="Whether to NOT use tune.Tuner(), but rather a simple for-loop calling "
        "`algo.train()` repeatedly until one of the stop criteria is met.",
    )
    parser.add_argument(
        "--num-samples",
        type=int,
        default=1,
        help="How many (tune.Tuner.fit()) experiments to execute - if possible in "
        "parallel.",
    )
    parser.add_argument(
        "--verbose",
        type=int,
        default=2,
        help="The verbosity level for the `tune.Tuner()` running the experiment.",
    )
    parser.add_argument(
        "--checkpoint-freq",
        type=int,
        default=0,
        help=(
            "The frequency (in training iterations) with which to create checkpoints. "
            "Note that if --wandb-key is provided, all checkpoints will "
            "automatically be uploaded to WandB."
        ),
    )
    parser.add_argument(
        "--checkpoint-at-end",
        action="store_true",
        help=(
            "Whether to create a checkpoint at the very end of the experiment. "
            "Note that if --wandb-key is provided, all checkpoints will "
            "automatically be uploaded to WandB."
        ),
    )

    # WandB logging options.
    parser.add_argument(
        "--wandb-key",
        type=str,
        default=None,
        help="The WandB API key to use for uploading results.",
    )
    parser.add_argument(
        "--wandb-project",
        type=str,
        default=None,
        help="The WandB project name to use.",
    )
    parser.add_argument(
        "--wandb-run-name",
        type=str,
        default=None,
        help="The WandB run name to use.",
    )

    # Experiment stopping and testing criteria.
    parser.add_argument(
        "--stop-reward",
        type=float,
        default=default_reward,
        help="Reward at which the script should stop training.",
    )
    parser.add_argument(
        "--stop-iters",
        type=int,
        default=default_iters,
        help="The number of iterations to train.",
    )
    parser.add_argument(
        "--stop-timesteps",
        type=int,
        default=default_timesteps,
        help="The number of (environment sampling) timesteps to train.",
    )
    parser.add_argument(
        "--as-test",
        action="store_true",
        help="Whether this script should be run as a test. If set, --stop-reward must "
        "be achieved within --stop-timesteps AND --stop-iters, otherwise this "
        "script will throw an exception at the end.",
    )

    # Learner scaling options.
    # Old API stack: config.num_gpus.
    # New API stack: config.num_learner_workers (w/ num_gpus_per_learner_worker=1).
    parser.add_argument("--num-gpus", type=int, default=0)

    # Ray init options.
    parser.add_argument("--num-cpus", type=int, default=0)
    parser.add_argument(
        "--local-mode",
        action="store_true",
        help="Init Ray in local mode for easier debugging.",
    )
    return parser


def run_rllib_example_script_experiment(
    base_config: "AlgorithmConfig",
    args: argparse.Namespace,
    *,
    stop: Optional[Dict] = None,
    success_metric: str = "sampler_results/episode_reward_mean",
) -> Union[ResultDict, tune.result_grid.ResultGrid]:
    """Given an algorithm config and some command line args, runs an experiment.

    There are some constraints on what properties must be defined in `args`.
    It should ideally be generated via the ``

    Args:
        base_config: The AlgorithmConfig object to use for this experiment. This base
            config will be automatically "extended" based on some of the provided
            `args`. For example, `args.num_env_runners` is used to set
            `config.num_rollout_workers`, etc..
        args: A argparse.Namespace object which must have the following properties
            defined: `stop_iters`, `stop_reward`, `stop_timesteps`, `no_tune`,
            `verbose`, `checkpoint_freq`, `as_test`. Optionally, for wandb logging:
            `wandb_key`, `wandb_project`, `wandb_run_name`.

    Returns:
        The last ResultDict from a --no-tune run OR the tune.Tuner.fit()
        results.
    """
    ray.init(num_cpus=args.num_cpus or None, local_mode=args.local_mode)

    stop = stop or {
        "training_iteration": args.stop_iters,
        "sampler_results/episode_reward_mean": args.stop_reward,
        "timesteps_total": args.stop_timesteps,
    }

    from ray.rllib.env.multi_agent_env_runner import MultiAgentEnvRunner
    from ray.rllib.env.single_agent_env_runner import SingleAgentEnvRunner

    # Extend the `base_config` based on provided `args`.
    config = (
        base_config.framework(args.framework)
        .experimental(_enable_new_api_stack=args.enable_new_api_stack)
        .rollouts(
            num_rollout_workers=args.num_env_runners,
            # Set up the correct env-runner to use depending on
            # old-stack/new-stack and multi-agent settings.
            env_runner_cls=(
                None
                if not args.enable_new_api_stack
                else (
                    SingleAgentEnvRunner
                    if args.num_agents == 0
                    else MultiAgentEnvRunner
                )
            ),
        )
        .resources(
            # Old stack.
            num_gpus=0 if args.enable_new_api_stack else args.num_gpus,
            # New stack.
            num_learner_workers=args.num_gpus,
            num_gpus_per_learner_worker=1 if torch.cuda.is_available() else 0,
            num_cpus_for_local_worker=1,
        )
    )

    if args.no_tune:
        algo = config.build()
        for iter in range(args.stop_iters):
            results = algo.train()
            # print(f"R={results['sampler_results']['episode_reward_mean']}", end="")
            print(
                f"policy loss: {results['learner_results']['p0']['policy_loss']}, value loss: {results['learner_results']['p0']['vf_loss']}"
            )
            if "evaluation" in results:
                Reval = results["evaluation"]["sampler_results"]["episode_reward_mean"]
                print(f" R(eval)={Reval}", end="")
            print()
            for key, value in stop.items():
                val = results
                for k in key.split("/"):
                    try:
                        val = val[k]
                    except KeyError:
                        val = None
                        break
                if val is not None and val >= value:
                    print(f"Stop criterium ({key}={value}) fulfilled!")
                    return results
        return results

    callbacks = None
    if hasattr(args, "wandb_key") and args.wandb_key is not None:
        project = args.wandb_project or (
            args.algo.lower() + "-" + re.sub("\\W+", "-", str(config.env).lower())
        )
        callbacks = [
            WandbLoggerCallback(
                api_key=args.wandb_key,
                project=project,
                upload_checkpoints=True,
                **({"name": args.wandb_run_name} if args.wandb_run_name else {}),
            )
        ]

    progress_reporter = None
    # Use better ProgressReporter for multi-agent cases: List individual policy rewards.
    if args.num_agents > 0:
        progress_reporter = CLIReporter(
            metric_columns={
                **{
                    "training_iteration": "iter",
                    "time_total_s": "total time (s)",
                    "timesteps_total": "ts",
                    "sampler_results/episode_reward_mean": "combined reward",
                },
                **{
                    f"policy_reward_mean/{pid}": f"reward {pid}"
                    for pid in config.policies
                },
            },
        )

    # Force Tuner to use old progress output as the new one silently ignores our custom
    # `CLIReporter`.
    os.environ["RAY_AIR_NEW_OUTPUT"] = "0"

    results = tune.Tuner(
        config.algo_class,
        param_space=config,
        run_config=air.RunConfig(
            stop=stop,
            verbose=args.verbose,
            callbacks=callbacks,
            checkpoint_config=air.CheckpointConfig(
                checkpoint_frequency=args.checkpoint_freq,
                checkpoint_at_end=args.checkpoint_at_end,
            ),
            progress_reporter=progress_reporter,
        ),
        tune_config=tune.TuneConfig(num_samples=args.num_samples),
    ).fit()

    if args.as_test:
        check_learning_achieved(
            results,
            args.stop_reward,
            metric=success_metric,
        )

    return results


def check_learning_achieved(
    tune_results: "tune.ResultGrid",
    min_value: float,
    evaluation: Optional[bool] = None,
    metric: str = "sampler_results/episode_reward_mean",
):
    """Throws an error if `min_reward` is not reached within tune_results.

    Checks the last iteration found in tune_results for its
    "episode_reward_mean" value and compares it to `min_reward`.

    Args:
        tune_results: The tune.Tuner().fit() returned results object.
        min_reward: The min reward that must be reached.
        evaluation: If True, use `evaluation/sampler_results/[metric]`, if False, use
            `sampler_results/[metric]`, if None, use evaluation sampler results if
            available otherwise, use train sampler results.

    Raises:
        ValueError: If `min_reward` not reached.
    """
    # Get maximum reward of all trials
    # (check if at least one trial achieved some learning)
    recorded_values = []
    for _, row in tune_results.get_dataframe().iterrows():
        if evaluation or (evaluation is None and f"evaluation/{metric}" in row):
            recorded_values.append(row[f"evaluation/{metric}"])
        else:
            recorded_values.append(row[metric])
    best_value = max(recorded_values)
    if best_value < min_value:
        raise ValueError(f"`{metric}` of {min_value} not reached!")
    print(f"`{metric}` of {min_value} reached! ok")
