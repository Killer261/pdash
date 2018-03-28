# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: trade_msg.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='trade_msg.proto',
  package='cpchain',
  syntax='proto3',
  serialized_pb=_b('\n\x0ftrade_msg.proto\x12\x07\x63pchain\"\x96\x04\n\x07Message\x12*\n\x04type\x18\x01 \x01(\x0e\x32\x1c.cpchain.Message.MessageType\x12\x13\n\x0bseller_addr\x18\x02 \x01(\x0c\x12\x12\n\nbuyer_addr\x18\x03 \x01(\x0c\x12\x13\n\x0bmarket_hash\x18\x04 \x01(\x0c\x12)\n\x07storage\x18\x05 \x01(\x0b\x32\x18.cpchain.Message.Storage\x1a\xaa\x02\n\x07Storage\x12\x32\n\x04type\x18\x01 \x01(\x0e\x32$.cpchain.Message.Storage.StorageType\x12\x35\n\x04ipfs\x18\x02 \x01(\x0b\x32%.cpchain.Message.Storage.IPFS_StorageH\x00\x12\x31\n\x02s3\x18\x03 \x01(\x0b\x32#.cpchain.Message.Storage.S3_StorageH\x00\x1a:\n\x0cIPFS_Storage\x12\x11\n\tfile_hash\x18\x01 \x01(\x0c\x12\x17\n\x0f\x64\x65\x66\x61ult_gateway\x18\x02 \x01(\t\x1a\x19\n\nS3_Storage\x12\x0b\n\x03uri\x18\x01 \x01(\t\"\x1f\n\x0bStorageType\x12\x08\n\x04IPFS\x10\x00\x12\x06\n\x02S3\x10\x01\x42\t\n\x07storage\"I\n\x0bMessageType\x12\x1d\n\x19SELLER_UPLOAD_KEY_FILEURI\x10\x00\x12\x1b\n\x17\x42UYER_DOWNLOAD_KEY_FILE\x10\x01\x62\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_MESSAGE_STORAGE_STORAGETYPE = _descriptor.EnumDescriptor(
  name='StorageType',
  full_name='cpchain.Message.Storage.StorageType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='IPFS', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='S3', index=1, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=446,
  serialized_end=477,
)
_sym_db.RegisterEnumDescriptor(_MESSAGE_STORAGE_STORAGETYPE)

_MESSAGE_MESSAGETYPE = _descriptor.EnumDescriptor(
  name='MessageType',
  full_name='cpchain.Message.MessageType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SELLER_UPLOAD_KEY_FILEURI', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BUYER_DOWNLOAD_KEY_FILE', index=1, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=490,
  serialized_end=563,
)
_sym_db.RegisterEnumDescriptor(_MESSAGE_MESSAGETYPE)


_MESSAGE_STORAGE_IPFS_STORAGE = _descriptor.Descriptor(
  name='IPFS_Storage',
  full_name='cpchain.Message.Storage.IPFS_Storage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='file_hash', full_name='cpchain.Message.Storage.IPFS_Storage.file_hash', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='default_gateway', full_name='cpchain.Message.Storage.IPFS_Storage.default_gateway', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
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
  serialized_start=359,
  serialized_end=417,
)

_MESSAGE_STORAGE_S3_STORAGE = _descriptor.Descriptor(
  name='S3_Storage',
  full_name='cpchain.Message.Storage.S3_Storage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uri', full_name='cpchain.Message.Storage.S3_Storage.uri', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
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
  serialized_start=419,
  serialized_end=444,
)

