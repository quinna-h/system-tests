from utils import weblog, interfaces, scenarios, features, rfc
from utils._context.header_tag_vars import *


@rfc("https://docs.google.com/document/d/12NBx-nD-IoQEMiCRnJXneq4Be7cbtSc6pJLOFUWTpNE/edit")
@features.appsec_standalone
@scenarios.appsec_standalone
class Test_AppSecStandalone_UpstreamPropagation:
    """APM correctly propagates AppSec events in distributing tracing."""

    # TODO downstream propagation

    def setup_no_appsec_upstream__no_attack__is_kept_with_priority_1__from_minus_1(self):
        trace_id = 1212121212121212121
        parent_id = 34343434
        self.r = weblog.get(
            "/requestdownstream/?url=http%3A%2F%2Flocalhost%3A7777%2Fwaf%2F",
            headers={
                "x-datadog-trace-id": str(trace_id),
                "x-datadog-parent-id": str(parent_id),
                "x-datadog-sampling-priority": "-1",
                "x-datadog-origin": "rum",
                "x-datadog-tags": "_dd.p.other=1",
            },
        )

    def test_no_appsec_upstream__no_attack__is_kept_with_priority_1__from_minus_1(self):
        for data, _, span in interfaces.library.get_spans(request=self.r):
            assert span["metrics"]["_sampling_priority_v1"] < 2
            assert span["metrics"]["_dd.apm.enabled"] == 0
            assert "_dd.p.appsec" not in span["meta"]
            assert "_dd.p.other" in span["meta"]
            assert span["trace_id"] == 1212121212121212121

            # Some tracers use true while others use yes
            assert any(
                ["Datadog-Client-Computed-Stats", trueish,] in data["request"]["headers"] for trueish in ["yes", "true"]
            )

    def setup_no_appsec_upstream__no_attack__is_kept_with_priority_1__from_0(self):
        trace_id = 1212121212121212121
        parent_id = 34343434
        self.r = weblog.get(
            "/waf/",
            headers={
                "x-datadog-trace-id": str(trace_id),
                "x-datadog-parent-id": str(parent_id),
                "x-datadog-sampling-priority": "0",
                "x-datadog-origin": "rum",
                "x-datadog-tags": "_dd.p.other=1",
            },
        )

    def test_no_appsec_upstream__no_attack__is_kept_with_priority_1__from_0(self):
        for data, _, span in interfaces.library.get_spans(request=self.r):
            assert span["metrics"]["_sampling_priority_v1"] < 2
            assert span["metrics"]["_dd.apm.enabled"] == 0
            assert "_dd.p.appsec" not in span["meta"]
            assert "_dd.p.other" in span["meta"]
            assert span["trace_id"] == 1212121212121212121

            # Some tracers use true while others use yes
            assert any(
                ["Datadog-Client-Computed-Stats", trueish,] in data["request"]["headers"] for trueish in ["yes", "true"]
            )

    def setup_no_appsec_upstream__no_attack__is_kept_with_priority_1__from_1(self):
        trace_id = 1212121212121212121
        parent_id = 34343434
        self.r = weblog.get(
            "/waf/",
            headers={
                "x-datadog-trace-id": str(trace_id),
                "x-datadog-parent-id": str(parent_id),
                "x-datadog-sampling-priority": "1",
                "x-datadog-origin": "rum",
                "x-datadog-tags": "_dd.p.other=1",
            },
        )

    def test_no_appsec_upstream__no_attack__is_kept_with_priority_1__from_1(self):
        for data, _, span in interfaces.library.get_spans(request=self.r):
            assert span["metrics"]["_sampling_priority_v1"] < 2
            assert span["metrics"]["_dd.apm.enabled"] == 0
            assert "_dd.p.appsec" not in span["meta"]
            assert "_dd.p.other" in span["meta"]
            assert span["trace_id"] == 1212121212121212121

            # Some tracers use true while others use yes
            assert any(
                ["Datadog-Client-Computed-Stats", trueish,] in data["request"]["headers"] for trueish in ["yes", "true"]
            )

    def setup_no_appsec_upstream__no_attack__is_kept_with_priority_1__from_2(self):
        trace_id = 1212121212121212121
        parent_id = 34343434
        self.r = weblog.get(
            "/waf/",
            headers={
                "x-datadog-trace-id": str(trace_id),
                "x-datadog-parent-id": str(parent_id),
                "x-datadog-sampling-priority": "2",
                "x-datadog-origin": "rum",
                "x-datadog-tags": "_dd.p.other=1",
            },
        )

    def test_no_appsec_upstream__no_attack__is_kept_with_priority_1__from_2(self):
        for data, _, span in interfaces.library.get_spans(request=self.r):
            assert span["metrics"]["_sampling_priority_v1"] < 2
            assert span["metrics"]["_dd.apm.enabled"] == 0
            assert "_dd.p.appsec" not in span["meta"]
            assert "_dd.p.other" in span["meta"]
            assert span["trace_id"] == 1212121212121212121

            # Some tracers use true while others use yes
            assert any(
                ["Datadog-Client-Computed-Stats", trueish,] in data["request"]["headers"] for trueish in ["yes", "true"]
            )

    def setup_no_upstream_appsec_propagation__with_attack__is_kept_with_priority_2__from_minus_1(self):
        trace_id = 1212121212121212121
        parent_id = 34343434
        self.r = weblog.get(
            "/requestdownstream/?url=http%3A%2F%2Flocalhost%3A7777%2Fwaf%2F",
            headers={
                "x-datadog-trace-id": str(trace_id),
                "x-datadog-parent-id": str(parent_id),
                "x-datadog-origin": "rum",
                "x-datadog-sampling-priority": "-1",
                "x-datadog-tags": "_dd.p.other=1",
                "User-Agent": "Arachni/v1",
            },
        )

    def test_no_upstream_appsec_propagation__with_attack__is_kept_with_priority_2__from_minus_1(self):
        for data, _, span in interfaces.library.get_spans(request=self.r):
            import pdb

            pdb.set_trace()
            assert data["request"]["content"][0][0]["meta"]["_dd.appsec.s.req.headers"][0]["user-agent"][0] != 8

            assert span["metrics"]["_sampling_priority_v1"] == 2
            assert span["metrics"]["_dd.apm.enabled"] == 0
            assert span["meta"]["_dd.p.appsec"] == "1"
            assert span["trace_id"] == 1212121212121212121

            # Some tracers use true while others use yes
            assert any(
                ["Datadog-Client-Computed-Stats", trueish,] in data["request"]["headers"] for trueish in ["yes", "true"]
            )

    def setup_no_upstream_appsec_propagation__with_attack__is_kept_with_priority_2__from_0(self):
        trace_id = 1212121212121212121
        parent_id = 34343434
        self.r = weblog.get(
            "/waf/",
            headers={
                "x-datadog-trace-id": str(trace_id),
                "x-datadog-parent-id": str(parent_id),
                "x-datadog-origin": "rum",
                "x-datadog-sampling-priority": "0",
                "x-datadog-tags": "_dd.p.other=1",
                "User-Agent": "Arachni/v1",
            },
        )

    def test_no_upstream_appsec_propagation__with_attack__is_kept_with_priority_2__from_0(self):
        for data, _, span in interfaces.library.get_spans(request=self.r):
            assert span["metrics"]["_sampling_priority_v1"] == 2
            assert span["metrics"]["_dd.apm.enabled"] == 0
            assert span["meta"]["_dd.p.appsec"] == "1"
            assert span["trace_id"] == 1212121212121212121

            # Some tracers use true while others use yes
            assert any(
                ["Datadog-Client-Computed-Stats", trueish,] in data["request"]["headers"] for trueish in ["yes", "true"]
            )

    def setup_upstream_appsec_propagation__no_attack__is_propagated_as_is__being_0(self):
        trace_id = 1212121212121212121
        parent_id = 34343434
        self.r = weblog.get(
            "/waf/",
            headers={
                "x-datadog-trace-id": str(trace_id),
                "x-datadog-parent-id": str(parent_id),
                "x-datadog-origin": "rum",
                "x-datadog-sampling-priority": "0",
                "x-datadog-tags": "_dd.p.appsec=1",
            },
        )

    def test_upstream_appsec_propagation__no_attack__is_propagated_as_is__being_0(self):
        for data, _, span in interfaces.library.get_spans(request=self.r):
            assert span["metrics"]["_sampling_priority_v1"] == 2
            assert span["metrics"]["_dd.apm.enabled"] == 0
            assert span["meta"]["_dd.p.appsec"] == "1"
            assert span["trace_id"] == 1212121212121212121

            # Some tracers use true while others use yes
            assert any(
                ["Datadog-Client-Computed-Stats", trueish,] in data["request"]["headers"] for trueish in ["yes", "true"]
            )

    def setup_upstream_appsec_propagation__no_attack__is_propagated_as_is__being_1(self):
        trace_id = 1212121212121212121
        parent_id = 34343434
        self.r = weblog.get(
            "/waf/",
            headers={
                "x-datadog-trace-id": str(trace_id),
                "x-datadog-parent-id": str(parent_id),
                "x-datadog-origin": "rum",
                "x-datadog-sampling-priority": "1",
                "x-datadog-tags": "_dd.p.appsec=1",
            },
        )

    def test_upstream_appsec_propagation__no_attack__is_propagated_as_is__being_1(self):
        for data, _, span in interfaces.library.get_spans(request=self.r):
            assert span["metrics"]["_sampling_priority_v1"] == 2
            assert span["metrics"]["_dd.apm.enabled"] == 0
            assert span["meta"]["_dd.p.appsec"] == "1"
            assert span["trace_id"] == 1212121212121212121

            # Some tracers use true while others use yes
            assert any(
                ["Datadog-Client-Computed-Stats", trueish,] in data["request"]["headers"] for trueish in ["yes", "true"]
            )

    def setup_upstream_appsec_propagation__no_attack__is_propagated_as_is__being_2(self):
        trace_id = 1212121212121212121
        parent_id = 34343434
        self.r = weblog.get(
            "/requestdownstream/?url=http%3A%2F%2Flocalhost%3A7777%2Fwaf%2F",
            headers={
                "x-datadog-trace-id": str(trace_id),
                "x-datadog-parent-id": str(parent_id),
                "x-datadog-origin": "rum",
                "x-datadog-sampling-priority": "2",
                "x-datadog-tags": "_dd.p.appsec=1",
            },
        )

    def test_upstream_appsec_propagation__no_attack__is_propagated_as_is__being_2(self):
        for data, _, span in interfaces.library.get_spans(request=self.r):
            assert span["metrics"]["_sampling_priority_v1"] == 2
            assert span["metrics"]["_dd.apm.enabled"] == 0
            assert span["meta"]["_dd.p.appsec"] == "1"
            assert span["trace_id"] == 1212121212121212121

            # Some tracers use true while others use yes
            assert any(
                ["Datadog-Client-Computed-Stats", trueish,] in data["request"]["headers"] for trueish in ["yes", "true"]
            )

    def setup_any_upstream_propagation__with_attack__raises_priority_to_2__from_minus_1(self):
        trace_id = 1212121212121212121
        parent_id = 34343434
        self.r = weblog.get(
            "/requestdownstream/?url=http%3A%2F%2Flocalhost%3A7777%2Fwaf%2F",
            headers={
                "x-datadog-trace-id": str(trace_id),
                "x-datadog-parent-id": str(parent_id),
                "x-datadog-origin": "rum",
                "x-datadog-sampling-priority": "-1",
                "User-Agent": "Arachni/v1",
            },
        )

    def test_any_upstream_propagation__with_attack__raises_priority_to_2__from_minus_1(self):
        for data, _, span in interfaces.library.get_spans(request=self.r):
            assert span["metrics"]["_sampling_priority_v1"] == 2
            assert span["metrics"]["_dd.apm.enabled"] == 0
            assert span["meta"]["_dd.p.appsec"] == "1"
            assert span["trace_id"] == 1212121212121212121

            # Some tracers use true while others use yes
            assert any(
                ["Datadog-Client-Computed-Stats", trueish,] in data["request"]["headers"] for trueish in ["yes", "true"]
            )

    def setup_any_upstream_propagation__with_attack__raises_priority_to_2__from_0(self):
        trace_id = 1212121212121212121
        parent_id = 34343434
        self.r = weblog.get(
            "/waf/",
            headers={
                "x-datadog-trace-id": str(trace_id),
                "x-datadog-parent-id": str(parent_id),
                "x-datadog-origin": "rum",
                "x-datadog-sampling-priority": "0",
                "User-Agent": "Arachni/v1",
            },
        )

    def test_any_upstream_propagation__with_attack__raises_priority_to_2__from_0(self):
        for data, _, span in interfaces.library.get_spans(request=self.r):
            assert span["metrics"]["_sampling_priority_v1"] == 2
            assert span["metrics"]["_dd.apm.enabled"] == 0
            assert span["meta"]["_dd.p.appsec"] == "1"
            assert span["trace_id"] == 1212121212121212121

            # Some tracers use true while others use yes
            assert any(
                ["Datadog-Client-Computed-Stats", trueish,] in data["request"]["headers"] for trueish in ["yes", "true"]
            )

    def setup_any_upstream_propagation__with_attack__raises_priority_to_2__from_1(self):
        trace_id = 1212121212121212121
        parent_id = 34343434
        self.r = weblog.get(
            "/waf/",
            headers={
                "x-datadog-trace-id": str(trace_id),
                "x-datadog-parent-id": str(parent_id),
                "x-datadog-origin": "rum",
                "x-datadog-sampling-priority": "0",
                "User-Agent": "Arachni/v1",
            },
        )

    def test_any_upstream_propagation__with_attack__raises_priority_to_2__from_1(self):
        for data, _, span in interfaces.library.get_spans(request=self.r):
            assert span["metrics"]["_sampling_priority_v1"] == 2
            assert span["metrics"]["_dd.apm.enabled"] == 0
            assert span["meta"]["_dd.p.appsec"] == "1"
            assert span["trace_id"] == 1212121212121212121

            # Some tracers use true while others use yes
            assert any(
                ["Datadog-Client-Computed-Stats", trueish,] in data["request"]["headers"] for trueish in ["yes", "true"]
            )
