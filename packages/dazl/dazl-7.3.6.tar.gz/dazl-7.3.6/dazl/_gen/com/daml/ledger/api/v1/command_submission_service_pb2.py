# Copyright (c) 2017-2021 Digital Asset (Switzerland) GmbH and/or its affiliates. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: com/daml/ledger/api/v1/command_submission_service.proto

from google.protobuf import (
    descriptor as _descriptor,
    message as _message,
    reflection as _reflection,
    symbol_database as _symbol_database,
)

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2

from . import (
    commands_pb2 as com_dot_daml_dot_ledger_dot_api_dot_v1_dot_commands__pb2,
    trace_context_pb2 as com_dot_daml_dot_ledger_dot_api_dot_v1_dot_trace__context__pb2,
)

DESCRIPTOR = _descriptor.FileDescriptor(
    name="com/daml/ledger/api/v1/command_submission_service.proto",
    package="com.daml.ledger.api.v1",
    syntax="proto3",
    serialized_options=b'\n\026com.daml.ledger.api.v1B"CommandSubmissionServiceOuterClass\252\002\026Com.Daml.Ledger.Api.V1',
    create_key=_descriptor._internal_create_key,
    serialized_pb=b'\n7com/daml/ledger/api/v1/command_submission_service.proto\x12\x16\x63om.daml.ledger.api.v1\x1a*com/daml/ledger/api/v1/trace_context.proto\x1a%com/daml/ledger/api/v1/commands.proto\x1a\x1bgoogle/protobuf/empty.proto"\x81\x01\n\rSubmitRequest\x12\x32\n\x08\x63ommands\x18\x01 \x01(\x0b\x32 .com.daml.ledger.api.v1.Commands\x12<\n\rtrace_context\x18\xe8\x07 \x01(\x0b\x32$.com.daml.ledger.api.v1.TraceContext2c\n\x18\x43ommandSubmissionService\x12G\n\x06Submit\x12%.com.daml.ledger.api.v1.SubmitRequest\x1a\x16.google.protobuf.EmptyBU\n\x16\x63om.daml.ledger.api.v1B"CommandSubmissionServiceOuterClass\xaa\x02\x16\x43om.Daml.Ledger.Api.V1b\x06proto3',
    dependencies=[
        com_dot_daml_dot_ledger_dot_api_dot_v1_dot_trace__context__pb2.DESCRIPTOR,
        com_dot_daml_dot_ledger_dot_api_dot_v1_dot_commands__pb2.DESCRIPTOR,
        google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,
    ],
)


_SUBMITREQUEST = _descriptor.Descriptor(
    name="SubmitRequest",
    full_name="com.daml.ledger.api.v1.SubmitRequest",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="commands",
            full_name="com.daml.ledger.api.v1.SubmitRequest.commands",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="trace_context",
            full_name="com.daml.ledger.api.v1.SubmitRequest.trace_context",
            index=1,
            number=1000,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=196,
    serialized_end=325,
)

_SUBMITREQUEST.fields_by_name[
    "commands"
].message_type = com_dot_daml_dot_ledger_dot_api_dot_v1_dot_commands__pb2._COMMANDS
_SUBMITREQUEST.fields_by_name[
    "trace_context"
].message_type = com_dot_daml_dot_ledger_dot_api_dot_v1_dot_trace__context__pb2._TRACECONTEXT
DESCRIPTOR.message_types_by_name["SubmitRequest"] = _SUBMITREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SubmitRequest = _reflection.GeneratedProtocolMessageType(
    "SubmitRequest",
    (_message.Message,),
    {
        "DESCRIPTOR": _SUBMITREQUEST,
        "__module__": "com.daml.ledger.api.v1.command_submission_service_pb2"
        # @@protoc_insertion_point(class_scope:com.daml.ledger.api.v1.SubmitRequest)
    },
)
_sym_db.RegisterMessage(SubmitRequest)


DESCRIPTOR._options = None

_COMMANDSUBMISSIONSERVICE = _descriptor.ServiceDescriptor(
    name="CommandSubmissionService",
    full_name="com.daml.ledger.api.v1.CommandSubmissionService",
    file=DESCRIPTOR,
    index=0,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
    serialized_start=327,
    serialized_end=426,
    methods=[
        _descriptor.MethodDescriptor(
            name="Submit",
            full_name="com.daml.ledger.api.v1.CommandSubmissionService.Submit",
            index=0,
            containing_service=None,
            input_type=_SUBMITREQUEST,
            output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
            serialized_options=None,
            create_key=_descriptor._internal_create_key,
        ),
    ],
)
_sym_db.RegisterServiceDescriptor(_COMMANDSUBMISSIONSERVICE)

DESCRIPTOR.services_by_name["CommandSubmissionService"] = _COMMANDSUBMISSIONSERVICE

# @@protoc_insertion_point(module_scope)
