# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: raft.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='raft.proto',
  package='grpc',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\nraft.proto\x12\x04grpc\"\x11\n\x03\x41\x63k\x12\n\n\x02id\x18\x01 \x01(\x03\"\x81\x01\n\x08TableLog\x12\x10\n\x08\x66ileName\x18\x01 \x01(\t\x12\x0f\n\x07\x63hunkId\x18\x02 \x01(\x03\x12\n\n\x02ip\x18\x03 \x01(\t\x12\x0c\n\x04port\x18\x04 \x01(\t\x12\x11\n\tlog_index\x18\x05 \x01(\x03\x12%\n\toperation\x18\x06 \x01(\x0e\x32\x12.grpc.LogOperation\"g\n\x05Table\x12\x14\n\x0c\x63ycle_number\x18\x01 \x01(\x03\x12\x11\n\tleader_ip\x18\x02 \x01(\t\x12\x13\n\x0bleader_port\x18\x03 \x01(\t\x12 \n\x08tableLog\x18\x04 \x03(\x0b\x32\x0e.grpc.TableLog\"O\n\tCandidacy\x12\x14\n\x0c\x63ycle_number\x18\x01 \x01(\x03\x12\n\n\x02ip\x18\x02 \x01(\t\x12\x0c\n\x04port\x18\x03 \x01(\t\x12\x12\n\nlog_length\x18\x04 \x01(\x03\"D\n\x11\x43\x61ndidacyResponse\x12\x19\n\x05voted\x18\x01 \x01(\x0e\x32\n.grpc.Vote\x12\x14\n\x0c\x63ycle_number\x18\x02 \x01(\x03\"*\n\x0e\x44\x61taCenterInfo\x12\n\n\x02ip\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\t\")\n\rProxyInfoRaft\x12\n\n\x02ip\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\t\"\x07\n\x05\x45mpty\"b\n\x0fReplicationInfo\x12\x10\n\x08\x66ileName\x18\x01 \x01(\t\x12\x0f\n\x07\x63hunkId\x18\x02 \x01(\x03\x12,\n\x0e\x66romDatacenter\x18\x03 \x01(\x0b\x32\x14.grpc.DataCenterInfo\"T\n\x0f\x43hunkUploadInfo\x12\x0f\n\x07\x63hunkId\x18\x01 \x01(\x03\x12\x30\n\x12uploadedDatacenter\x18\x02 \x01(\x0b\x32\x14.grpc.DataCenterInfo\"]\n\x16UploadCompleteFileInfo\x12\x10\n\x08\x66ileName\x18\x01 \x01(\t\x12\x31\n\x12lstChunkUploadInfo\x18\x02 \x03(\x0b\x32\x15.grpc.ChunkUploadInfo\"5\n\x10RequestChunkInfo\x12\x10\n\x08\x66ileName\x18\x01 \x01(\t\x12\x0f\n\x07\x63hunkId\x18\x02 \x01(\x03\"y\n\x11\x43hunkLocationInfo\x12\x10\n\x08\x66ileName\x18\x01 \x01(\t\x12\x0f\n\x07\x63hunkId\x18\x02 \x01(\x03\x12+\n\rlstDataCenter\x18\x03 \x03(\x0b\x32\x14.grpc.DataCenterInfo\x12\x14\n\x0cisChunkFound\x18\x04 \x01(\x08*i\n\x0cLogOperation\x12\x13\n\x0fUploadRequested\x10\x00\x12\x0c\n\x08Uploaded\x10\x01\x12\x0f\n\x0bUploadFaied\x10\x02\x12\x0b\n\x07\x44\x65leted\x10\x03\x12\x18\n\x14TemporaryUnavailable\x10\x04*\x17\n\x04Vote\x12\x07\n\x03YES\x10\x00\x12\x06\n\x02NO\x10\x01*v\n\x10ReplicationState\x12\x16\n\x12ReplicationPending\x10\x00\x12\x18\n\x14ReplicationRequested\x10\x01\x12\x16\n\x12ReplicationStarted\x10\x02\x12\x18\n\x14ReplicationCompleted\x10\x03\x32\xa3\x04\n\x0bRaftService\x12&\n\x0cRaftHeartbit\x12\x0b.grpc.Table\x1a\t.grpc.Ack\x12\x37\n\x0bRequestVote\x12\x0f.grpc.Candidacy\x1a\x17.grpc.CandidacyResponse\x12\'\n\nAddFileLog\x12\x0e.grpc.TableLog\x1a\t.grpc.Ack\x12\x32\n\rAddDataCenter\x12\x14.grpc.DataCenterInfo\x1a\x0b.grpc.Empty\x12/\n\x13\x44\x61taCenterHeartbeat\x12\x0b.grpc.Empty\x1a\x0b.grpc.Empty\x12\x37\n\x13ReplicationInitiate\x12\x15.grpc.ReplicationInfo\x1a\t.grpc.Ack\x12,\n\x08\x41\x64\x64Proxy\x12\x13.grpc.ProxyInfoRaft\x1a\x0b.grpc.Empty\x12*\n\x0eProxyHeartbeat\x12\x0b.grpc.Empty\x1a\x0b.grpc.Empty\x12@\n\x13\x46ileUploadCompleted\x12\x1c.grpc.UploadCompleteFileInfo\x1a\x0b.grpc.Empty\x12P\n\x1dGetDataCenterListForFileChunk\x12\x16.grpc.RequestChunkInfo\x1a\x17.grpc.ChunkLocationInfob\x06proto3')
)

