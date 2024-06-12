from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProtoObservation(_message.Message):
    __slots__ = ("obsTree", "trainState", "positionNextNode", "timestamp")
    OBSTREE_FIELD_NUMBER: _ClassVar[int]
    TRAINSTATE_FIELD_NUMBER: _ClassVar[int]
    POSITIONNEXTNODE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    obsTree: _containers.RepeatedScalarFieldContainer[float]
    trainState: _containers.RepeatedScalarFieldContainer[float]
    positionNextNode: _containers.RepeatedScalarFieldContainer[float]
    timestamp: float
    def __init__(self, obsTree: _Optional[_Iterable[float]] = ..., trainState: _Optional[_Iterable[float]] = ..., positionNextNode: _Optional[_Iterable[float]] = ..., timestamp: _Optional[float] = ...) -> None: ...

class ProtoStepOutput(_message.Message):
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
    observation: ProtoObservation
    reward: float
    terminated: bool
    truncated: bool
    info: _containers.ScalarMap[str, str]
    def __init__(self, observation: _Optional[_Union[ProtoObservation, _Mapping]] = ..., reward: _Optional[float] = ..., terminated: bool = ..., truncated: bool = ..., info: _Optional[_Mapping[str, str]] = ...) -> None: ...

class ProtoStepOutputMap(_message.Message):
    __slots__ = ("dictStepOutput",)
    class DictStepOutputEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ProtoStepOutput
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ProtoStepOutput, _Mapping]] = ...) -> None: ...
    DICTSTEPOUTPUT_FIELD_NUMBER: _ClassVar[int]
    dictStepOutput: _containers.MessageMap[str, ProtoStepOutput]
    def __init__(self, dictStepOutput: _Optional[_Mapping[str, ProtoStepOutput]] = ...) -> None: ...

class ProtoAgentIDs(_message.Message):
    __slots__ = ("agentId",)
    AGENTID_FIELD_NUMBER: _ClassVar[int]
    agentId: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, agentId: _Optional[_Iterable[str]] = ...) -> None: ...

class ProtoActionMap(_message.Message):
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

class ProtoObservationMap(_message.Message):
    __slots__ = ("dictObservation",)
    class DictObservationEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ProtoObservation
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ProtoObservation, _Mapping]] = ...) -> None: ...
    DICTOBSERVATION_FIELD_NUMBER: _ClassVar[int]
    dictObservation: _containers.MessageMap[str, ProtoObservation]
    def __init__(self, dictObservation: _Optional[_Mapping[str, ProtoObservation]] = ...) -> None: ...

class ProtoConfirmationResponse(_message.Message):
    __slots__ = ("ack",)
    ACK_FIELD_NUMBER: _ClassVar[int]
    ack: str
    def __init__(self, ack: _Optional[str] = ...) -> None: ...

class ProtoGetActionRequest(_message.Message):
    __slots__ = ("timestamp", "trainId")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TRAINID_FIELD_NUMBER: _ClassVar[int]
    timestamp: float
    trainId: str
    def __init__(self, timestamp: _Optional[float] = ..., trainId: _Optional[str] = ...) -> None: ...

class ProtoGrpcPort(_message.Message):
    __slots__ = ("grpcPort",)
    GRPCPORT_FIELD_NUMBER: _ClassVar[int]
    grpcPort: int
    def __init__(self, grpcPort: _Optional[int] = ...) -> None: ...
