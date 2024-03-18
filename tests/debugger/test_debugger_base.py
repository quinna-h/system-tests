# Unless explicitly stated otherwise all files in this repository are licensed under the the Apache License Version 2.0.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2021 Datadog, Inc.

from utils import scenarios, interfaces, weblog, features, missing_feature, context
from utils.tools import logger


def validate_probes(expected_probes):
    def get_probes_map():
        agent_logs_endpoint_requests = list(interfaces.agent.get_data(path_filters="/api/v2/logs"))
        probe_hash = {}

        for request in agent_logs_endpoint_requests:
            content = request["request"]["content"]
            if content is not None:
                for content in content:
                    debugger = content["debugger"]
                    if "diagnostics" in debugger:
                        probe_id = debugger["diagnostics"]["probeId"]
                        probe_hash[probe_id] = debugger["diagnostics"]

        return probe_hash

    def check_probe_status(expected_id, expected_status, probe_status_map):
        if expected_id not in probe_status_map:
            raise ValueError("Probe " + expected_id + " was not received.")

        actual_status = probe_status_map[expected_id]["status"]
        if actual_status != expected_status:
            raise ValueError(
                "Received probe "
                + expected_id
                + " with status "
                + actual_status
                + ", but expected for "
                + expected_status
            )

    probe_map = get_probes_map()
    for expected_id, expected_status in expected_probes.items():
        check_probe_status(expected_id, expected_status, probe_map)


def validate_snapshots(expected_snapshots):
    def get_snapshot_map():
        agent_logs_endpoint_requests = list(interfaces.agent.get_data(path_filters="/api/v2/logs"))
        snapshot_hash = {}

        for request in agent_logs_endpoint_requests:
            content = request["request"]["content"]
            if content is not None:
                for content in content:
                    debugger = content["debugger"]
                    if "snapshot" in debugger:
                        probe_id = debugger["snapshot"]["probe"]["id"]
                        snapshot_hash[probe_id] = debugger["snapshot"]

        return snapshot_hash

    def check_snapshot(expected_id, snapshot_status_map):
        if expected_id not in snapshot_status_map:
            raise ValueError("Snapshot " + expected_id + " was not received.")

    snapshot_map = get_snapshot_map()
    for expected_snapshot in expected_snapshots:
        check_snapshot(expected_snapshot, snapshot_map)


def validate_spans(expected_spans):
    def get_span_map():
        agent_logs_endpoint_requests = list(interfaces.agent.get_data(path_filters="/api/v0.2/traces"))
        span_hash = {}
        for request in agent_logs_endpoint_requests:
            content = request["request"]["content"]
            if content is not None:
                for payload in content["tracerPayloads"]:
                    for chunk in payload["chunks"]:
                        for span in chunk["spans"]:
                            if span["name"] == "dd.dynamic.span":
                                span_hash[span["meta"]["debugger.probeid"]] = span
                            else:
                                for key, value in span["meta"].items():
                                    if key.startswith("_dd.di"):
                                        span_hash[value] = span["meta"][key.split(".")[2]]

        return span_hash

    def check_trace(expected_id, trace_map):
        if expected_id not in trace_map:
            raise ValueError("Trace " + expected_id + " was not received.")

    span_map = get_span_map()
    for expected_trace in expected_spans:
        check_trace(expected_trace, span_map)


class _Base_Debugger_Snapshot_Test:
    expected_probe_ids = []

    def assert_remote_config_is_sent(self):
        for data in interfaces.library.get_data("/v0.7/config"):
            logger.debug(f"Found config in {data['log_filename']}")
            if "client_configs" in data.get("response", {}).get("content", {}):
                return

        raise ValueError("I was expecting a remote config")

    def _is_all_probes_installed(self, data):
        contents = data.get("request", {}).get("content", [])

        if contents is None:
            return False

        installed_ids = set()
        for content in contents:
            diagnostics = content.get("debugger", {}).get("diagnostics", {})
            if diagnostics.get("status") == "INSTALLED":
                installed_ids.add(diagnostics.get("probeId"))

        logger.debug(f"Found probes in {data['log_filename']}:\n    {installed_ids}")

        if set(self.expected_probe_ids).issubset(installed_ids):
            logger.debug(f"Succes: found probes {installed_ids}")
            return True

        missings_ids = set(self.expected_probe_ids) - set(installed_ids)

        logger.debug(f"Found some probes, but not all of them. Missing probes are {missings_ids}")

    def assert_all_probes_are_installed(self):
        logger.debug(f"Checking if I found all my probes:\n    {self.expected_probe_ids}")
        for data in interfaces.agent.get_data("/api/v2/logs"):
            if self._is_all_probes_installed(data):
                return

        raise ValueError("At least one probe is missing")

    def wait_for_all_probes_installed(self, data):
        if data["path"] == "/api/v2/logs":
            if self._is_all_probes_installed(data):
                return True

        return False