_LOGOPERATION = _descriptor.EnumDescriptor(
  name='LogOperation',
  full_name='grpc.LogOperation',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UploadRequested', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='Uploaded', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UploadFaied', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='Deleted', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TemporaryUnavailable', index=4, number=4,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=982,
  serialized_end=1087,
)
_sym_db.RegisterEnumDescriptor(_LOGOPERATION)

LogOperation = enum_type_wrapper.EnumTypeWrapper(_LOGOPERATION)
_VOTE = _descriptor.EnumDescriptor(
  name='Vote',
  full_name='grpc.Vote',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='YES', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NO', index=1, number=1,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1089,
  serialized_end=1112,
)
_sym_db.RegisterEnumDescriptor(_VOTE)

Vote = enum_type_wrapper.EnumTypeWrapper(_VOTE)
_REPLICATIONSTATE = _descriptor.EnumDescriptor(
  name='ReplicationState',
  full_name='grpc.ReplicationState',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ReplicationPending', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ReplicationRequested', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ReplicationStarted', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ReplicationCompleted', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1114,
  serialized_end=1232,
)
_sym_db.RegisterEnumDescriptor(_REPLICATIONSTATE)

ReplicationState = enum_type_wrapper.EnumTypeWrapper(_REPLICATIONSTATE)
UploadRequested = 0
Uploaded = 1
UploadFaied = 2
Deleted = 3
TemporaryUnavailable = 4
YES = 0
NO = 1
ReplicationPending = 0
ReplicationRequested = 1
ReplicationStarted = 2
ReplicationCompleted = 3



_ACK = _descriptor.Descriptor(
  name='Ack',
  full_name='grpc.Ack',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='grpc.Ack.id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=20,
  serialized_end=37,
)


_TABLELOG = _descriptor.Descriptor(
  name='TableLog',
  full_name='grpc.TableLog',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='fileName', full_name='grpc.TableLog.fileName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='chunkId', full_name='grpc.TableLog.chunkId', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ip', full_name='grpc.TableLog.ip', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='port', full_name='grpc.TableLog.port', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='log_index', full_name='grpc.TableLog.log_index', index=4,
      number=5, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='operation', full_name='grpc.TableLog.operation', index=5,
      number=6, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=40,
  serialized_end=169,
)


_TABLE = _descriptor.Descriptor(
  name='Table',
  full_name='grpc.Table',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cycle_number', full_name='grpc.Table.cycle_number', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='leader_ip', full_name='grpc.Table.leader_ip', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='leader_port', full_name='grpc.Table.leader_port', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tableLog', full_name='grpc.Table.tableLog', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=171,
  serialized_end=274,
)


_CANDIDACY = _descriptor.Descriptor(
  name='Candidacy',
  full_name='grpc.Candidacy',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cycle_number', full_name='grpc.Candidacy.cycle_number', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ip', full_name='grpc.Candidacy.ip', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='port', full_name='grpc.Candidacy.port', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='log_length', full_name='grpc.Candidacy.log_length', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=276,
  serialized_end=355,
)


