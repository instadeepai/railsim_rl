from collections import namedtuple


StepOutput = namedtuple(
    "StepOutput", ["observation_d", "reward_d", "terminated_d", "truncated_d", "info_d"]
)