# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/apm_test_client.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1cprotos/apm_test_client.proto\"\x8a\x02\n\rStartSpanArgs\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x14\n\x07service\x18\x02 \x01(\tH\x00\x88\x01\x01\x12\x16\n\tparent_id\x18\x03 \x01(\x04H\x01\x88\x01\x01\x12\x15\n\x08resource\x18\x04 \x01(\tH\x02\x88\x01\x01\x12\x11\n\x04type\x18\x05 \x01(\tH\x03\x88\x01\x01\x12\x13\n\x06origin\x18\x06 \x01(\tH\x04\x88\x01\x01\x12\x32\n\x0chttp_headers\x18\x07 \x01(\x0b\x32\x17.DistributedHTTPHeadersH\x05\x88\x01\x01\x42\n\n\x08_serviceB\x0c\n\n_parent_idB\x0b\n\t_resourceB\x07\n\x05_typeB\t\n\x07_originB\x0f\n\r_http_headers\"<\n\x16\x44istributedHTTPHeaders\x12\"\n\x0chttp_headers\x18\t \x03(\x0b\x32\x0c.HeaderTuple\")\n\x0bHeaderTuple\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"4\n\x0fStartSpanReturn\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\x12\x10\n\x08trace_id\x18\x02 \x01(\x04\"$\n\x11InjectHeadersArgs\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\"Z\n\x13InjectHeadersReturn\x12\x32\n\x0chttp_headers\x18\x01 \x01(\x0b\x32\x17.DistributedHTTPHeadersH\x00\x88\x01\x01\x42\x0f\n\r_http_headers\"\x1c\n\x0e\x46inishSpanArgs\x12\n\n\x02id\x18\x01 \x01(\x04\"\x12\n\x10\x46inishSpanReturn\">\n\x0fSpanSetMetaArgs\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\x12\x0b\n\x03key\x18\x02 \x01(\t\x12\r\n\x05value\x18\x03 \x01(\t\"\x13\n\x11SpanSetMetaReturn\"@\n\x11SpanSetMetricArgs\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\x12\x0b\n\x03key\x18\x02 \x01(\t\x12\r\n\x05value\x18\x03 \x01(\x02\"\x15\n\x13SpanSetMetricReturn\"\x7f\n\x10SpanSetErrorArgs\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\x12\x11\n\x04type\x18\x02 \x01(\tH\x00\x88\x01\x01\x12\x14\n\x07message\x18\x03 \x01(\tH\x01\x88\x01\x01\x12\x12\n\x05stack\x18\x04 \x01(\tH\x02\x88\x01\x01\x42\x07\n\x05_typeB\n\n\x08_messageB\x08\n\x06_stack\"\x14\n\x12SpanSetErrorReturn\"\x10\n\x0e\x46lushSpansArgs\"\x12\n\x10\x46lushSpansReturn\"\x15\n\x13\x46lushTraceStatsArgs\"\x17\n\x15\x46lushTraceStatsReturn\"\xff\x02\n\x11OtelStartSpanArgs\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x15\n\x08new_root\x18\x02 \x01(\x08H\x00\x88\x01\x01\x12\x16\n\tparent_id\x18\x03 \x01(\x04H\x01\x88\x01\x01\x12\x16\n\tspan_kind\x18\t \x01(\x04H\x02\x88\x01\x01\x12\x14\n\x07service\x18\x04 \x01(\tH\x03\x88\x01\x01\x12\x15\n\x08resource\x18\x05 \x01(\tH\x04\x88\x01\x01\x12\x11\n\x04type\x18\x06 \x01(\tH\x05\x88\x01\x01\x12\x16\n\ttimestamp\x18\x07 \x01(\x03H\x06\x88\x01\x01\x12\x32\n\x0chttp_headers\x18\n \x01(\x0b\x32\x17.DistributedHTTPHeadersH\x07\x88\x01\x01\x12\x1f\n\nattributes\x18\x08 \x01(\x0b\x32\x0b.AttributesB\x0b\n\t_new_rootB\x0c\n\n_parent_idB\x0c\n\n_span_kindB\n\n\x08_serviceB\x0b\n\t_resourceB\x07\n\x05_typeB\x0c\n\n_timestampB\x0f\n\r_http_headers\"8\n\x13OtelStartSpanReturn\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\x12\x10\n\x08trace_id\x18\x02 \x01(\x04\"C\n\x0fOtelEndSpanArgs\x12\n\n\x02id\x18\x01 \x01(\x04\x12\x16\n\ttimestamp\x18\x02 \x01(\x03H\x00\x88\x01\x01\x42\x0c\n\n_timestamp\"\x13\n\x11OtelEndSpanReturn\"%\n\x12OtelForceFlushArgs\x12\x0f\n\x07seconds\x18\x01 \x01(\r\"\'\n\x14OtelForceFlushReturn\x12\x0f\n\x07success\x18\x01 \x01(\x08\"%\n\x12OtelFlushSpansArgs\x12\x0f\n\x07seconds\x18\x01 \x01(\r\"\'\n\x14OtelFlushSpansReturn\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x19\n\x17OtelFlushTraceStatsArgs\"\x1b\n\x19OtelFlushTraceStatsReturn\"\x14\n\x12OtelStopTracerArgs\"\x16\n\x14OtelStopTracerReturn\"A\n\x13OtelStartTracerArgs\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0b\n\x03\x65nv\x18\x02 \x01(\t\x12\x0f\n\x07service\x18\x03 \x01(\t\"\x17\n\x15OtelStartTracerReturn\"&\n\x13OtelIsRecordingArgs\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\"-\n\x15OtelIsRecordingReturn\x12\x14\n\x0cis_recording\x18\x01 \x01(\x08\"&\n\x13OtelSpanContextArgs\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\"t\n\x15OtelSpanContextReturn\x12\x0f\n\x07span_id\x18\x01 \x01(\t\x12\x10\n\x08trace_id\x18\x02 \x01(\t\x12\x13\n\x0btrace_flags\x18\x03 \x01(\t\x12\x13\n\x0btrace_state\x18\x04 \x01(\t\x12\x0e\n\x06remote\x18\x05 \x01(\x08\"G\n\x11OtelSetStatusArgs\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\x12\x0c\n\x04\x63ode\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\"\x15\n\x13OtelSetStatusReturn\"0\n\x0fOtelSetNameArgs\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\x12\x0c\n\x04name\x18\x02 \x01(\t\"\x13\n\x11OtelSetNameReturn\"I\n\x15OtelSetAttributesArgs\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\x12\x1f\n\nattributes\x18\x02 \x01(\x0b\x32\x0b.Attributes\"\x19\n\x17OtelSetAttributesReturn\"r\n\nAttributes\x12*\n\x08key_vals\x18\x03 \x03(\x0b\x32\x18.Attributes.KeyValsEntry\x1a\x38\n\x0cKeyValsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x17\n\x05value\x18\x02 \x01(\x0b\x32\x08.ListVal:\x02\x38\x01\" \n\x07ListVal\x12\x15\n\x03val\x18\x01 \x03(\x0b\x32\x08.AttrVal\"g\n\x07\x41ttrVal\x12\x12\n\x08\x62ool_val\x18\x01 \x01(\x08H\x00\x12\x14\n\nstring_val\x18\x02 \x01(\tH\x00\x12\x14\n\ndouble_val\x18\x03 \x01(\x01H\x00\x12\x15\n\x0binteger_val\x18\x04 \x01(\x03H\x00\x42\x05\n\x03val\"\x10\n\x0eStopTracerArgs\"\x12\n\x10StopTracerReturn\"=\n\x0fStartTracerArgs\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0b\n\x03\x65nv\x18\x02 \x01(\t\x12\x0f\n\x07service\x18\x03 \x01(\t\"\x13\n\x11StartTracerReturn2\x83\t\n\tAPMClient\x12/\n\tStartSpan\x12\x0e.StartSpanArgs\x1a\x10.StartSpanReturn\"\x00\x12\x32\n\nFinishSpan\x12\x0f.FinishSpanArgs\x1a\x11.FinishSpanReturn\"\x00\x12\x35\n\x0bSpanSetMeta\x12\x10.SpanSetMetaArgs\x1a\x12.SpanSetMetaReturn\"\x00\x12;\n\rSpanSetMetric\x12\x12.SpanSetMetricArgs\x1a\x14.SpanSetMetricReturn\"\x00\x12\x38\n\x0cSpanSetError\x12\x11.SpanSetErrorArgs\x1a\x13.SpanSetErrorReturn\"\x00\x12;\n\rInjectHeaders\x12\x12.InjectHeadersArgs\x1a\x14.InjectHeadersReturn\"\x00\x12\x32\n\nFlushSpans\x12\x0f.FlushSpansArgs\x1a\x11.FlushSpansReturn\"\x00\x12\x41\n\x0f\x46lushTraceStats\x12\x14.FlushTraceStatsArgs\x1a\x16.FlushTraceStatsReturn\"\x00\x12;\n\rOtelStartSpan\x12\x12.OtelStartSpanArgs\x1a\x14.OtelStartSpanReturn\"\x00\x12\x35\n\x0bOtelEndSpan\x12\x10.OtelEndSpanArgs\x1a\x12.OtelEndSpanReturn\"\x00\x12\x41\n\x0fOtelIsRecording\x12\x14.OtelIsRecordingArgs\x1a\x16.OtelIsRecordingReturn\"\x00\x12\x41\n\x0fOtelSpanContext\x12\x14.OtelSpanContextArgs\x1a\x16.OtelSpanContextReturn\"\x00\x12;\n\rOtelSetStatus\x12\x12.OtelSetStatusArgs\x1a\x14.OtelSetStatusReturn\"\x00\x12\x35\n\x0bOtelSetName\x12\x10.OtelSetNameArgs\x1a\x12.OtelSetNameReturn\"\x00\x12G\n\x11OtelSetAttributes\x12\x16.OtelSetAttributesArgs\x1a\x18.OtelSetAttributesReturn\"\x00\x12>\n\x0eOtelFlushSpans\x12\x13.OtelFlushSpansArgs\x1a\x15.OtelFlushSpansReturn\"\x00\x12M\n\x13OtelFlushTraceStats\x12\x18.OtelFlushTraceStatsArgs\x1a\x1a.OtelFlushTraceStatsReturn\"\x00\x12\x35\n\x0bStartTracer\x12\x10.StartTracerArgs\x1a\x12.StartTracerReturn\"\x00\x12\x32\n\nStopTracer\x12\x0f.StopTracerArgs\x1a\x11.StopTracerReturn\"\x00\x42\x16\n\x14\x63om.datadoghq.clientb\x06proto3')



