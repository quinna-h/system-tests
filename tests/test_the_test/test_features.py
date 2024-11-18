from utils import scenarios, features
from utils.tools import logger

from .utils import run_system_tests


FILENAME = "tests/test_the_test/test_features.py"


def execute_process(forced_test):
    return run_system_tests(test_path=FILENAME, forced_test=forced_test)


@scenarios.mock_the_test
@features.not_reported
def test_schemas():
    pass


@scenarios.test_the_test
def test_not_reported():
    result = run_system_tests(test_path=FILENAME)

    assert len(result) == 0


@scenarios.test_the_test
def test_all_class_has_feature_decorator(session, deselected_items):

    allow_no_feature_nodes = session.config.inicfg["allow_no_feature_nodes"]
    processed_nodes = set()
    shouldfail = False

    for item in session.items + deselected_items:
        reported_node_id = "::".join(item.nodeid.split("::", 2)[0:2])

        if reported_node_id in processed_nodes:
            continue

        processed_nodes.add(reported_node_id)

        allow_missing_declaration = False

        for node in allow_no_feature_nodes:
            if item.nodeid.startswith(node):
                allow_missing_declaration = True
                break

        if allow_missing_declaration:
            continue

        declared_features = [marker.kwargs["feature_id"] for marker in item.iter_markers("features")]

        if len(declared_features) == 0:
            logger.error(f"Missing feature declaration for {reported_node_id}")
            shouldfail = True

    DOC_URL = "https://github.com/DataDog/system-tests/blob/main/docs/edit/add-new-test.md"
    if shouldfail:
        raise ValueError(f"Some test classes misses @features decorator. More info on {DOC_URL}")