_CANDIDACYRESPONSE = _descriptor.Descriptor(
  name='CandidacyResponse',
  full_name='grpc.CandidacyResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='voted', full_name='grpc.CandidacyResponse.voted', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cycle_number', full_name='grpc.CandidacyResponse.cycle_number', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=357,
  serialized_end=425,
)


_DATACENTERINFO = _descriptor.Descriptor(
  name='DataCenterInfo',
  full_name='grpc.DataCenterInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ip', full_name='grpc.DataCenterInfo.ip', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='port', full_name='grpc.DataCenterInfo.port', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=427,
  serialized_end=469,
)


_PROXYINFORAFT = _descriptor.Descriptor(
  name='ProxyInfoRaft',
  full_name='grpc.ProxyInfoRaft',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ip', full_name='grpc.ProxyInfoRaft.ip', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='port', full_name='grpc.ProxyInfoRaft.port', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=471,
  serialized_end=512,
)


_EMPTY = _descriptor.Descriptor(
  name='Empty',
  full_name='grpc.Empty',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=514,
  serialized_end=521,
)


_REPLICATIONINFO = _descriptor.Descriptor(
  name='ReplicationInfo',
  full_name='grpc.ReplicationInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='fileName', full_name='grpc.ReplicationInfo.fileName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='chunkId', full_name='grpc.ReplicationInfo.chunkId', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='fromDatacenter', full_name='grpc.ReplicationInfo.fromDatacenter', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=523,
  serialized_end=621,
)


_CHUNKUPLOADINFO = _descriptor.Descriptor(
  name='ChunkUploadInfo',
  full_name='grpc.ChunkUploadInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='chunkId', full_name='grpc.ChunkUploadInfo.chunkId', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='uploadedDatacenter', full_name='grpc.ChunkUploadInfo.uploadedDatacenter', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=623,
  serialized_end=707,
)


_UPLOADCOMPLETEFILEINFO = _descriptor.Descriptor(
  name='UploadCompleteFileInfo',
  full_name='grpc.UploadCompleteFileInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='fileName', full_name='grpc.UploadCompleteFileInfo.fileName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='lstChunkUploadInfo', full_name='grpc.UploadCompleteFileInfo.lstChunkUploadInfo', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=709,
  serialized_end=802,
)


_REQUESTCHUNKINFO = _descriptor.Descriptor(
  name='RequestChunkInfo',
  full_name='grpc.RequestChunkInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='fileName', full_name='grpc.RequestChunkInfo.fileName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='chunkId', full_name='grpc.RequestChunkInfo.chunkId', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=804,
  serialized_end=857,
)


_CHUNKLOCATIONINFO = _descriptor.Descriptor(
  name='ChunkLocationInfo',
  full_name='grpc.ChunkLocationInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='fileName', full_name='grpc.ChunkLocationInfo.fileName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='chunkId', full_name='grpc.ChunkLocationInfo.chunkId', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='lstDataCenter', full_name='grpc.ChunkLocationInfo.lstDataCenter', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='isChunkFound', full_name='grpc.ChunkLocationInfo.isChunkFound', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=859,
  serialized_end=980,
)