_STARTSPANARGS = DESCRIPTOR.message_types_by_name['StartSpanArgs']
_DISTRIBUTEDHTTPHEADERS = DESCRIPTOR.message_types_by_name['DistributedHTTPHeaders']
_HEADERTUPLE = DESCRIPTOR.message_types_by_name['HeaderTuple']
_STARTSPANRETURN = DESCRIPTOR.message_types_by_name['StartSpanReturn']
_INJECTHEADERSARGS = DESCRIPTOR.message_types_by_name['InjectHeadersArgs']
_INJECTHEADERSRETURN = DESCRIPTOR.message_types_by_name['InjectHeadersReturn']
_FINISHSPANARGS = DESCRIPTOR.message_types_by_name['FinishSpanArgs']
_FINISHSPANRETURN = DESCRIPTOR.message_types_by_name['FinishSpanReturn']
_SPANSETMETAARGS = DESCRIPTOR.message_types_by_name['SpanSetMetaArgs']
_SPANSETMETARETURN = DESCRIPTOR.message_types_by_name['SpanSetMetaReturn']
_SPANSETMETRICARGS = DESCRIPTOR.message_types_by_name['SpanSetMetricArgs']
_SPANSETMETRICRETURN = DESCRIPTOR.message_types_by_name['SpanSetMetricReturn']
_SPANSETERRORARGS = DESCRIPTOR.message_types_by_name['SpanSetErrorArgs']
_SPANSETERRORRETURN = DESCRIPTOR.message_types_by_name['SpanSetErrorReturn']
_FLUSHSPANSARGS = DESCRIPTOR.message_types_by_name['FlushSpansArgs']
_FLUSHSPANSRETURN = DESCRIPTOR.message_types_by_name['FlushSpansReturn']
_FLUSHTRACESTATSARGS = DESCRIPTOR.message_types_by_name['FlushTraceStatsArgs']
_FLUSHTRACESTATSRETURN = DESCRIPTOR.message_types_by_name['FlushTraceStatsReturn']
_OTELSTARTSPANARGS = DESCRIPTOR.message_types_by_name['OtelStartSpanArgs']
_OTELSTARTSPANRETURN = DESCRIPTOR.message_types_by_name['OtelStartSpanReturn']
_OTELENDSPANARGS = DESCRIPTOR.message_types_by_name['OtelEndSpanArgs']
_OTELENDSPANRETURN = DESCRIPTOR.message_types_by_name['OtelEndSpanReturn']
_OTELFORCEFLUSHARGS = DESCRIPTOR.message_types_by_name['OtelForceFlushArgs']
_OTELFORCEFLUSHRETURN = DESCRIPTOR.message_types_by_name['OtelForceFlushReturn']
_OTELFLUSHSPANSARGS = DESCRIPTOR.message_types_by_name['OtelFlushSpansArgs']
_OTELFLUSHSPANSRETURN = DESCRIPTOR.message_types_by_name['OtelFlushSpansReturn']
_OTELFLUSHTRACESTATSARGS = DESCRIPTOR.message_types_by_name['OtelFlushTraceStatsArgs']
_OTELFLUSHTRACESTATSRETURN = DESCRIPTOR.message_types_by_name['OtelFlushTraceStatsReturn']
_OTELSTOPTRACERARGS = DESCRIPTOR.message_types_by_name['OtelStopTracerArgs']
_OTELSTOPTRACERRETURN = DESCRIPTOR.message_types_by_name['OtelStopTracerReturn']
_OTELSTARTTRACERARGS = DESCRIPTOR.message_types_by_name['OtelStartTracerArgs']
_OTELSTARTTRACERRETURN = DESCRIPTOR.message_types_by_name['OtelStartTracerReturn']
_OTELISRECORDINGARGS = DESCRIPTOR.message_types_by_name['OtelIsRecordingArgs']
_OTELISRECORDINGRETURN = DESCRIPTOR.message_types_by_name['OtelIsRecordingReturn']
_OTELSPANCONTEXTARGS = DESCRIPTOR.message_types_by_name['OtelSpanContextArgs']
_OTELSPANCONTEXTRETURN = DESCRIPTOR.message_types_by_name['OtelSpanContextReturn']
_OTELSETSTATUSARGS = DESCRIPTOR.message_types_by_name['OtelSetStatusArgs']
_OTELSETSTATUSRETURN = DESCRIPTOR.message_types_by_name['OtelSetStatusReturn']
_OTELSETNAMEARGS = DESCRIPTOR.message_types_by_name['OtelSetNameArgs']
_OTELSETNAMERETURN = DESCRIPTOR.message_types_by_name['OtelSetNameReturn']
_OTELSETATTRIBUTESARGS = DESCRIPTOR.message_types_by_name['OtelSetAttributesArgs']
_OTELSETATTRIBUTESRETURN = DESCRIPTOR.message_types_by_name['OtelSetAttributesReturn']
_ATTRIBUTES = DESCRIPTOR.message_types_by_name['Attributes']
_ATTRIBUTES_KEYVALSENTRY = _ATTRIBUTES.nested_types_by_name['KeyValsEntry']
_LISTVAL = DESCRIPTOR.message_types_by_name['ListVal']
_ATTRVAL = DESCRIPTOR.message_types_by_name['AttrVal']
_STOPTRACERARGS = DESCRIPTOR.message_types_by_name['StopTracerArgs']
_STOPTRACERRETURN = DESCRIPTOR.message_types_by_name['StopTracerReturn']
_STARTTRACERARGS = DESCRIPTOR.message_types_by_name['StartTracerArgs']
_STARTTRACERRETURN = DESCRIPTOR.message_types_by_name['StartTracerReturn']
StartSpanArgs = _reflection.GeneratedProtocolMessageType('StartSpanArgs', (_message.Message,), {
  'DESCRIPTOR' : _STARTSPANARGS,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:StartSpanArgs)
  })
