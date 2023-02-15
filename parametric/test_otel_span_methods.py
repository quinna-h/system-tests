import time
import pytest

from parametric.spec.trace import find_trace_by_root
from parametric.spec.trace import find_span_in_traces
from parametric.spec.trace import find_span
from parametric.spec.otel_trace import OtelSpan
from parametric.spec.otel_trace import OTEL_UNSET_CODE, OTEL_ERROR_CODE, OTEL_OK_CODE
from parametric.spec.otel_trace import SK_PRODUCER

# todo: add prefix_library to run otel_*


@pytest.mark.skip_library("dotnet", "Not implemented")
@pytest.mark.skip_library("nodejs", "Not implemented")
@pytest.mark.skip_library("python", "Not implemented")
@pytest.mark.skip_library("java", "Not implemented")
def test_otel_start_span(test_agent, test_library):
    """
        - Start/end a span with start and end options
        - Start a tracer with options
    """
    test_library.otel_env = "otel_env"
    test_library.otel_service = "otel_serv"

    # entering test_otel_library starts the tracer with the above options
    with test_library:
        duration_s = int(2 * 1000000)
        start_time = int(time.time())
        starting_attributes = {"start_attr_key": "start_attr_val"}
        with test_library.start_otel_span(
            "operation", span_kind=SK_PRODUCER, timestamp=start_time, new_root=True, attributes=starting_attributes,
        ) as parent:
            parent.finish(timestamp=start_time + duration_s)
    duration_ns = duration_s / (1e-9)

    traces = test_agent.wait_for_num_traces(1)
    trace = find_trace_by_root(traces, OtelSpan(name="operation"))
    assert len(trace) == 1

    root_span = find_span(trace, OtelSpan(name="operation"))
    assert root_span["meta"]["env"] == "otel_env"
    assert root_span["service"] == "otel_serv"
    assert root_span["name"] == "operation"
    assert root_span["resource"] == "operation"
    assert root_span["meta"]["start_attr_key"] == "start_attr_val"
    assert root_span["duration"] == duration_ns


@pytest.mark.skip_library("dotnet", "Not implemented")
@pytest.mark.skip_library("nodejs", "Not implemented")
@pytest.mark.skip_library("python", "Not implemented")
@pytest.mark.skip_library("java", "Not implemented")
def test_otel_set_attributes(test_agent, test_library):
    """
        - Set attributes of multiple types for an otel span
    """
    parent_start_time = int(time.time())
    with test_library:
        with test_library.start_otel_span(
            "operation", span_kind=SK_PRODUCER, timestamp=parent_start_time, new_root=True,
        ) as parent:
            parent.set_attributes({"key": ["val1", "val2"]})
            parent.set_attributes({"key2": [1]})
            parent.set_attributes({"pi": 3.14, "hi": "bye"})

    traces = test_agent.wait_for_num_traces(1)
    trace = find_trace_by_root(traces, OtelSpan(name="operation"))
    assert len(trace) == 1

    root_span = find_span(trace, OtelSpan(name="operation"))

    assert root_span["name"] == "operation"
    assert root_span["resource"] == "operation"
    assert "val2" in root_span["meta"]["key"]
    assert "val1" in root_span["meta"]["key"]
    assert root_span["metrics"]["key2"] == 1
    assert root_span["metrics"]["pi"] == 3.14
    assert root_span["meta"]["hi"] == "bye"


@pytest.mark.skip_library("dotnet", "Not implemented")
@pytest.mark.skip_library("nodejs", "Not implemented")
@pytest.mark.skip_library("python", "Not implemented")
@pytest.mark.skip_library("java", "Not implemented")
def test_otel_span_end(test_agent, test_library):
    """
    Test functionality of ending a span. After ending:
        - operations on that span become noop
        - span.is_recording() is false
        - child spans are still running and can be ended later
        - still possible to start child spans from parent context
    """
    with test_library:
        # start parent
        with test_library.start_otel_span(name="parent") as parent:
            pid = parent.span_id
            # start first child
            with test_library.start_otel_span(name="child1", parent_id=pid) as child_1:
                parent.finish()
                parent.set_name("grandparent")  # should have no affect

                # start second child after parent has been ended
                with test_library.start_otel_span(name="child2", parent_id=pid) as child_2:
                    child_1.set_attributes({"key": "value"})
                    child_2.set_attributes({"k2": "v2"})

                    assert child_1.is_recording()
                    assert child_2.is_recording()
                    assert not parent.is_recording()

                    child_1.finish()
                    child_2.finish()

    traces = test_agent.wait_for_num_traces(1)
    trace = find_trace_by_root(traces, OtelSpan(name="parent"))
    assert len(trace) == 3

    root_span = find_span(trace, OtelSpan(name="parent"))
    assert root_span["name"] == "parent"

    c1 = find_span(trace, OtelSpan(name="child1"))
    c2 = find_span(trace, OtelSpan(name="child2"))
    assert "value" in c1["meta"]["key"]
    assert "v2" in c2["meta"]["k2"]


@pytest.mark.skip_library("dotnet", "Not implemented")
@pytest.mark.skip_library("nodejs", "Not implemented")
@pytest.mark.skip_library("python", "Not implemented")
@pytest.mark.skip_library("java", "Not implemented")
def test_otel_set_span_status(test_agent, test_library):
    """
        This test verifies that setting the status of a span
        behaves accordingly to the Otel API spec
        (https://opentelemetry.io/docs/reference/specification/trace/api/#set-status)
        By checking the following:
        1. attempts to set the value of `Unset` are ignored
        2. description must only be used with `Error` value
        3. setting the status to `Ok` is final and will override any
            any prior or future status values
    """
    with test_library:
        with test_library.start_otel_span(name="error_span") as span:
            span.set_status(OTEL_ERROR_CODE, "error_desc")
            span.set_status(OTEL_UNSET_CODE, "unset_desc")
        with test_library.start_otel_span(name="ok_span") as span:
            span.set_status(OTEL_OK_CODE, "ok_desc")
            span.set_status(OTEL_ERROR_CODE, "error_desc")

    err_spn = OtelSpan(name="error_span")
    ok_spn = OtelSpan(name="ok_span")

    traces = test_agent.wait_for_num_traces(2)

    span = find_span(find_trace_by_root(traces, err_spn), err_spn)
    tags = span.get("meta")
    assert tags is not None
    assert tags.get("error.message") == "error_desc"

    span = find_span(find_trace_by_root(traces, ok_spn), ok_spn)
    tags = span.get("meta")
    assert tags is not None
    assert "error.message" not in tags
