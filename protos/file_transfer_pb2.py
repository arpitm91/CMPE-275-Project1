# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: file_transfer.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='file_transfer.proto',
  package='grpc',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x13\x66ile_transfer.proto\x12\x04grpc\"#\n\x0fRequestFileList\x12\x10\n\x08isClient\x18\x01 \x01(\x08\"\x1c\n\x08\x46ileInfo\x12\x10\n\x08\x66ileName\x18\x01 \x01(\t\"4\n\x0e\x46ileUploadInfo\x12\x10\n\x08\x66ileName\x18\x01 \x01(\t\x12\x10\n\x08\x66ileSize\x18\x02 \x01(\x02\"C\n\tChunkInfo\x12\x10\n\x08\x66ileName\x18\x01 \x01(\t\x12\x0f\n\x07\x63hunkId\x18\x02 \x01(\x03\x12\x13\n\x0bstartSeqNum\x18\x03 \x01(\x03\"_\n\x0c\x46ileMetaData\x12\x10\n\x08\x66ileName\x18\x01 \x01(\t\x12\x0f\n\x07\x63hunkId\x18\x02 \x01(\x03\x12\x0c\n\x04\x64\x61ta\x18\x03 \x01(\x0c\x12\x0e\n\x06seqNum\x18\x04 \x01(\x03\x12\x0e\n\x06seqMax\x18\x05 \x01(\x03\"a\n\x0e\x46ileUploadData\x12\x10\n\x08\x66ileName\x18\x01 \x01(\t\x12\x0f\n\x07\x63hunkId\x18\x02 \x01(\x03\x12\x0c\n\x04\x64\x61ta\x18\x03 \x01(\x0c\x12\x0e\n\x06seqNum\x18\x04 \x01(\x03\x12\x0e\n\x06seqMax\x18\x05 \x01(\x03\"%\n\tProxyInfo\x12\n\n\x02ip\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\t\"o\n\x10\x46ileLocationInfo\x12\x10\n\x08\x66ileName\x18\x01 \x01(\t\x12\x11\n\tmaxChunks\x18\x02 \x01(\x03\x12!\n\x08lstProxy\x18\x03 \x03(\x0b\x32\x0f.grpc.ProxyInfo\x12\x13\n\x0bisFileFound\x18\x04 \x01(\x08\" \n\x08\x46ileList\x12\x14\n\x0clstFileNames\x18\x01 \x03(\t\".\n\tProxyList\x12!\n\x08lstProxy\x18\x01 \x03(\x0b\x32\x0f.grpc.ProxyInfo2\xe9\x02\n\x13\x44\x61taTransferService\x12\x39\n\x0fRequestFileInfo\x12\x0e.grpc.FileInfo\x1a\x16.grpc.FileLocationInfo\x12\x39\n\x0fGetFileLocation\x12\x0e.grpc.FileInfo\x1a\x16.grpc.FileLocationInfo\x12\x36\n\rDownloadChunk\x12\x0f.grpc.ChunkInfo\x1a\x12.grpc.FileMetaData0\x01\x12\x34\n\nUploadFile\x12\x14.grpc.FileUploadData\x1a\x0e.grpc.FileInfo(\x01\x12\x32\n\tListFiles\x12\x15.grpc.RequestFileList\x1a\x0e.grpc.FileList\x12:\n\x11RequestFileUpload\x12\x14.grpc.FileUploadInfo\x1a\x0f.grpc.ProxyListb\x06proto3')
)




_REQUESTFILELIST = _descriptor.Descriptor(
  name='RequestFileList',
  full_name='grpc.RequestFileList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='isClient', full_name='grpc.RequestFileList.isClient', index=0,
      number=1, type=8, cpp_type=7, label=1,
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
  serialized_start=29,
  serialized_end=64,
)


_FILEINFO = _descriptor.Descriptor(
  name='FileInfo',
  full_name='grpc.FileInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='fileName', full_name='grpc.FileInfo.fileName', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=66,
  serialized_end=94,
)


_FILEUPLOADINFO = _descriptor.Descriptor(
  name='FileUploadInfo',
  full_name='grpc.FileUploadInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='fileName', full_name='grpc.FileUploadInfo.fileName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='fileSize', full_name='grpc.FileUploadInfo.fileSize', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=96,
  serialized_end=148,
)


_CHUNKINFO = _descriptor.Descriptor(
  name='ChunkInfo',
  full_name='grpc.ChunkInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='fileName', full_name='grpc.ChunkInfo.fileName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='chunkId', full_name='grpc.ChunkInfo.chunkId', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='startSeqNum', full_name='grpc.ChunkInfo.startSeqNum', index=2,
      number=3, type=3, cpp_type=2, label=1,
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
  serialized_start=150,
  serialized_end=217,
)