_TABLELOG.fields_by_name['operation'].enum_type = _LOGOPERATION
_TABLE.fields_by_name['tableLog'].message_type = _TABLELOG
_CANDIDACYRESPONSE.fields_by_name['voted'].enum_type = _VOTE
_REPLICATIONINFO.fields_by_name['fromDatacenter'].message_type = _DATACENTERINFO
_CHUNKUPLOADINFO.fields_by_name['uploadedDatacenter'].message_type = _DATACENTERINFO
_UPLOADCOMPLETEFILEINFO.fields_by_name['lstChunkUploadInfo'].message_type = _CHUNKUPLOADINFO
_CHUNKLOCATIONINFO.fields_by_name['lstDataCenter'].message_type = _DATACENTERINFO
DESCRIPTOR.message_types_by_name['Ack'] = _ACK
DESCRIPTOR.message_types_by_name['TableLog'] = _TABLELOG
DESCRIPTOR.message_types_by_name['Table'] = _TABLE
DESCRIPTOR.message_types_by_name['Candidacy'] = _CANDIDACY
DESCRIPTOR.message_types_by_name['CandidacyResponse'] = _CANDIDACYRESPONSE
DESCRIPTOR.message_types_by_name['DataCenterInfo'] = _DATACENTERINFO
DESCRIPTOR.message_types_by_name['ProxyInfoRaft'] = _PROXYINFORAFT
DESCRIPTOR.message_types_by_name['Empty'] = _EMPTY
DESCRIPTOR.message_types_by_name['ReplicationInfo'] = _REPLICATIONINFO
DESCRIPTOR.message_types_by_name['ChunkUploadInfo'] = _CHUNKUPLOADINFO
DESCRIPTOR.message_types_by_name['UploadCompleteFileInfo'] = _UPLOADCOMPLETEFILEINFO
DESCRIPTOR.message_types_by_name['RequestChunkInfo'] = _REQUESTCHUNKINFO
DESCRIPTOR.message_types_by_name['ChunkLocationInfo'] = _CHUNKLOCATIONINFO
DESCRIPTOR.enum_types_by_name['LogOperation'] = _LOGOPERATION
DESCRIPTOR.enum_types_by_name['Vote'] = _VOTE
DESCRIPTOR.enum_types_by_name['ReplicationState'] = _REPLICATIONSTATE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Ack = _reflection.GeneratedProtocolMessageType('Ack', (_message.Message,), dict(
  DESCRIPTOR = _ACK,
  __module__ = 'raft_pb2'
  # @@protoc_insertion_point(class_scope:grpc.Ack)
  ))
_sym_db.RegisterMessage(Ack)

TableLog = _reflection.GeneratedProtocolMessageType('TableLog', (_message.Message,), dict(
  DESCRIPTOR = _TABLELOG,
  __module__ = 'raft_pb2'
  # @@protoc_insertion_point(class_scope:grpc.TableLog)
  ))
_sym_db.RegisterMessage(TableLog)

Table = _reflection.GeneratedProtocolMessageType('Table', (_message.Message,), dict(
  DESCRIPTOR = _TABLE,
  __module__ = 'raft_pb2'
  # @@protoc_insertion_point(class_scope:grpc.Table)
  ))
_sym_db.RegisterMessage(Table)

Candidacy = _reflection.GeneratedProtocolMessageType('Candidacy', (_message.Message,), dict(
  DESCRIPTOR = _CANDIDACY,
  __module__ = 'raft_pb2'
  # @@protoc_insertion_point(class_scope:grpc.Candidacy)
  ))
_sym_db.RegisterMessage(Candidacy)

CandidacyResponse = _reflection.GeneratedProtocolMessageType('CandidacyResponse', (_message.Message,), dict(
  DESCRIPTOR = _CANDIDACYRESPONSE,
  __module__ = 'raft_pb2'
  # @@protoc_insertion_point(class_scope:grpc.CandidacyResponse)
  ))
_sym_db.RegisterMessage(CandidacyResponse)

DataCenterInfo = _reflection.GeneratedProtocolMessageType('DataCenterInfo', (_message.Message,), dict(
  DESCRIPTOR = _DATACENTERINFO,
  __module__ = 'raft_pb2'
  # @@protoc_insertion_point(class_scope:grpc.DataCenterInfo)
  ))
_sym_db.RegisterMessage(DataCenterInfo)

ProxyInfoRaft = _reflection.GeneratedProtocolMessageType('ProxyInfoRaft', (_message.Message,), dict(
  DESCRIPTOR = _PROXYINFORAFT,
  __module__ = 'raft_pb2'
  # @@protoc_insertion_point(class_scope:grpc.ProxyInfoRaft)
  ))
_sym_db.RegisterMessage(ProxyInfoRaft)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), dict(
  DESCRIPTOR = _EMPTY,
  __module__ = 'raft_pb2'
  # @@protoc_insertion_point(class_scope:grpc.Empty)
  ))
_sym_db.RegisterMessage(Empty)

ReplicationInfo = _reflection.GeneratedProtocolMessageType('ReplicationInfo', (_message.Message,), dict(
  DESCRIPTOR = _REPLICATIONINFO,
  __module__ = 'raft_pb2'
  # @@protoc_insertion_point(class_scope:grpc.ReplicationInfo)
  ))
