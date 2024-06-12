from collections import namedtuple

StepOutput = namedtuple(
    "StepOutput", ["timestamp", "observation_d", "reward_d", "terminated_d", "truncated_d", "info_d"]
)