_FILEMETADATA = _descriptor.Descriptor(
  name='FileMetaData',
  full_name='grpc.FileMetaData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='fileName', full_name='grpc.FileMetaData.fileName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='chunkId', full_name='grpc.FileMetaData.chunkId', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='grpc.FileMetaData.data', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='seqNum', full_name='grpc.FileMetaData.seqNum', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='seqMax', full_name='grpc.FileMetaData.seqMax', index=4,
      number=5, type=3, cpp_type=2, label=1,
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
  serialized_start=219,
  serialized_end=314,
)


_FILEUPLOADDATA = _descriptor.Descriptor(
  name='FileUploadData',
  full_name='grpc.FileUploadData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='fileName', full_name='grpc.FileUploadData.fileName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='chunkId', full_name='grpc.FileUploadData.chunkId', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='grpc.FileUploadData.data', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='seqNum', full_name='grpc.FileUploadData.seqNum', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='seqMax', full_name='grpc.FileUploadData.seqMax', index=4,
      number=5, type=3, cpp_type=2, label=1,
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
  serialized_start=316,
  serialized_end=413,
)


_PROXYINFO = _descriptor.Descriptor(
  name='ProxyInfo',
  full_name='grpc.ProxyInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ip', full_name='grpc.ProxyInfo.ip', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='port', full_name='grpc.ProxyInfo.port', index=1,
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
  serialized_start=415,
  serialized_end=452,
)


_FILELOCATIONINFO = _descriptor.Descriptor(
  name='FileLocationInfo',
  full_name='grpc.FileLocationInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='fileName', full_name='grpc.FileLocationInfo.fileName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='maxChunks', full_name='grpc.FileLocationInfo.maxChunks', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='lstProxy', full_name='grpc.FileLocationInfo.lstProxy', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='isFileFound', full_name='grpc.FileLocationInfo.isFileFound', index=3,
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
  serialized_start=454,
  serialized_end=565,
)


_FILELIST = _descriptor.Descriptor(
  name='FileList',
  full_name='grpc.FileList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='lstFileNames', full_name='grpc.FileList.lstFileNames', index=0,
      number=1, type=9, cpp_type=9, label=3,
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
  serialized_start=567,
  serialized_end=599,
)


_PROXYLIST = _descriptor.Descriptor(
  name='ProxyList',
  full_name='grpc.ProxyList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='lstProxy', full_name='grpc.ProxyList.lstProxy', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=601,
  serialized_end=647,
)

_FILELOCATIONINFO.fields_by_name['lstProxy'].message_type = _PROXYINFO
_PROXYLIST.fields_by_name['lstProxy'].message_type = _PROXYINFO
DESCRIPTOR.message_types_by_name['RequestFileList'] = _REQUESTFILELIST
DESCRIPTOR.message_types_by_name['FileInfo'] = _FILEINFO
DESCRIPTOR.message_types_by_name['FileUploadInfo'] = _FILEUPLOADINFO
DESCRIPTOR.message_types_by_name['ChunkInfo'] = _CHUNKINFO
DESCRIPTOR.message_types_by_name['FileMetaData'] = _FILEMETADATA
DESCRIPTOR.message_types_by_name['FileUploadData'] = _FILEUPLOADDATA
DESCRIPTOR.message_types_by_name['ProxyInfo'] = _PROXYINFO
DESCRIPTOR.message_types_by_name['FileLocationInfo'] = _FILELOCATIONINFO
DESCRIPTOR.message_types_by_name['FileList'] = _FILELIST
DESCRIPTOR.message_types_by_name['ProxyList'] = _PROXYLIST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RequestFileList = _reflection.GeneratedProtocolMessageType('RequestFileList', (_message.Message,), dict(
  DESCRIPTOR = _REQUESTFILELIST,
  __module__ = 'file_transfer_pb2'
  # @@protoc_insertion_point(class_scope:grpc.RequestFileList)
  ))
_sym_db.RegisterMessage(RequestFileList)

FileInfo = _reflection.GeneratedProtocolMessageType('FileInfo', (_message.Message,), dict(
  DESCRIPTOR = _FILEINFO,
  __module__ = 'file_transfer_pb2'
  # @@protoc_insertion_point(class_scope:grpc.FileInfo)
  ))
_sym_db.RegisterMessage(FileInfo)

