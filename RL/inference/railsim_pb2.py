# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: railsim.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\rrailsim.proto"L\n\x0bObservation\x12\x0f\n\x07obsTree\x18\x01 \x03(\x01\x12\x12\n\ntrainState\x18\x02 \x03(\x01\x12\x18\n\x10positionNextNode\x18\x03 \x03(\x01"\xb8\x01\n\nStepOutput\x12!\n\x0bobservation\x18\x01 \x01(\x0b\x32\x0c.Observation\x12\x0e\n\x06reward\x18\x02 \x01(\x01\x12\x12\n\nterminated\x18\x03 \x01(\x08\x12\x11\n\ttruncated\x18\x04 \x01(\x08\x12#\n\x04info\x18\x05 \x03(\x0b\x32\x15.StepOutput.InfoEntry\x1a+\n\tInfoEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01"{\n\x0bResetOutput\x12\x19\n\x03obs\x18\x01 \x01(\x0b\x32\x0c.Observation\x12$\n\x04info\x18\x02 \x03(\x0b\x32\x16.ResetOutput.InfoEntry\x1a+\n\tInfoEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01"\x8f\x01\n\rStepOutputMap\x12:\n\x0e\x64ictStepOutput\x18\x01 \x03(\x0b\x32".StepOutputMap.DictStepOutputEntry\x1a\x42\n\x13\x44ictStepOutputEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1a\n\x05value\x18\x02 \x01(\x0b\x32\x0b.StepOutput:\x02\x38\x01"\x95\x01\n\x0eResetOutputMap\x12=\n\x0f\x64ictResetOutput\x18\x01 \x03(\x0b\x32$.ResetOutputMap.DictResetOutputEntry\x1a\x44\n\x14\x44ictResetOutputEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1b\n\x05value\x18\x02 \x01(\x0b\x32\x0c.ResetOutput:\x02\x38\x01"n\n\tActionMap\x12.\n\ndictAction\x18\x01 \x03(\x0b\x32\x1a.ActionMap.DictActionEntry\x1a\x31\n\x0f\x44ictActionEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01"\x95\x01\n\x0eObservationMap\x12=\n\x0f\x64ictObservation\x18\x01 \x03(\x0b\x32$.ObservationMap.DictObservationEntry\x1a\x44\n\x14\x44ictObservationEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1b\n\x05value\x18\x02 \x01(\x0b\x32\x0c.Observation:\x02\x38\x01"\x1e\n\x06String\x12\x14\n\x03msg\x18\x01 \x01(\x0b\x32\x07.String2>\n\x10RailsimConnecter\x12*\n\tgetAction\x12\x0f.ObservationMap\x1a\n.ActionMap"\x00\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "railsim_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals["_STEPOUTPUT_INFOENTRY"]._options = None
    _globals["_STEPOUTPUT_INFOENTRY"]._serialized_options = b"8\001"
    _globals["_RESETOUTPUT_INFOENTRY"]._options = None
    _globals["_RESETOUTPUT_INFOENTRY"]._serialized_options = b"8\001"
    _globals["_STEPOUTPUTMAP_DICTSTEPOUTPUTENTRY"]._options = None
    _globals["_STEPOUTPUTMAP_DICTSTEPOUTPUTENTRY"]._serialized_options = b"8\001"
    _globals["_RESETOUTPUTMAP_DICTRESETOUTPUTENTRY"]._options = None
    _globals["_RESETOUTPUTMAP_DICTRESETOUTPUTENTRY"]._serialized_options = b"8\001"
    _globals["_ACTIONMAP_DICTACTIONENTRY"]._options = None
    _globals["_ACTIONMAP_DICTACTIONENTRY"]._serialized_options = b"8\001"
    _globals["_OBSERVATIONMAP_DICTOBSERVATIONENTRY"]._options = None
    _globals["_OBSERVATIONMAP_DICTOBSERVATIONENTRY"]._serialized_options = b"8\001"
    _globals["_OBSERVATION"]._serialized_start = 17
    _globals["_OBSERVATION"]._serialized_end = 93
    _globals["_STEPOUTPUT"]._serialized_start = 96
    _globals["_STEPOUTPUT"]._serialized_end = 280
    _globals["_STEPOUTPUT_INFOENTRY"]._serialized_start = 237
    _globals["_STEPOUTPUT_INFOENTRY"]._serialized_end = 280
    _globals["_RESETOUTPUT"]._serialized_start = 282
    _globals["_RESETOUTPUT"]._serialized_end = 405
    _globals["_RESETOUTPUT_INFOENTRY"]._serialized_start = 237
    _globals["_RESETOUTPUT_INFOENTRY"]._serialized_end = 280
    _globals["_STEPOUTPUTMAP"]._serialized_start = 408
    _globals["_STEPOUTPUTMAP"]._serialized_end = 551
    _globals["_STEPOUTPUTMAP_DICTSTEPOUTPUTENTRY"]._serialized_start = 485
    _globals["_STEPOUTPUTMAP_DICTSTEPOUTPUTENTRY"]._serialized_end = 551
    _globals["_RESETOUTPUTMAP"]._serialized_start = 554
    _globals["_RESETOUTPUTMAP"]._serialized_end = 703
    _globals["_RESETOUTPUTMAP_DICTRESETOUTPUTENTRY"]._serialized_start = 635
    _globals["_RESETOUTPUTMAP_DICTRESETOUTPUTENTRY"]._serialized_end = 703
    _globals["_ACTIONMAP"]._serialized_start = 705
    _globals["_ACTIONMAP"]._serialized_end = 815
    _globals["_ACTIONMAP_DICTACTIONENTRY"]._serialized_start = 766
    _globals["_ACTIONMAP_DICTACTIONENTRY"]._serialized_end = 815
    _globals["_OBSERVATIONMAP"]._serialized_start = 818
    _globals["_OBSERVATIONMAP"]._serialized_end = 967
    _globals["_OBSERVATIONMAP_DICTOBSERVATIONENTRY"]._serialized_start = 899
    _globals["_OBSERVATIONMAP_DICTOBSERVATIONENTRY"]._serialized_end = 967
    _globals["_STRING"]._serialized_start = 969
    _globals["_STRING"]._serialized_end = 999
    _globals["_RAILSIMCONNECTER"]._serialized_start = 1001
    _globals["_RAILSIMCONNECTER"]._serialized_end = 1063
# @@protoc_insertion_point(module_scope)
