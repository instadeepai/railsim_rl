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

class ConfirmationResponse(_message.Message):
    __slots__ = ("ack",)
    ACK_FIELD_NUMBER: _ClassVar[int]
    ack: str
    def __init__(self, ack: _Optional[str] = ...) -> None: ...

class GrpcPort(_message.Message):
    __slots__ = ("grpcPort",)
    GRPCPORT_FIELD_NUMBER: _ClassVar[int]
    grpcPort: int
    def __init__(self, grpcPort: _Optional[int] = ...) -> None: ...
