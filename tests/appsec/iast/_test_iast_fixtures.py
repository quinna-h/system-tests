import json
from utils import weblog, interfaces, context
from utils.tools import logging


def _get_expectation(d):
    if d is None:
        return None
    if isinstance(d, str):
        return d
    elif callable(d):
        return d()
    else:
        expected = d.get(context.library.library)
        if isinstance(expected, dict):
            expected = expected.get(context.weblog_variant)
        return expected


def _get_span_meta(request):
    spans = [span for _, span in interfaces.library.get_root_spans(request=request)]
    assert spans, "No root span found"
    span = spans[0]
    meta = span.get("meta", {})
    return meta


def get_iast_event(request):
    meta = _get_span_meta(request=request)
    assert "_dd.iast.json" in meta, "No _dd.iast.json tag in span"
    return meta["_dd.iast.json"]


def assert_iast_vulnerability(
    request, vulnerability_count=1, vulnerability_type=None, expected_location=None, expected_evidence=None
):
    iast = get_iast_event(request=request)
    assert iast["vulnerabilities"], "Expected at least one vulnerability"
    vulns = iast["vulnerabilities"]
    if vulnerability_type:
        vulns = [v for v in vulns if v["type"] == vulnerability_type]
        assert vulns, f"No vulnerability of type {vulnerability_type}"
    if expected_location:
        vulns = [v for v in vulns if v.get("location", {}).get("path", "") == expected_location]
        assert vulns, f"No vulnerability with location {expected_location}"
    if expected_evidence:
        vulns = [v for v in vulns if v.get("evidence", {}).get("value", "") == expected_evidence]
        assert vulns, f"No vulnerability with evidence value {expected_evidence}"
    assert len(vulns) == vulnerability_count


def _check_telemetry_response_from_agent():
    # Java tracer (at least) disable telemetry if agent answer 403
    # Checking that agent answers 200
    # we do not fail the test, because we are not sure it's the official behavior
    for data in interfaces.library.get_telemetry_data():
        code = data["response"]["status_code"]
        if code != 200:
            filename = data["log_filename"]
            logging.warning(f"Agent answered {code} on {filename}, it may cause telemetry issues")
            return


class SinkFixture:
    def __init__(
        self,
        vulnerability_type,
        http_method,
        insecure_endpoint,
        secure_endpoint,
        data,
        location_map=None,
        evidence_map=None,
    ):
        self.vulnerability_type = vulnerability_type
        self.http_method = http_method
        self.insecure_endpoint = insecure_endpoint
        self.secure_endpoint = secure_endpoint
        self.data = data
        self.expected_location = _get_expectation(location_map)
        self.expected_evidence = _get_expectation(evidence_map)
        self.insecure_request = None
        self.secure_request = None

    def setup_insecure(self):
        if self.insecure_request is None:
            self.insecure_request = weblog.request(method=self.http_method, path=self.insecure_endpoint, data=self.data)

    def test_insecure(self):
        assert_iast_vulnerability(
            request=self.insecure_request,
            vulnerability_count=1,
            vulnerability_type=self.vulnerability_type,
            expected_location=self.expected_location,
            expected_evidence=self.expected_evidence,
        )

    def setup_secure(self):
        if self.secure_request is None:
            self.secure_request = weblog.request(method=self.http_method, path=self.secure_endpoint, data=self.data)

    def test_secure(self):
        meta = _get_span_meta(request=self.secure_request)
        iast_json = meta.get("_dd.iast.json")
        assert iast_json is None, f"Unexpected vulnerabilities reported: {iast_json}"

    def setup_telemetry_metric_instrumented_sink(self):
        self.setup_insecure()

    def test_telemetry_metric_instrumented_sink(self):

        _check_telemetry_response_from_agent()

        expected_namespace = "iast"
        expected_metric = "instrumented.sink"
        series = interfaces.library.get_telemetry_metric_series(expected_namespace, expected_metric)
        assert series, f"Got no series for metric {expected_metric}"
        logging.debug("Series: %s", series)

        # lower the vulnerability_type, as all assertion will be case-insensitive
        expected_tag = f"vulnerability_type:{self.vulnerability_type}".lower()

        # Filter by taking only series where expected tag is in the list serie.tags (case insentive check)
        series = [serie for serie in series if expected_tag in map(str.lower, serie["tags"])]

        assert len(series) != 0, f"Got no series for metric {expected_metric} with tag {expected_tag}"

        for s in series:
            assert s["_computed_namespace"] == expected_namespace
            assert s["metric"] == expected_metric
            assert s["common"] is True
            assert s["type"] == "count"
            assert len(s["points"]) == 1
            p = s["points"][0]
            assert p[1] >= 1

    def setup_telemetry_metric_executed_sink(self):
        self.setup_insecure()

    def test_telemetry_metric_executed_sink(self):

        _check_telemetry_response_from_agent()

        expected_namespace = "iast"
        expected_metric = "executed.sink"
        series = interfaces.library.get_telemetry_metric_series(expected_namespace, expected_metric)
        assert series, f"Got no series for metric {expected_metric}"
        logging.debug("Series: %s", series)

        # lower the vulnerability_type, as all assertion will be case-insensitive
        expected_tag = f"vulnerability_type:{self.vulnerability_type}".lower()

        # Filter by taking only series where expected tag is in the list serie.tags (case insentive check)
        series = [serie for serie in series if expected_tag in map(str.lower, serie["tags"])]

        assert len(series) != 0, f"Got no series for metric {expected_metric} with tag {expected_tag}"

        for s in series:
            assert s["_computed_namespace"] == expected_namespace
            assert s["metric"] == expected_metric
            assert s["common"] is True
            assert s["type"] == "count"
            assert len(s["points"]) == 1
            p = s["points"][0]
            assert p[1] >= 1


