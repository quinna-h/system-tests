from collections import defaultdict
import json
import os
from manifests.parser.core import load as load_manifests
from utils._context._scenarios import ScenarioGroup


def handle_labels(labels: list[str], scenarios_groups: set[str]):

    if "run-all-scenarios" in labels:
        scenarios_groups.add(ScenarioGroup.ALL.value)
    else:
        if "run-integration-scenarios" in labels:
            scenarios_groups.add(ScenarioGroup.INTEGRATIONS.value)
        if "run-sampling-scenario" in labels:
            scenarios_groups.add(ScenarioGroup.SAMPLING.value)
        if "run-profiling-scenario" in labels:
            scenarios_groups.add(ScenarioGroup.PROFILING.value)
        if "run-debugger-scenarios" in labels:
            scenarios_groups.add(ScenarioGroup.DEBUGGER.value)
        if "run-appsec-scenarios" in labels:
            scenarios_groups.add(ScenarioGroup.APPSEC.value)
        if "run-open-telemetry-scenarios" in labels:
            scenarios_groups.add(ScenarioGroup.OPEN_TELEMETRY.value)
        if "run-parametric-scenario" in labels:
            scenarios_groups.add(ScenarioGroup.PARAMETRIC.value)
        if "run-graphql-scenarios" in labels:
            scenarios_groups.add(ScenarioGroup.GRAPHQL.value)
        if "run-libinjection-scenarios" in labels:
            scenarios_groups.add(ScenarioGroup.LIB_INJECTION.value)


def main():
    scenarios = set()
    scenarios_groups = set()

    event_name = os.environ["GITHUB_EVENT_NAME"]
    ref = os.environ["GITHUB_REF"]

    if event_name == "schedule" or ref == "refs/heads/main":
        scenarios_groups.add(ScenarioGroup.ALL.value)

    elif event_name == "pull_request":
        labels = json.loads(os.environ["GITHUB_PULL_REQUEST_LABELS"])
        label_names = [label["name"] for label in labels]
        handle_labels(label_names, scenarios_groups)

        # this file is generated with
        # ./run.sh MOCK_THE_TEST --collect-only --scenario-report
        with open("logs_mock_the_test/scenarios.json", "r", encoding="utf-8") as f:
            scenario_map = json.load(f)

        modified_nodeids = set()

        new_manifests = load_manifests("manifests/")
        old_manifests = load_manifests("original/manifests/")

        for nodeid in set(list(new_manifests.keys()) + list(old_manifests.keys())):
            if (
                nodeid not in old_manifests
                or nodeid not in new_manifests
                or new_manifests[nodeid] != old_manifests[nodeid]
            ):
                modified_nodeids.add(nodeid)

        scenarios_by_files = defaultdict(set)
        for nodeid in scenario_map:
            file = nodeid.split(":", 1)[0]
            scenarios_by_files[file].add(scenario_map[nodeid])

            for modified_nodeid in modified_nodeids:
                if nodeid.startswith(modified_nodeid):
                    scenarios.add(scenario_map[nodeid])
                    break

        # this file is generated with
        #   git fetch origin ${{ github.event.pull_request.base.sha || github.sha }}
        #   git diff --name-only HEAD ${{ github.event.pull_request.base.sha || github.sha }} >> modified_files.txt

        with open("modified_files.txt", "r", encoding="utf-8") as f:
            modified_files = [line.strip() for line in f.readlines()]

        for file in modified_files:
            if file.startswith("utils/interfaces/schemas") or file == "tests/test_schemas.py":
                scenarios_groups.add(ScenarioGroup.END_TO_END.value)

            if file in scenarios_by_files:
                scenarios.update(scenarios_by_files[file])

    print("scenarios=" + ",".join(scenarios))
    print("scenarios_groups=" + ",".join(scenarios_groups))


if __name__ == "__main__":
    main()