_sym_db.RegisterMessage(StartSpanArgs)

DistributedHTTPHeaders = _reflection.GeneratedProtocolMessageType('DistributedHTTPHeaders', (_message.Message,), {
  'DESCRIPTOR' : _DISTRIBUTEDHTTPHEADERS,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:DistributedHTTPHeaders)
  })
_sym_db.RegisterMessage(DistributedHTTPHeaders)

HeaderTuple = _reflection.GeneratedProtocolMessageType('HeaderTuple', (_message.Message,), {
  'DESCRIPTOR' : _HEADERTUPLE,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:HeaderTuple)
  })
_sym_db.RegisterMessage(HeaderTuple)

StartSpanReturn = _reflection.GeneratedProtocolMessageType('StartSpanReturn', (_message.Message,), {
  'DESCRIPTOR' : _STARTSPANRETURN,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:StartSpanReturn)
  })
_sym_db.RegisterMessage(StartSpanReturn)

InjectHeadersArgs = _reflection.GeneratedProtocolMessageType('InjectHeadersArgs', (_message.Message,), {
  'DESCRIPTOR' : _INJECTHEADERSARGS,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:InjectHeadersArgs)
  })
_sym_db.RegisterMessage(InjectHeadersArgs)

InjectHeadersReturn = _reflection.GeneratedProtocolMessageType('InjectHeadersReturn', (_message.Message,), {
  'DESCRIPTOR' : _INJECTHEADERSRETURN,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:InjectHeadersReturn)
  })