_MESSAGE_STORAGE = _descriptor.Descriptor(
  name='Storage',
  full_name='cpchain.Message.Storage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='cpchain.Message.Storage.type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ipfs', full_name='cpchain.Message.Storage.ipfs', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='s3', full_name='cpchain.Message.Storage.s3', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_MESSAGE_STORAGE_IPFS_STORAGE, _MESSAGE_STORAGE_S3_STORAGE, ],
  enum_types=[
    _MESSAGE_STORAGE_STORAGETYPE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='storage', full_name='cpchain.Message.Storage.storage',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=190,
  serialized_end=488,
)

_MESSAGE = _descriptor.Descriptor(
  name='Message',
  full_name='cpchain.Message',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='cpchain.Message.type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='seller_addr', full_name='cpchain.Message.seller_addr', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='buyer_addr', full_name='cpchain.Message.buyer_addr', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='market_hash', full_name='cpchain.Message.market_hash', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='storage', full_name='cpchain.Message.storage', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_MESSAGE_STORAGE, ],
  enum_types=[
    _MESSAGE_MESSAGETYPE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=29,
  serialized_end=563,
)

_MESSAGE_STORAGE_IPFS_STORAGE.containing_type = _MESSAGE_STORAGE
_MESSAGE_STORAGE_S3_STORAGE.containing_type = _MESSAGE_STORAGE
_MESSAGE_STORAGE.fields_by_name['type'].enum_type = _MESSAGE_STORAGE_STORAGETYPE
_MESSAGE_STORAGE.fields_by_name['ipfs'].message_type = _MESSAGE_STORAGE_IPFS_STORAGE
_MESSAGE_STORAGE.fields_by_name['s3'].message_type = _MESSAGE_STORAGE_S3_STORAGE
_MESSAGE_STORAGE.containing_type = _MESSAGE
_MESSAGE_STORAGE_STORAGETYPE.containing_type = _MESSAGE_STORAGE
_MESSAGE_STORAGE.oneofs_by_name['storage'].fields.append(
  _MESSAGE_STORAGE.fields_by_name['ipfs'])
_MESSAGE_STORAGE.fields_by_name['ipfs'].containing_oneof = _MESSAGE_STORAGE.oneofs_by_name['storage']
_MESSAGE_STORAGE.oneofs_by_name['storage'].fields.append(
  _MESSAGE_STORAGE.fields_by_name['s3'])
_MESSAGE_STORAGE.fields_by_name['s3'].containing_oneof = _MESSAGE_STORAGE.oneofs_by_name['storage']
_MESSAGE.fields_by_name['type'].enum_type = _MESSAGE_MESSAGETYPE
_MESSAGE.fields_by_name['storage'].message_type = _MESSAGE_STORAGE
_MESSAGE_MESSAGETYPE.containing_type = _MESSAGE
DESCRIPTOR.message_types_by_name['Message'] = _MESSAGE

Message = _reflection.GeneratedProtocolMessageType('Message', (_message.Message,), dict(

  Storage = _reflection.GeneratedProtocolMessageType('Storage', (_message.Message,), dict(

    IPFS_Storage = _reflection.GeneratedProtocolMessageType('IPFS_Storage', (_message.Message,), dict(
      DESCRIPTOR = _MESSAGE_STORAGE_IPFS_STORAGE,
      __module__ = 'trade_msg_pb2'
      # @@protoc_insertion_point(class_scope:cpchain.Message.Storage.IPFS_Storage)
      ))
    ,

    S3_Storage = _reflection.GeneratedProtocolMessageType('S3_Storage', (_message.Message,), dict(
      DESCRIPTOR = _MESSAGE_STORAGE_S3_STORAGE,
      __module__ = 'trade_msg_pb2'
      # @@protoc_insertion_point(class_scope:cpchain.Message.Storage.S3_Storage)
      ))
    ,
    DESCRIPTOR = _MESSAGE_STORAGE,
    __module__ = 'trade_msg_pb2'
    # @@protoc_insertion_point(class_scope:cpchain.Message.Storage)
    ))
  ,
  DESCRIPTOR = _MESSAGE,
  __module__ = 'trade_msg_pb2'
  # @@protoc_insertion_point(class_scope:cpchain.Message)
  ))
_sym_db.RegisterMessage(Message)
_sym_db.RegisterMessage(Message.Storage)
_sym_db.RegisterMessage(Message.Storage.IPFS_Storage)
_sym_db.RegisterMessage(Message.Storage.S3_Storage)


# @@protoc_insertion_point(module_scope)