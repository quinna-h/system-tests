import time
from urllib.parse import urlparse

from utils import scenarios, features, context, irrelevant, bug, interfaces
from utils import weblog
from utils.tools import logger, get_rid_from_request


@scenarios.docker_ssi
class TestDockerSSIFeatures:
    """ Test the ssi in a simulated host injection environment (docker container + test agent) 
    We test that the injection is performed and traces and telemetry are generated. 
    If the language version is not supported, we only check that we don't break the app and telemetry is generated."""

    _r = None

    def _setup_all(self):
        if TestDockerSSIFeatures._r is None:
            parsed_url = urlparse(context.scenario.weblog_url)
            TestDockerSSIFeatures._r = weblog.request(
                "GET", parsed_url.path, domain=parsed_url.hostname, port=parsed_url.port
            )
            logger.info(f"Setup Docker SSI installation {TestDockerSSIFeatures._r}")

        self.r = TestDockerSSIFeatures._r

    def setup_install_supported_runtime(self):
        self._setup_all()

    @features.ssi_guardrails
    @bug(
        condition="centos-7" in context.weblog_variant and context.library == "java", reason="APMON-1490",
    )
    @irrelevant(context.library == "java" and context.installed_language_runtime < "1.8")
    def test_install_supported_runtime(self):
        logger.info(f"Testing Docker SSI installation on supported lang runtime: {context.scenario.library.library}")
        assert self.r.status_code == 200, f"Failed to get response from {context.scenario.weblog_url}"

        # If the language version is supported there are traces related with the request
        traces_for_request = interfaces.test_agent.get_traces(request=self.r)
        assert traces_for_request, f"No traces found for request {get_rid_from_request(self.r)}"
        assert "runtime-id" in traces_for_request["meta"], "No runtime-id found in traces"

        # There is telemetry data related with the runtime-id
        telemetry_data = interfaces.test_agent.get_telemetry_for_runtime(traces_for_request["meta"]["runtime-id"])
        assert telemetry_data, "No telemetry data found"

    def setup_install_weblog_running(self):
        self._setup_all()

    @features.ssi_guardrails
    @bug(
        condition="centos-7" in context.scenario.weblog_variant and context.scenario.library.library == "java",
        reason="APMON-1490",
    )
    def test_install_weblog_running(self):
        logger.info(
            f"Testing Docker SSI installation. The weblog should be running: {context.scenario.library.library}"
        )
        assert self.r.status_code == 200, f"Failed to get response from {context.scenario.weblog_url}"

        # There is telemetry data about the auto instrumentation. We only validate there is data
        telemetry_autoinject_data = interfaces.test_agent.get_telemetry_for_autoinject()
        assert len(telemetry_autoinject_data) >= 1
        for data in telemetry_autoinject_data:
            assert data["metric"] == "inject.success"

    def setup_service_name(self):
        self._setup_all()

    @features.ssi_service_naming
    @irrelevant(condition=not context.weblog_variant.startswith("tomcat-app"))
    def test_service_name(self):
        logger.info("Testing Docker SSI service name")
        # There are traces related with the request and the service name is payment-service
        traces_for_request = interfaces.test_agent.get_traces(request=self.r)
        assert traces_for_request, f"No traces found for request {get_rid_from_request(self.r)}"
        assert "service" in traces_for_request, "No service name found in traces"
        assert (
            traces_for_request["service"] == "payment-service"
        ), f"Service name is not payment-service but {traces_for_request['service']}"