_sym_db.RegisterMessage(InjectHeadersReturn)

FinishSpanArgs = _reflection.GeneratedProtocolMessageType('FinishSpanArgs', (_message.Message,), {
  'DESCRIPTOR' : _FINISHSPANARGS,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:FinishSpanArgs)
  })
_sym_db.RegisterMessage(FinishSpanArgs)

FinishSpanReturn = _reflection.GeneratedProtocolMessageType('FinishSpanReturn', (_message.Message,), {
  'DESCRIPTOR' : _FINISHSPANRETURN,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:FinishSpanReturn)
  })
_sym_db.RegisterMessage(FinishSpanReturn)

SpanSetMetaArgs = _reflection.GeneratedProtocolMessageType('SpanSetMetaArgs', (_message.Message,), {
  'DESCRIPTOR' : _SPANSETMETAARGS,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:SpanSetMetaArgs)
  })
_sym_db.RegisterMessage(SpanSetMetaArgs)

SpanSetMetaReturn = _reflection.GeneratedProtocolMessageType('SpanSetMetaReturn', (_message.Message,), {
  'DESCRIPTOR' : _SPANSETMETARETURN,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:SpanSetMetaReturn)
  })
_sym_db.RegisterMessage(SpanSetMetaReturn)

SpanSetMetricArgs = _reflection.GeneratedProtocolMessageType('SpanSetMetricArgs', (_message.Message,), {
  'DESCRIPTOR' : _SPANSETMETRICARGS,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:SpanSetMetricArgs)
  })