class BaseSourceTest:
    endpoint = None
    requests_kwargs = None
    source_type = None
    source_name = None
    source_value = None
    requests: dict = None

    def setup_source_reported(self):
        assert isinstance(self.requests_kwargs, list), f"{self.__class__}.requests_kwargs must be a list of dicts"

        # optimize by attaching requests to the class object, to avoid calling it several times. We can't attach them
        # to self, and we need to attach the request on class object, as there are one class instance by test case

        if self.__class__.requests is None:
            self.__class__.requests = {}
            for kwargs in self.requests_kwargs:
                method = kwargs["method"]
                # store them as method:request to allow later custom test by method
                self.__class__.requests[method] = weblog.request(path=self.endpoint, **kwargs)

        self.requests = self.__class__.requests

    def test_source_reported(self):
        for request in self.requests.values():
            self.validate_request_reported(request)

    def validate_request_reported(self, request, source_type=None):
        if source_type is None:  # allow to overwrite source_type for parameter value node's use case
            source_type = self.source_type

        iast = get_iast_event(request=request)
        sources = iast["sources"]
        assert sources, "No source reported"
        if source_type:
            assert source_type in {s.get("origin") for s in sources}
            sources = [s for s in sources if s["origin"] == source_type]
        if self.source_name:
            assert self.source_name in {s.get("name") for s in sources}
            sources = [s for s in sources if s["name"] == self.source_name]
        if self.source_value:
            assert self.source_value in {s.get("value") for s in sources}
            sources = [s for s in sources if s["value"] == self.source_value]
        assert sources, f"No source found with origin={source_type}, name={self.source_name}, value={self.source_value}"
        assert len(sources) == 1, "Expected a single source with the matching criteria"

    setup_telemetry_metric_instrumented_source = setup_source_reported

    def test_telemetry_metric_instrumented_source(self):

        _check_telemetry_response_from_agent()

        expected_namespace = "iast"
        expected_metric = "instrumented.source"
        series = interfaces.library.get_telemetry_metric_series(expected_namespace, expected_metric)
        assert series, f"Got no series for metric {expected_metric}"
        logging.debug(f"Series: {json.dumps(series, indent=2)}")

        # lower the source_type, as all assertion will be case-insensitive
        expected_tag = f"source_type:{self.source_type}".lower()

        # Filter by taking only series where expected tag is in the list serie.tags (case insentive check)
        series = [serie for serie in series if expected_tag in map(str.lower, serie["tags"])]

        assert len(series) != 0, f"Got no series for metric {expected_metric} with tag {expected_tag}"

        for s in series:
            assert s["_computed_namespace"] == expected_namespace
            assert s["metric"] == expected_metric
            assert s["common"] is True
            assert s["type"] == "count"
            assert len(s["points"]) == 1
            p = s["points"][0]
            assert p[1] >= 1

    setup_telemetry_metric_executed_source = setup_source_reported

    def test_telemetry_metric_executed_source(self):

        _check_telemetry_response_from_agent()

        expected_namespace = "iast"
        expected_metric = "executed.source"
        series = interfaces.library.get_telemetry_metric_series(expected_namespace, expected_metric)
        assert series, f"Got no series for metric {expected_metric}"

        # lower the source_type, as all assertion will be case-insensitive
        expected_tag = f"source_type:{self.source_type}".lower()

        # Filter by taking only series where expected tag is in the list serie.tags (case insentive check)
        series = [serie for serie in series if expected_tag in map(str.lower, serie["tags"])]

        assert len(series) != 0, f"Got no series for metric {expected_metric} with tag {expected_tag}"

        logging.debug(f"Series:\n{json.dumps(series, indent=2)}")

        for s in series:
            assert s["_computed_namespace"] == expected_namespace
            assert s["metric"] == expected_metric
            assert s["common"] is True
            assert s["type"] == "count"
            assert len(s["points"]) == 1
            p = s["points"][0]
            assert p[1] >= 1
