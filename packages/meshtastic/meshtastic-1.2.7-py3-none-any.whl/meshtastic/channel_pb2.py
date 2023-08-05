# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: channel.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='channel.proto',
  package='',
  syntax='proto3',
  serialized_options=b'\n\023com.geeksville.meshB\rChannelProtosH\003',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\rchannel.proto\"\xe6\x02\n\x0f\x43hannelSettings\x12\x10\n\x08tx_power\x18\x01 \x01(\x05\x12\x32\n\x0cmodem_config\x18\x03 \x01(\x0e\x32\x1c.ChannelSettings.ModemConfig\x12\x11\n\tbandwidth\x18\x06 \x01(\r\x12\x15\n\rspread_factor\x18\x07 \x01(\r\x12\x13\n\x0b\x63oding_rate\x18\x08 \x01(\r\x12\x13\n\x0b\x63hannel_num\x18\t \x01(\r\x12\x0b\n\x03psk\x18\x04 \x01(\x0c\x12\x0c\n\x04name\x18\x05 \x01(\t\x12\n\n\x02id\x18\n \x01(\x07\x12\x16\n\x0euplink_enabled\x18\x10 \x01(\x08\x12\x18\n\x10\x64ownlink_enabled\x18\x11 \x01(\x08\"`\n\x0bModemConfig\x12\x12\n\x0e\x42w125Cr45Sf128\x10\x00\x12\x12\n\x0e\x42w500Cr45Sf128\x10\x01\x12\x14\n\x10\x42w31_25Cr48Sf512\x10\x02\x12\x13\n\x0f\x42w125Cr48Sf4096\x10\x03\"\x8b\x01\n\x07\x43hannel\x12\r\n\x05index\x18\x01 \x01(\r\x12\"\n\x08settings\x18\x02 \x01(\x0b\x32\x10.ChannelSettings\x12\x1b\n\x04role\x18\x03 \x01(\x0e\x32\r.Channel.Role\"0\n\x04Role\x12\x0c\n\x08\x44ISABLED\x10\x00\x12\x0b\n\x07PRIMARY\x10\x01\x12\r\n\tSECONDARY\x10\x02\x42&\n\x13\x63om.geeksville.meshB\rChannelProtosH\x03\x62\x06proto3'
)



_CHANNELSETTINGS_MODEMCONFIG = _descriptor.EnumDescriptor(
  name='ModemConfig',
  full_name='ChannelSettings.ModemConfig',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='Bw125Cr45Sf128', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='Bw500Cr45Sf128', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='Bw31_25Cr48Sf512', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='Bw125Cr48Sf4096', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=280,
  serialized_end=376,
)
_sym_db.RegisterEnumDescriptor(_CHANNELSETTINGS_MODEMCONFIG)

_CHANNEL_ROLE = _descriptor.EnumDescriptor(
  name='Role',
  full_name='Channel.Role',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='DISABLED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PRIMARY', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SECONDARY', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=470,
  serialized_end=518,
)
_sym_db.RegisterEnumDescriptor(_CHANNEL_ROLE)


_CHANNELSETTINGS = _descriptor.Descriptor(
  name='ChannelSettings',
  full_name='ChannelSettings',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='tx_power', full_name='ChannelSettings.tx_power', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='modem_config', full_name='ChannelSettings.modem_config', index=1,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bandwidth', full_name='ChannelSettings.bandwidth', index=2,
      number=6, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='spread_factor', full_name='ChannelSettings.spread_factor', index=3,
      number=7, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='coding_rate', full_name='ChannelSettings.coding_rate', index=4,
      number=8, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='channel_num', full_name='ChannelSettings.channel_num', index=5,
      number=9, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='psk', full_name='ChannelSettings.psk', index=6,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='ChannelSettings.name', index=7,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='id', full_name='ChannelSettings.id', index=8,
      number=10, type=7, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='uplink_enabled', full_name='ChannelSettings.uplink_enabled', index=9,
      number=16, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='downlink_enabled', full_name='ChannelSettings.downlink_enabled', index=10,
      number=17, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CHANNELSETTINGS_MODEMCONFIG,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=18,
  serialized_end=376,
)


_CHANNEL = _descriptor.Descriptor(
  name='Channel',
  full_name='Channel',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='index', full_name='Channel.index', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='settings', full_name='Channel.settings', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='role', full_name='Channel.role', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CHANNEL_ROLE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=379,
  serialized_end=518,
)

_CHANNELSETTINGS.fields_by_name['modem_config'].enum_type = _CHANNELSETTINGS_MODEMCONFIG
_CHANNELSETTINGS_MODEMCONFIG.containing_type = _CHANNELSETTINGS
_CHANNEL.fields_by_name['settings'].message_type = _CHANNELSETTINGS
_CHANNEL.fields_by_name['role'].enum_type = _CHANNEL_ROLE
_CHANNEL_ROLE.containing_type = _CHANNEL
DESCRIPTOR.message_types_by_name['ChannelSettings'] = _CHANNELSETTINGS
DESCRIPTOR.message_types_by_name['Channel'] = _CHANNEL
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ChannelSettings = _reflection.GeneratedProtocolMessageType('ChannelSettings', (_message.Message,), {
  'DESCRIPTOR' : _CHANNELSETTINGS,
  '__module__' : 'channel_pb2'
  # @@protoc_insertion_point(class_scope:ChannelSettings)
  })
_sym_db.RegisterMessage(ChannelSettings)

Channel = _reflection.GeneratedProtocolMessageType('Channel', (_message.Message,), {
  'DESCRIPTOR' : _CHANNEL,
  '__module__' : 'channel_pb2'
  # @@protoc_insertion_point(class_scope:Channel)
  })
_sym_db.RegisterMessage(Channel)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