_sym_db.RegisterMessage(SpanSetMetricArgs)

SpanSetMetricReturn = _reflection.GeneratedProtocolMessageType('SpanSetMetricReturn', (_message.Message,), {
  'DESCRIPTOR' : _SPANSETMETRICRETURN,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:SpanSetMetricReturn)
  })
_sym_db.RegisterMessage(SpanSetMetricReturn)

SpanSetErrorArgs = _reflection.GeneratedProtocolMessageType('SpanSetErrorArgs', (_message.Message,), {
  'DESCRIPTOR' : _SPANSETERRORARGS,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:SpanSetErrorArgs)
  })
_sym_db.RegisterMessage(SpanSetErrorArgs)

SpanSetErrorReturn = _reflection.GeneratedProtocolMessageType('SpanSetErrorReturn', (_message.Message,), {
  'DESCRIPTOR' : _SPANSETERRORRETURN,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:SpanSetErrorReturn)
  })
_sym_db.RegisterMessage(SpanSetErrorReturn)

FlushSpansArgs = _reflection.GeneratedProtocolMessageType('FlushSpansArgs', (_message.Message,), {
  'DESCRIPTOR' : _FLUSHSPANSARGS,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:FlushSpansArgs)
  })
_sym_db.RegisterMessage(FlushSpansArgs)

FlushSpansReturn = _reflection.GeneratedProtocolMessageType('FlushSpansReturn', (_message.Message,), {
  'DESCRIPTOR' : _FLUSHSPANSRETURN,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:FlushSpansReturn)
  })
_sym_db.RegisterMessage(FlushSpansReturn)

FlushTraceStatsArgs = _reflection.GeneratedProtocolMessageType('FlushTraceStatsArgs', (_message.Message,), {
  'DESCRIPTOR' : _FLUSHTRACESTATSARGS,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:FlushTraceStatsArgs)
  })
_sym_db.RegisterMessage(FlushTraceStatsArgs)

FlushTraceStatsReturn = _reflection.GeneratedProtocolMessageType('FlushTraceStatsReturn', (_message.Message,), {
  'DESCRIPTOR' : _FLUSHTRACESTATSRETURN,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:FlushTraceStatsReturn)
  })
_sym_db.RegisterMessage(FlushTraceStatsReturn)

OtelStartSpanArgs = _reflection.GeneratedProtocolMessageType('OtelStartSpanArgs', (_message.Message,), {
  'DESCRIPTOR' : _OTELSTARTSPANARGS,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:OtelStartSpanArgs)
  })
_sym_db.RegisterMessage(OtelStartSpanArgs)

OtelStartSpanReturn = _reflection.GeneratedProtocolMessageType('OtelStartSpanReturn', (_message.Message,), {
  'DESCRIPTOR' : _OTELSTARTSPANRETURN,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:OtelStartSpanReturn)
  })
_sym_db.RegisterMessage(OtelStartSpanReturn)

OtelEndSpanArgs = _reflection.GeneratedProtocolMessageType('OtelEndSpanArgs', (_message.Message,), {
  'DESCRIPTOR' : _OTELENDSPANARGS,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:OtelEndSpanArgs)
  })
_sym_db.RegisterMessage(OtelEndSpanArgs)

OtelEndSpanReturn = _reflection.GeneratedProtocolMessageType('OtelEndSpanReturn', (_message.Message,), {
  'DESCRIPTOR' : _OTELENDSPANRETURN,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:OtelEndSpanReturn)
  })
_sym_db.RegisterMessage(OtelEndSpanReturn)

OtelForceFlushArgs = _reflection.GeneratedProtocolMessageType('OtelForceFlushArgs', (_message.Message,), {
  'DESCRIPTOR' : _OTELFORCEFLUSHARGS,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:OtelForceFlushArgs)
  })
_sym_db.RegisterMessage(OtelForceFlushArgs)

OtelForceFlushReturn = _reflection.GeneratedProtocolMessageType('OtelForceFlushReturn', (_message.Message,), {
  'DESCRIPTOR' : _OTELFORCEFLUSHRETURN,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:OtelForceFlushReturn)
  })
_sym_db.RegisterMessage(OtelForceFlushReturn)

OtelFlushSpansArgs = _reflection.GeneratedProtocolMessageType('OtelFlushSpansArgs', (_message.Message,), {
  'DESCRIPTOR' : _OTELFLUSHSPANSARGS,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:OtelFlushSpansArgs)
  })
_sym_db.RegisterMessage(OtelFlushSpansArgs)