_sym_db.RegisterMessage(ReplicationInfo)

ChunkUploadInfo = _reflection.GeneratedProtocolMessageType('ChunkUploadInfo', (_message.Message,), dict(
  DESCRIPTOR = _CHUNKUPLOADINFO,
  __module__ = 'raft_pb2'
  # @@protoc_insertion_point(class_scope:grpc.ChunkUploadInfo)
  ))
_sym_db.RegisterMessage(ChunkUploadInfo)

UploadCompleteFileInfo = _reflection.GeneratedProtocolMessageType('UploadCompleteFileInfo', (_message.Message,), dict(
  DESCRIPTOR = _UPLOADCOMPLETEFILEINFO,
  __module__ = 'raft_pb2'
  # @@protoc_insertion_point(class_scope:grpc.UploadCompleteFileInfo)
  ))
_sym_db.RegisterMessage(UploadCompleteFileInfo)

RequestChunkInfo = _reflection.GeneratedProtocolMessageType('RequestChunkInfo', (_message.Message,), dict(
  DESCRIPTOR = _REQUESTCHUNKINFO,
  __module__ = 'raft_pb2'
  # @@protoc_insertion_point(class_scope:grpc.RequestChunkInfo)
  ))
_sym_db.RegisterMessage(RequestChunkInfo)

ChunkLocationInfo = _reflection.GeneratedProtocolMessageType('ChunkLocationInfo', (_message.Message,), dict(
  DESCRIPTOR = _CHUNKLOCATIONINFO,
  __module__ = 'raft_pb2'
  # @@protoc_insertion_point(class_scope:grpc.ChunkLocationInfo)
  ))
_sym_db.RegisterMessage(ChunkLocationInfo)



_RAFTSERVICE = _descriptor.ServiceDescriptor(
  name='RaftService',
  full_name='grpc.RaftService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=1235,
  serialized_end=1782,
  methods=[
  _descriptor.MethodDescriptor(
    name='RaftHeartbit',
    full_name='grpc.RaftService.RaftHeartbit',
    index=0,
    containing_service=None,
    input_type=_TABLE,
    output_type=_ACK,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='RequestVote',
    full_name='grpc.RaftService.RequestVote',
    index=1,
    containing_service=None,
    input_type=_CANDIDACY,
    output_type=_CANDIDACYRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='AddFileLog',
    full_name='grpc.RaftService.AddFileLog',
    index=2,
    containing_service=None,
    input_type=_TABLELOG,
    output_type=_ACK,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='AddDataCenter',
    full_name='grpc.RaftService.AddDataCenter',
    index=3,
    containing_service=None,
    input_type=_DATACENTERINFO,
    output_type=_EMPTY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='DataCenterHeartbeat',
    full_name='grpc.RaftService.DataCenterHeartbeat',
    index=4,
    containing_service=None,
    input_type=_EMPTY,
    output_type=_EMPTY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='ReplicationInitiate',
    full_name='grpc.RaftService.ReplicationInitiate',
    index=5,
    containing_service=None,
    input_type=_REPLICATIONINFO,
    output_type=_ACK,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='AddProxy',
    full_name='grpc.RaftService.AddProxy',
    index=6,
    containing_service=None,
    input_type=_PROXYINFORAFT,
    output_type=_EMPTY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='ProxyHeartbeat',
    full_name='grpc.RaftService.ProxyHeartbeat',
    index=7,
    containing_service=None,
    input_type=_EMPTY,
    output_type=_EMPTY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='FileUploadCompleted',
    full_name='grpc.RaftService.FileUploadCompleted',
    index=8,
    containing_service=None,
    input_type=_UPLOADCOMPLETEFILEINFO,
    output_type=_EMPTY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetDataCenterListForFileChunk',
    full_name='grpc.RaftService.GetDataCenterListForFileChunk',
    index=9,
    containing_service=None,
    input_type=_REQUESTCHUNKINFO,
    output_type=_CHUNKLOCATIONINFO,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_RAFTSERVICE)

DESCRIPTOR.services_by_name['RaftService'] = _RAFTSERVICE

# @@protoc_insertion_point(module_scope)
