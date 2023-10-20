# Unless explicitly stated otherwise all files in this repository are licensed under the the Apache License Version 2.0.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2021 Datadog, Inc.

from utils import context, coverage, missing_feature, bug
from .._test_iast_fixtures import BaseSourceTest


@coverage.basic
class TestParameterValue(BaseSourceTest):
    """Verify that request parameters are tainted"""

    endpoint = "/iast/source/parameter/test"
    requests_kwargs = [
        {"method": "GET", "params": {"table": "user"}},
        {"method": "POST", "data": {"table": "user"}},
    ]
    # In test case in node, the value is redacted
    source_value = None if context.library.library == "nodejs" else "user"
    source_type = "http.request.body" if context.library.library == "nodejs" else "http.request.parameter"
    source_name = "table"

    def test_source_reported(self):
        # overwrite the base test, to handle the source_type spcial use case in node
        ...

    @bug(weblog_variant="jersey-grizzly2", reason="name field of source not set")
    @bug(library="python", reason="Python frameworks need a header, if not, 415 status code")
    def test_source_post_reported(self):
        self.validate_request_reported(self.requests["POST"])

    @bug(weblog_variant="jersey-grizzly2", reason="name field of source not set")
    def test_source_get_reported(self):
        self.validate_request_reported(self.requests["GET"], source_type="http.request.parameter")

    @missing_feature(context.library < "java@1.13.0", reason="Not implemented")
    @missing_feature(
        context.library == "java" and not context.weblog_variant.startswith("spring-boot"), reason="Not implemented"
    )
    @missing_feature(library="nodejs", reason="Not implemented")
    def test_telemetry_metric_instrumented_source(self):
        super().test_telemetry_metric_instrumented_source()

    @missing_feature(context.library < "java@1.13.0", reason="Not implemented")
    @missing_feature(
        context.library == "java" and not context.weblog_variant.startswith("spring-boot"), reason="Not implemented"
    )
    @missing_feature(library="nodejs", reason="Not implemented")
    def test_telemetry_metric_executed_source(self):
        super().test_telemetry_metric_executed_source()