OtelFlushSpansReturn = _reflection.GeneratedProtocolMessageType('OtelFlushSpansReturn', (_message.Message,), {
  'DESCRIPTOR' : _OTELFLUSHSPANSRETURN,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:OtelFlushSpansReturn)
  })
_sym_db.RegisterMessage(OtelFlushSpansReturn)

OtelFlushTraceStatsArgs = _reflection.GeneratedProtocolMessageType('OtelFlushTraceStatsArgs', (_message.Message,), {
  'DESCRIPTOR' : _OTELFLUSHTRACESTATSARGS,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:OtelFlushTraceStatsArgs)
  })
_sym_db.RegisterMessage(OtelFlushTraceStatsArgs)

OtelFlushTraceStatsReturn = _reflection.GeneratedProtocolMessageType('OtelFlushTraceStatsReturn', (_message.Message,), {
  'DESCRIPTOR' : _OTELFLUSHTRACESTATSRETURN,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:OtelFlushTraceStatsReturn)
  })
_sym_db.RegisterMessage(OtelFlushTraceStatsReturn)

OtelStopTracerArgs = _reflection.GeneratedProtocolMessageType('OtelStopTracerArgs', (_message.Message,), {
  'DESCRIPTOR' : _OTELSTOPTRACERARGS,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:OtelStopTracerArgs)
  })
_sym_db.RegisterMessage(OtelStopTracerArgs)

OtelStopTracerReturn = _reflection.GeneratedProtocolMessageType('OtelStopTracerReturn', (_message.Message,), {
  'DESCRIPTOR' : _OTELSTOPTRACERRETURN,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:OtelStopTracerReturn)
  })
_sym_db.RegisterMessage(OtelStopTracerReturn)

OtelStartTracerArgs = _reflection.GeneratedProtocolMessageType('OtelStartTracerArgs', (_message.Message,), {
  'DESCRIPTOR' : _OTELSTARTTRACERARGS,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:OtelStartTracerArgs)
  })
_sym_db.RegisterMessage(OtelStartTracerArgs)

OtelStartTracerReturn = _reflection.GeneratedProtocolMessageType('OtelStartTracerReturn', (_message.Message,), {
  'DESCRIPTOR' : _OTELSTARTTRACERRETURN,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:OtelStartTracerReturn)
  })
_sym_db.RegisterMessage(OtelStartTracerReturn)

OtelIsRecordingArgs = _reflection.GeneratedProtocolMessageType('OtelIsRecordingArgs', (_message.Message,), {
  'DESCRIPTOR' : _OTELISRECORDINGARGS,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:OtelIsRecordingArgs)
  })
_sym_db.RegisterMessage(OtelIsRecordingArgs)

OtelIsRecordingReturn = _reflection.GeneratedProtocolMessageType('OtelIsRecordingReturn', (_message.Message,), {
  'DESCRIPTOR' : _OTELISRECORDINGRETURN,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:OtelIsRecordingReturn)
  })
_sym_db.RegisterMessage(OtelIsRecordingReturn)

OtelSpanContextArgs = _reflection.GeneratedProtocolMessageType('OtelSpanContextArgs', (_message.Message,), {
  'DESCRIPTOR' : _OTELSPANCONTEXTARGS,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:OtelSpanContextArgs)
  })
_sym_db.RegisterMessage(OtelSpanContextArgs)

OtelSpanContextReturn = _reflection.GeneratedProtocolMessageType('OtelSpanContextReturn', (_message.Message,), {
  'DESCRIPTOR' : _OTELSPANCONTEXTRETURN,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:OtelSpanContextReturn)
  })
_sym_db.RegisterMessage(OtelSpanContextReturn)

OtelSetStatusArgs = _reflection.GeneratedProtocolMessageType('OtelSetStatusArgs', (_message.Message,), {
  'DESCRIPTOR' : _OTELSETSTATUSARGS,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:OtelSetStatusArgs)
  })
_sym_db.RegisterMessage(OtelSetStatusArgs)

OtelSetStatusReturn = _reflection.GeneratedProtocolMessageType('OtelSetStatusReturn', (_message.Message,), {
  'DESCRIPTOR' : _OTELSETSTATUSRETURN,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:OtelSetStatusReturn)
  })
_sym_db.RegisterMessage(OtelSetStatusReturn)

OtelSetNameArgs = _reflection.GeneratedProtocolMessageType('OtelSetNameArgs', (_message.Message,), {
  'DESCRIPTOR' : _OTELSETNAMEARGS,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:OtelSetNameArgs)
  })
_sym_db.RegisterMessage(OtelSetNameArgs)

OtelSetNameReturn = _reflection.GeneratedProtocolMessageType('OtelSetNameReturn', (_message.Message,), {
  'DESCRIPTOR' : _OTELSETNAMERETURN,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:OtelSetNameReturn)
  })
_sym_db.RegisterMessage(OtelSetNameReturn)

