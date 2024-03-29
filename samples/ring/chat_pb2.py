# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chat.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='chat.proto',
  package='grpc',
  syntax='proto3',
  serialized_pb=_b('\n\nchat.proto\x12\x04grpc\"\xaa\x01\n\x07Message\x12\n\n\x02id\x18\x01 \x01(\x03\x12\x1f\n\x04type\x18\x02 \x01(\x0e\x32\x11.grpc.MessageType\x12\x0c\n\x04\x64\x61ta\x18\x03 \x01(\x0c\x12\x13\n\x0b\x64\x65stination\x18\x04 \x01(\t\x12\x0e\n\x06origin\x18\x05 \x01(\t\x12\x11\n\ttimestamp\x18\x06 \x01(\x03\x12\x0c\n\x04hops\x18\x07 \x01(\x03\x12\x0e\n\x06seqnum\x18\x08 \x01(\x03\x12\x0e\n\x06seqmax\x18\t \x01(\x03\"\x11\n\x03\x41\x63k\x12\n\n\x02id\x18\x01 \x01(\x03\"\x14\n\x04User\x12\x0c\n\x04name\x18\x01 \x01(\t*!\n\x0bMessageType\x12\x08\n\x04Text\x10\x00\x12\x08\n\x04\x46ile\x10\x01\x32\\\n\x13\x44\x61taTransferService\x12 \n\x04Send\x12\r.grpc.Message\x1a\t.grpc.Ack\x12#\n\x04Ping\x12\n.grpc.User\x1a\r.grpc.Message0\x01\x62\x06proto3')
)

_MESSAGETYPE = _descriptor.EnumDescriptor(
  name='MessageType',
  full_name='grpc.MessageType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='Text', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='File', index=1, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=234,
  serialized_end=267,
)
_sym_db.RegisterEnumDescriptor(_MESSAGETYPE)

MessageType = enum_type_wrapper.EnumTypeWrapper(_MESSAGETYPE)
Text = 0
File = 1



_MESSAGE = _descriptor.Descriptor(
  name='Message',
  full_name='grpc.Message',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='grpc.Message.id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='grpc.Message.type', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='grpc.Message.data', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='destination', full_name='grpc.Message.destination', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='origin', full_name='grpc.Message.origin', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='grpc.Message.timestamp', index=5,
      number=6, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='hops', full_name='grpc.Message.hops', index=6,
      number=7, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='seqnum', full_name='grpc.Message.seqnum', index=7,
      number=8, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='seqmax', full_name='grpc.Message.seqmax', index=8,
      number=9, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=21,
  serialized_end=191,
)


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
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=193,
  serialized_end=210,
)


_USER = _descriptor.Descriptor(
  name='User',
  full_name='grpc.User',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='grpc.User.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=212,
  serialized_end=232,
)

_MESSAGE.fields_by_name['type'].enum_type = _MESSAGETYPE
DESCRIPTOR.message_types_by_name['Message'] = _MESSAGE
DESCRIPTOR.message_types_by_name['Ack'] = _ACK
DESCRIPTOR.message_types_by_name['User'] = _USER
DESCRIPTOR.enum_types_by_name['MessageType'] = _MESSAGETYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Message = _reflection.GeneratedProtocolMessageType('Message', (_message.Message,), dict(
  DESCRIPTOR = _MESSAGE,
  __module__ = 'chat_pb2'
  # @@protoc_insertion_point(class_scope:grpc.Message)
  ))
_sym_db.RegisterMessage(Message)

Ack = _reflection.GeneratedProtocolMessageType('Ack', (_message.Message,), dict(
  DESCRIPTOR = _ACK,
  __module__ = 'chat_pb2'
  # @@protoc_insertion_point(class_scope:grpc.Ack)
  ))
_sym_db.RegisterMessage(Ack)

User = _reflection.GeneratedProtocolMessageType('User', (_message.Message,), dict(
  DESCRIPTOR = _USER,
  __module__ = 'chat_pb2'
  # @@protoc_insertion_point(class_scope:grpc.User)
  ))
_sym_db.RegisterMessage(User)



_DATATRANSFERSERVICE = _descriptor.ServiceDescriptor(
  name='DataTransferService',
  full_name='grpc.DataTransferService',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=269,
  serialized_end=361,
  methods=[
  _descriptor.MethodDescriptor(
    name='Send',
    full_name='grpc.DataTransferService.Send',
    index=0,
    containing_service=None,
    input_type=_MESSAGE,
    output_type=_ACK,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Ping',
    full_name='grpc.DataTransferService.Ping',
    index=1,
    containing_service=None,
    input_type=_USER,
    output_type=_MESSAGE,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_DATATRANSFERSERVICE)

DESCRIPTOR.services_by_name['DataTransferService'] = _DATATRANSFERSERVICE

# @@protoc_insertion_point(module_scope)