FileUploadInfo = _reflection.GeneratedProtocolMessageType('FileUploadInfo', (_message.Message,), dict(
  DESCRIPTOR = _FILEUPLOADINFO,
  __module__ = 'file_transfer_pb2'
  # @@protoc_insertion_point(class_scope:grpc.FileUploadInfo)
  ))
_sym_db.RegisterMessage(FileUploadInfo)

ChunkInfo = _reflection.GeneratedProtocolMessageType('ChunkInfo', (_message.Message,), dict(
  DESCRIPTOR = _CHUNKINFO,
  __module__ = 'file_transfer_pb2'
  # @@protoc_insertion_point(class_scope:grpc.ChunkInfo)
  ))
_sym_db.RegisterMessage(ChunkInfo)

FileMetaData = _reflection.GeneratedProtocolMessageType('FileMetaData', (_message.Message,), dict(
  DESCRIPTOR = _FILEMETADATA,
  __module__ = 'file_transfer_pb2'
  # @@protoc_insertion_point(class_scope:grpc.FileMetaData)
  ))
_sym_db.RegisterMessage(FileMetaData)

FileUploadData = _reflection.GeneratedProtocolMessageType('FileUploadData', (_message.Message,), dict(
  DESCRIPTOR = _FILEUPLOADDATA,
  __module__ = 'file_transfer_pb2'
  # @@protoc_insertion_point(class_scope:grpc.FileUploadData)
  ))
_sym_db.RegisterMessage(FileUploadData)

ProxyInfo = _reflection.GeneratedProtocolMessageType('ProxyInfo', (_message.Message,), dict(
  DESCRIPTOR = _PROXYINFO,
  __module__ = 'file_transfer_pb2'
  # @@protoc_insertion_point(class_scope:grpc.ProxyInfo)
  ))
_sym_db.RegisterMessage(ProxyInfo)

FileLocationInfo = _reflection.GeneratedProtocolMessageType('FileLocationInfo', (_message.Message,), dict(
  DESCRIPTOR = _FILELOCATIONINFO,
  __module__ = 'file_transfer_pb2'
  # @@protoc_insertion_point(class_scope:grpc.FileLocationInfo)
  ))
_sym_db.RegisterMessage(FileLocationInfo)

FileList = _reflection.GeneratedProtocolMessageType('FileList', (_message.Message,), dict(
  DESCRIPTOR = _FILELIST,
  __module__ = 'file_transfer_pb2'
  # @@protoc_insertion_point(class_scope:grpc.FileList)
  ))
_sym_db.RegisterMessage(FileList)

ProxyList = _reflection.GeneratedProtocolMessageType('ProxyList', (_message.Message,), dict(
  DESCRIPTOR = _PROXYLIST,
  __module__ = 'file_transfer_pb2'
  # @@protoc_insertion_point(class_scope:grpc.ProxyList)
  ))
_sym_db.RegisterMessage(ProxyList)



_DATATRANSFERSERVICE = _descriptor.ServiceDescriptor(
  name='DataTransferService',
  full_name='grpc.DataTransferService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=650,
  serialized_end=1011,
  methods=[
  _descriptor.MethodDescriptor(
    name='RequestFileInfo',
    full_name='grpc.DataTransferService.RequestFileInfo',
    index=0,
    containing_service=None,
    input_type=_FILEINFO,
    output_type=_FILELOCATIONINFO,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetFileLocation',
    full_name='grpc.DataTransferService.GetFileLocation',
    index=1,
    containing_service=None,
    input_type=_FILEINFO,
    output_type=_FILELOCATIONINFO,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='DownloadChunk',
    full_name='grpc.DataTransferService.DownloadChunk',
    index=2,
    containing_service=None,
    input_type=_CHUNKINFO,
    output_type=_FILEMETADATA,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='UploadFile',
    full_name='grpc.DataTransferService.UploadFile',
    index=3,
    containing_service=None,
    input_type=_FILEUPLOADDATA,
    output_type=_FILEINFO,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='ListFiles',
    full_name='grpc.DataTransferService.ListFiles',
    index=4,
    containing_service=None,
    input_type=_REQUESTFILELIST,
    output_type=_FILELIST,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='RequestFileUpload',
    full_name='grpc.DataTransferService.RequestFileUpload',
    index=5,
    containing_service=None,
    input_type=_FILEUPLOADINFO,
    output_type=_PROXYLIST,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_DATATRANSFERSERVICE)

DESCRIPTOR.services_by_name['DataTransferService'] = _DATATRANSFERSERVICE

# @@protoc_insertion_point(module_scope)