OtelSetAttributesArgs = _reflection.GeneratedProtocolMessageType('OtelSetAttributesArgs', (_message.Message,), {
  'DESCRIPTOR' : _OTELSETATTRIBUTESARGS,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:OtelSetAttributesArgs)
  })
_sym_db.RegisterMessage(OtelSetAttributesArgs)

OtelSetAttributesReturn = _reflection.GeneratedProtocolMessageType('OtelSetAttributesReturn', (_message.Message,), {
  'DESCRIPTOR' : _OTELSETATTRIBUTESRETURN,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:OtelSetAttributesReturn)
  })
_sym_db.RegisterMessage(OtelSetAttributesReturn)

Attributes = _reflection.GeneratedProtocolMessageType('Attributes', (_message.Message,), {

  'KeyValsEntry' : _reflection.GeneratedProtocolMessageType('KeyValsEntry', (_message.Message,), {
    'DESCRIPTOR' : _ATTRIBUTES_KEYVALSENTRY,
    '__module__' : 'protos.apm_test_client_pb2'
    # @@protoc_insertion_point(class_scope:Attributes.KeyValsEntry)
    })
  ,
  'DESCRIPTOR' : _ATTRIBUTES,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:Attributes)
  })
_sym_db.RegisterMessage(Attributes)
_sym_db.RegisterMessage(Attributes.KeyValsEntry)

ListVal = _reflection.GeneratedProtocolMessageType('ListVal', (_message.Message,), {
  'DESCRIPTOR' : _LISTVAL,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:ListVal)
  })
_sym_db.RegisterMessage(ListVal)

AttrVal = _reflection.GeneratedProtocolMessageType('AttrVal', (_message.Message,), {
  'DESCRIPTOR' : _ATTRVAL,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:AttrVal)
  })
_sym_db.RegisterMessage(AttrVal)

StopTracerArgs = _reflection.GeneratedProtocolMessageType('StopTracerArgs', (_message.Message,), {
  'DESCRIPTOR' : _STOPTRACERARGS,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:StopTracerArgs)
  })
_sym_db.RegisterMessage(StopTracerArgs)

StopTracerReturn = _reflection.GeneratedProtocolMessageType('StopTracerReturn', (_message.Message,), {
  'DESCRIPTOR' : _STOPTRACERRETURN,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:StopTracerReturn)
  })
_sym_db.RegisterMessage(StopTracerReturn)

StartTracerArgs = _reflection.GeneratedProtocolMessageType('StartTracerArgs', (_message.Message,), {
  'DESCRIPTOR' : _STARTTRACERARGS,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:StartTracerArgs)
  })
_sym_db.RegisterMessage(StartTracerArgs)

StartTracerReturn = _reflection.GeneratedProtocolMessageType('StartTracerReturn', (_message.Message,), {
  'DESCRIPTOR' : _STARTTRACERRETURN,
  '__module__' : 'protos.apm_test_client_pb2'
  # @@protoc_insertion_point(class_scope:StartTracerReturn)
  })
_sym_db.RegisterMessage(StartTracerReturn)

