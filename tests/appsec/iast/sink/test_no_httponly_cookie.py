# Unless explicitly stated otherwise all files in this repository are licensed under the the Apache License Version 2.0.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2021 Datadog, Inc.

from utils import context, missing_feature, bug, weblog, features
from ..utils import BaseSinkTest, BaseSinkTestWithoutTelemetry, BaseTestCookieNameFilter


@features.iast_sink_http_only_cookie
class TestNoHttponlyCookie(BaseSinkTest):
    """Test no HttpOnly cookie detection."""

    vulnerability_type = "NO_HTTPONLY_COOKIE"
    http_method = "GET"
    insecure_endpoint = "/iast/no-httponly-cookie/test_insecure"
    secure_endpoint = "/iast/no-httponly-cookie/test_secure"
    data = {}
    location_map = {"nodejs": {"express4": "iast/index.js", "express4-typescript": "iast.ts"}}

    @bug(context.library < "java@1.18.3", reason="APMRP-360")
    def test_secure(self):
        super().test_secure()

    def setup_empty_cookie(self):
        self.request_empty_cookie = weblog.get("/iast/no-httponly-cookie/test_empty_cookie", data={})

    def test_empty_cookie(self):
        self.assert_no_iast_event(self.request_empty_cookie)

    @missing_feature(context.library < "java@1.22.0", reason="Metrics not implemented")
    @missing_feature(library="python", reason="Metrics not implemented")
    @missing_feature(library="dotnet", reason="Metrics not implemented")
    def test_telemetry_metric_instrumented_sink(self):
        super().test_telemetry_metric_instrumented_sink()

    @missing_feature(context.library < "java@1.22.0", reason="Metric not implemented")
    @missing_feature(weblog_variant="vertx4", reason="Metric not implemented")
    def test_telemetry_metric_executed_sink(self):
        super().test_telemetry_metric_executed_sink()


@features.iast_sink_http_only_cookie
class TestNoHttponlyCookieNameFilter(BaseTestCookieNameFilter):
    """Test no HttpOnly cookie name filter."""

    vulnerability_type = "NO_HTTPONLY_COOKIE"
    endpoint = "/iast/no-httponly-cookie/custom_cookie"
