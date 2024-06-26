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


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rrailsim.proto\x1a\x1bgoogle/protobuf/empty.proto\"d\n\x10ProtoObservation\x12\x0f\n\x07obsTree\x18\x01 \x03(\x01\x12\x12\n\ntrainState\x18\x02 \x03(\x01\x12\x18\n\x10positionNextNode\x18\x03 \x03(\x01\x12\x11\n\ttimestamp\x18\x04 \x01(\x01\"\xc7\x01\n\x0fProtoStepOutput\x12&\n\x0bobservation\x18\x01 \x01(\x0b\x32\x11.ProtoObservation\x12\x0e\n\x06reward\x18\x02 \x01(\x01\x12\x12\n\nterminated\x18\x03 \x01(\x08\x12\x11\n\ttruncated\x18\x04 \x01(\x08\x12(\n\x04info\x18\x05 \x03(\x0b\x32\x1a.ProtoStepOutput.InfoEntry\x1a+\n\tInfoEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x9e\x01\n\x12ProtoStepOutputMap\x12?\n\x0e\x64ictStepOutput\x18\x01 \x03(\x0b\x32\'.ProtoStepOutputMap.DictStepOutputEntry\x1aG\n\x13\x44ictStepOutputEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x1f\n\x05value\x18\x02 \x01(\x0b\x32\x10.ProtoStepOutput:\x02\x38\x01\" \n\rProtoAgentIDs\x12\x0f\n\x07\x61gentId\x18\x01 \x03(\t\"x\n\x0eProtoActionMap\x12\x33\n\ndictAction\x18\x01 \x03(\x0b\x32\x1f.ProtoActionMap.DictActionEntry\x1a\x31\n\x0f\x44ictActionEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\"\xa4\x01\n\x13ProtoObservationMap\x12\x42\n\x0f\x64ictObservation\x18\x01 \x03(\x0b\x32).ProtoObservationMap.DictObservationEntry\x1aI\n\x14\x44ictObservationEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12 \n\x05value\x18\x02 \x01(\x0b\x32\x11.ProtoObservation:\x02\x38\x01\"(\n\x19ProtoConfirmationResponse\x12\x0b\n\x03\x61\x63k\x18\x01 \x01(\t\";\n\x15ProtoGetActionRequest\x12\x11\n\ttimestamp\x18\x01 \x01(\x01\x12\x0f\n\x07trainId\x18\x02 \x01(\t\"!\n\rProtoGrpcPort\x12\x10\n\x08grpcPort\x18\x01 \x01(\x05\x32\x8c\x01\n\x10RailsimConnecter\x12\x36\n\tgetAction\x12\x16.ProtoGetActionRequest\x1a\x0f.ProtoActionMap\"\x00\x12@\n\x0bupdateState\x12\x13.ProtoStepOutputMap\x1a\x1a.ProtoConfirmationResponse\"\x00\x32\xaf\x01\n\x0eRailsimFactory\x12>\n\x0egetEnvironment\x12\x0e.ProtoGrpcPort\x1a\x1a.ProtoConfirmationResponse\"\x00\x12,\n\x08resetEnv\x12\x0e.ProtoGrpcPort\x1a\x0e.ProtoAgentIDs\"\x00\x12/\n\x0bgetAgentIds\x12\x0e.ProtoGrpcPort\x1a\x0e.ProtoAgentIDs\"\x00\x42&\n\"ch.sbb.matsim.contrib.railsim.grpcP\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'railsim_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\"ch.sbb.matsim.contrib.railsim.grpcP\001'
  _globals['_PROTOSTEPOUTPUT_INFOENTRY']._options = None
  _globals['_PROTOSTEPOUTPUT_INFOENTRY']._serialized_options = b'8\001'
  _globals['_PROTOSTEPOUTPUTMAP_DICTSTEPOUTPUTENTRY']._options = None
  _globals['_PROTOSTEPOUTPUTMAP_DICTSTEPOUTPUTENTRY']._serialized_options = b'8\001'
  _globals['_PROTOACTIONMAP_DICTACTIONENTRY']._options = None
  _globals['_PROTOACTIONMAP_DICTACTIONENTRY']._serialized_options = b'8\001'
  _globals['_PROTOOBSERVATIONMAP_DICTOBSERVATIONENTRY']._options = None
  _globals['_PROTOOBSERVATIONMAP_DICTOBSERVATIONENTRY']._serialized_options = b'8\001'
  _globals['_PROTOOBSERVATION']._serialized_start=46
  _globals['_PROTOOBSERVATION']._serialized_end=146
  _globals['_PROTOSTEPOUTPUT']._serialized_start=149
  _globals['_PROTOSTEPOUTPUT']._serialized_end=348
  _globals['_PROTOSTEPOUTPUT_INFOENTRY']._serialized_start=305
  _globals['_PROTOSTEPOUTPUT_INFOENTRY']._serialized_end=348
  _globals['_PROTOSTEPOUTPUTMAP']._serialized_start=351
  _globals['_PROTOSTEPOUTPUTMAP']._serialized_end=509
  _globals['_PROTOSTEPOUTPUTMAP_DICTSTEPOUTPUTENTRY']._serialized_start=438
  _globals['_PROTOSTEPOUTPUTMAP_DICTSTEPOUTPUTENTRY']._serialized_end=509
  _globals['_PROTOAGENTIDS']._serialized_start=511
  _globals['_PROTOAGENTIDS']._serialized_end=543
  _globals['_PROTOACTIONMAP']._serialized_start=545
  _globals['_PROTOACTIONMAP']._serialized_end=665
  _globals['_PROTOACTIONMAP_DICTACTIONENTRY']._serialized_start=616
  _globals['_PROTOACTIONMAP_DICTACTIONENTRY']._serialized_end=665
  _globals['_PROTOOBSERVATIONMAP']._serialized_start=668
  _globals['_PROTOOBSERVATIONMAP']._serialized_end=832
  _globals['_PROTOOBSERVATIONMAP_DICTOBSERVATIONENTRY']._serialized_start=759
  _globals['_PROTOOBSERVATIONMAP_DICTOBSERVATIONENTRY']._serialized_end=832
  _globals['_PROTOCONFIRMATIONRESPONSE']._serialized_start=834
  _globals['_PROTOCONFIRMATIONRESPONSE']._serialized_end=874
  _globals['_PROTOGETACTIONREQUEST']._serialized_start=876
  _globals['_PROTOGETACTIONREQUEST']._serialized_end=935
  _globals['_PROTOGRPCPORT']._serialized_start=937
  _globals['_PROTOGRPCPORT']._serialized_end=970
  _globals['_RAILSIMCONNECTER']._serialized_start=973
  _globals['_RAILSIMCONNECTER']._serialized_end=1113
  _globals['_RAILSIMFACTORY']._serialized_start=1116
  _globals['_RAILSIMFACTORY']._serialized_end=1291
# @@protoc_insertion_point(module_scope)