_APMCLIENT = DESCRIPTOR.services_by_name['APMClient']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\024com.datadoghq.client'
  _ATTRIBUTES_KEYVALSENTRY._options = None
  _ATTRIBUTES_KEYVALSENTRY._serialized_options = b'8\001'
  _STARTSPANARGS._serialized_start=33
  _STARTSPANARGS._serialized_end=299
  _DISTRIBUTEDHTTPHEADERS._serialized_start=301
  _DISTRIBUTEDHTTPHEADERS._serialized_end=361
  _HEADERTUPLE._serialized_start=363
  _HEADERTUPLE._serialized_end=404
  _STARTSPANRETURN._serialized_start=406
  _STARTSPANRETURN._serialized_end=458
  _INJECTHEADERSARGS._serialized_start=460
  _INJECTHEADERSARGS._serialized_end=496
  _INJECTHEADERSRETURN._serialized_start=498
  _INJECTHEADERSRETURN._serialized_end=588
  _FINISHSPANARGS._serialized_start=590
  _FINISHSPANARGS._serialized_end=618
  _FINISHSPANRETURN._serialized_start=620
  _FINISHSPANRETURN._serialized_end=638
  _SPANSETMETAARGS._serialized_start=640
  _SPANSETMETAARGS._serialized_end=702
  _SPANSETMETARETURN._serialized_start=704
  _SPANSETMETARETURN._serialized_end=723
  _SPANSETMETRICARGS._serialized_start=725
  _SPANSETMETRICARGS._serialized_end=789
  _SPANSETMETRICRETURN._serialized_start=791
  _SPANSETMETRICRETURN._serialized_end=812
  _SPANSETERRORARGS._serialized_start=814
  _SPANSETERRORARGS._serialized_end=941
  _SPANSETERRORRETURN._serialized_start=943
  _SPANSETERRORRETURN._serialized_end=963
  _FLUSHSPANSARGS._serialized_start=965
  _FLUSHSPANSARGS._serialized_end=981
  _FLUSHSPANSRETURN._serialized_start=983
  _FLUSHSPANSRETURN._serialized_end=1001
  _FLUSHTRACESTATSARGS._serialized_start=1003
  _FLUSHTRACESTATSARGS._serialized_end=1024
  _FLUSHTRACESTATSRETURN._serialized_start=1026
  _FLUSHTRACESTATSRETURN._serialized_end=1049
  _OTELSTARTSPANARGS._serialized_start=1052
  _OTELSTARTSPANARGS._serialized_end=1435
  _OTELSTARTSPANRETURN._serialized_start=1437
  _OTELSTARTSPANRETURN._serialized_end=1493
  _OTELENDSPANARGS._serialized_start=1495
  _OTELENDSPANARGS._serialized_end=1562
  _OTELENDSPANRETURN._serialized_start=1564
  _OTELENDSPANRETURN._serialized_end=1583
  _OTELFORCEFLUSHARGS._serialized_start=1585
  _OTELFORCEFLUSHARGS._serialized_end=1622
  _OTELFORCEFLUSHRETURN._serialized_start=1624
  _OTELFORCEFLUSHRETURN._serialized_end=1663
  _OTELFLUSHSPANSARGS._serialized_start=1665
  _OTELFLUSHSPANSARGS._serialized_end=1702
  _OTELFLUSHSPANSRETURN._serialized_start=1704
  _OTELFLUSHSPANSRETURN._serialized_end=1743
  _OTELFLUSHTRACESTATSARGS._serialized_start=1745
  _OTELFLUSHTRACESTATSARGS._serialized_end=1770
  _OTELFLUSHTRACESTATSRETURN._serialized_start=1772
  _OTELFLUSHTRACESTATSRETURN._serialized_end=1799
  _OTELSTOPTRACERARGS._serialized_start=1801
  _OTELSTOPTRACERARGS._serialized_end=1821
  _OTELSTOPTRACERRETURN._serialized_start=1823
  _OTELSTOPTRACERRETURN._serialized_end=1845
  _OTELSTARTTRACERARGS._serialized_start=1847
  _OTELSTARTTRACERARGS._serialized_end=1912
  _OTELSTARTTRACERRETURN._serialized_start=1914
  _OTELSTARTTRACERRETURN._serialized_end=1937
  _OTELISRECORDINGARGS._serialized_start=1939
  _OTELISRECORDINGARGS._serialized_end=1977
  _OTELISRECORDINGRETURN._serialized_start=1979
  _OTELISRECORDINGRETURN._serialized_end=2024
  _OTELSPANCONTEXTARGS._serialized_start=2026
  _OTELSPANCONTEXTARGS._serialized_end=2064
  _OTELSPANCONTEXTRETURN._serialized_start=2066
  _OTELSPANCONTEXTRETURN._serialized_end=2182
  _OTELSETSTATUSARGS._serialized_start=2184
  _OTELSETSTATUSARGS._serialized_end=2255
  _OTELSETSTATUSRETURN._serialized_start=2257
  _OTELSETSTATUSRETURN._serialized_end=2278
  _OTELSETNAMEARGS._serialized_start=2280
  _OTELSETNAMEARGS._serialized_end=2328
  _OTELSETNAMERETURN._serialized_start=2330
  _OTELSETNAMERETURN._serialized_end=2349
  _OTELSETATTRIBUTESARGS._serialized_start=2351
  _OTELSETATTRIBUTESARGS._serialized_end=2424
  _OTELSETATTRIBUTESRETURN._serialized_start=2426
  _OTELSETATTRIBUTESRETURN._serialized_end=2451
  _ATTRIBUTES._serialized_start=2453
  _ATTRIBUTES._serialized_end=2567
  _ATTRIBUTES_KEYVALSENTRY._serialized_start=2511
  _ATTRIBUTES_KEYVALSENTRY._serialized_end=2567
  _LISTVAL._serialized_start=2569
  _LISTVAL._serialized_end=2601
  _ATTRVAL._serialized_start=2603
  _ATTRVAL._serialized_end=2706
  _STOPTRACERARGS._serialized_start=2708
  _STOPTRACERARGS._serialized_end=2724
  _STOPTRACERRETURN._serialized_start=2726
  _STOPTRACERRETURN._serialized_end=2744
  _STARTTRACERARGS._serialized_start=2746
  _STARTTRACERARGS._serialized_end=2807
  _STARTTRACERRETURN._serialized_start=2809
  _STARTTRACERRETURN._serialized_end=2828
  _APMCLIENT._serialized_start=2831
  _APMCLIENT._serialized_end=3986
# @@protoc_insertion_point(module_scope)
