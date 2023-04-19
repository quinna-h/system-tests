#!/bin/bash

# Unless explicitly stated otherwise all files in this repository are licensed under the the Apache License Version 2.0.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2021 Datadog, Inc.

set -eu

FIRST_ARGUMENT=${1:-DEFAULT}
if [[ $FIRST_ARGUMENT =~ ^[A-Z0-9_]+$ ]]; then
    export SYSTEMTESTS_SCENARIO=$FIRST_ARGUMENT
    export RUNNER_ARGS="tests/"
else
    # Let user choose the target
    export SYSTEMTESTS_SCENARIO="CUSTOM"
    export RUNNER_ARGS=$@
fi

# clean any pycache folder
find utils tests -type d -name '__pycache__'  -prune -exec rm -rf {} +

if [[ -z "$IN_NIX_SHELL" ]]; then
   source venv/bin/activate
fi

pytest $RUNNER_ARGS
