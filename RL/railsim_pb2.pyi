from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Observation(_message.Message):
    __slots__ = ("obsTree", "trainState", "positionNextNode")
    OBSTREE_FIELD_NUMBER: _ClassVar[int]
    TRAINSTATE_FIELD_NUMBER: _ClassVar[int]
    POSITIONNEXTNODE_FIELD_NUMBER: _ClassVar[int]
    obsTree: _containers.RepeatedScalarFieldContainer[float]
    trainState: _containers.RepeatedScalarFieldContainer[float]
    positionNextNode: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, obsTree: _Optional[_Iterable[float]] = ..., trainState: _Optional[_Iterable[float]] = ..., positionNextNode: _Optional[_Iterable[float]] = ...) -> None: ...

class StepOutput(_message.Message):
    __slots__ = ("observation", "reward", "terminated", "truncated", "info")
    class InfoEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    OBSERVATION_FIELD_NUMBER: _ClassVar[int]
    REWARD_FIELD_NUMBER: _ClassVar[int]
    TERMINATED_FIELD_NUMBER: _ClassVar[int]
    TRUNCATED_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    observation: Observation
    reward: float
    terminated: bool
    truncated: bool
    info: _containers.ScalarMap[str, str]
    def __init__(self, observation: _Optional[_Union[Observation, _Mapping]] = ..., reward: _Optional[float] = ..., terminated: bool = ..., truncated: bool = ..., info: _Optional[_Mapping[str, str]] = ...) -> None: ...

class ResetOutput(_message.Message):
    __slots__ = ("obs", "info")
    class InfoEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    OBS_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    obs: Observation
    info: _containers.ScalarMap[str, str]
    def __init__(self, obs: _Optional[_Union[Observation, _Mapping]] = ..., info: _Optional[_Mapping[str, str]] = ...) -> None: ...

class StepOutputMap(_message.Message):
    __slots__ = ("dictStepOutput",)
    class DictStepOutputEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: StepOutput
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[StepOutput, _Mapping]] = ...) -> None: ...
    DICTSTEPOUTPUT_FIELD_NUMBER: _ClassVar[int]
    dictStepOutput: _containers.MessageMap[str, StepOutput]
    def __init__(self, dictStepOutput: _Optional[_Mapping[str, StepOutput]] = ...) -> None: ...

class ResetOutputMap(_message.Message):
    __slots__ = ("dictResetOutput",)
    class DictResetOutputEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ResetOutput
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ResetOutput, _Mapping]] = ...) -> None: ...
    DICTRESETOUTPUT_FIELD_NUMBER: _ClassVar[int]
    dictResetOutput: _containers.MessageMap[str, ResetOutput]
    def __init__(self, dictResetOutput: _Optional[_Mapping[str, ResetOutput]] = ...) -> None: ...

class ActionMap(_message.Message):
    __slots__ = ("dictAction",)
    class DictActionEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    DICTACTION_FIELD_NUMBER: _ClassVar[int]
    dictAction: _containers.ScalarMap[str, int]
    def __init__(self, dictAction: _Optional[_Mapping[str, int]] = ...) -> None: ...

class ObservationMap(_message.Message):
    __slots__ = ("dictObservation",)
    class DictObservationEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Observation
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Observation, _Mapping]] = ...) -> None: ...
    DICTOBSERVATION_FIELD_NUMBER: _ClassVar[int]
    dictObservation: _containers.MessageMap[str, Observation]
    def __init__(self, dictObservation: _Optional[_Mapping[str, Observation]] = ...) -> None: ...

class String(_message.Message):
    __slots__ = ("msg",)
    MSG_FIELD_NUMBER: _ClassVar[int]
    msg: String
    def __init__(self, msg: _Optional[_Union[String, _Mapping]] = ...) -> None: ...
