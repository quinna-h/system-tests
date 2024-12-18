import json
import yaml
import argparse


from docker_ssi_definitions import ALL_WEBLOGS


def generate_gitlab_pipeline(languages):
    pipeline = {
        "stages": ["dummy"],
        # A dummy job is necessary for cases where all of the test jobs are manual
        # The child pipeline shows as failed until at least 1 job is run
        "dummy": {
            "image": "registry.ddbuild.io/docker:20.10.13-gbi-focal",
            "tags": ["arch:amd64"],
            "stage": "dummy",
            "dependencies": [],
            "script": ["echo 'DONE'"],
        },
        "docker_ssi_fpd": {
            "image": "486234852809.dkr.ecr.us-east-1.amazonaws.com/ci/test-infra-definitions/runner:a58cc31c",
            "tags": ["arch:amd64"],
            "stage": "parse_docker_ssi_results",
            "allow_failure": True,
            "rules": [
                {"if": '$PARENT_PIPELINE_SOURCE == "schedule" && $CI_COMMIT_BRANCH == "main"', "when": "always"},
                {"when": "manual", "allow_failure": True},
            ],
            "before_script": [
                'export FP_IMPORT_URL=$(aws ssm get-parameter --region us-east-1 --name ci.system-tests.fp-import-url --with-decryption --query "Parameter.Value" --out text)',
                'export FP_API_KEY=$(aws ssm get-parameter --region us-east-1 --name ci.system-tests.fp-api-key --with-decryption --query "Parameter.Value" --out text)',
            ],
            "script": [
                "for folder in reports/logs*/ ; do",
                'echo "Checking folder: ${folder}"',
                "for filename in ./${folder}feature_parity.json; do",
                "if [ -e ${filename} ]",
                "then",
                'echo "Processing report: ${filename}"',
                'curl -X POST ${FP_IMPORT_URL} --fail --header "Content-Type: application/json"  --header "FP_API_KEY: ${FP_API_KEY}" --data "@${filename}" --include || true',
                "fi",
                "done",
                "done",
            ],
        },
        ".base_ssi_job": {
            "image": "registry.ddbuild.io/ci/libdatadog-build/system-tests:48436362",
            "script": [
                "./build.sh -i runner",
                "source venv/bin/activate",
                'timeout 2700s ./run.sh DOCKER_SSI --ssi-weblog "$weblog" --ssi-library "$TEST_LIBRARY" --ssi-base-image "$base_image" --ssi-arch "$arch" --ssi-installable-runtime "$installable_runtime" --report-run-url ${CI_PIPELINE_URL} --report-environment prod',
            ],
            "rules": [
                {"if": '$PARENT_PIPELINE_SOURCE == "schedule"', "when": "always"},
                {"when": "manual", "allow_failure": True},
            ],
            "after_script": [
                'SCENARIO_SUFIX=$(echo "DOCKER_SSI" | tr "[:upper:]" "[:lower:]")',
                'REPORTS_PATH="reports/"',
                'mkdir -p "$REPORTS_PATH"',
                'cp -R logs_"${SCENARIO_SUFIX}" $REPORTS_PATH/',
                'cleaned_base_image=$(echo "$base_image" | tr -cd "[:alnum:]_")',
                'cleaned_arch=$(echo "$arch" | tr -cd "[:alnum:]_")',
                'cleaned_runtime=$(echo "$installable_runtime" | tr -cd "[:alnum:]_")',
                'mv "$REPORTS_PATH"/logs_"${SCENARIO_SUFIX}" "$REPORTS_PATH"/logs_"${TEST_LIBRARY}"_"${weblog}"_"${SCENARIO_SUFIX}_${cleaned_base_image}_${cleaned_arch}_${cleaned_runtime}"',
            ],
            "artifacts": {"when": "always", "paths": ["reports/"]},
        },
    }

    for language in languages:
        pipeline["stages"].append(language)
        matrix = []

        filtered = [weblog for weblog in ALL_WEBLOGS if weblog.library == language]
        for weblog in filtered:
            weblog_matrix = weblog.get_matrix()
            if not weblog_matrix:
                continue
            for test in weblog_matrix:
                if test["arch"] == "linux/amd64":
                    test["runner"] = "docker"
                else:
                    test["runner"] = "docker-arm"
                test.pop("unique_name", None)
                matrix.append(test)
        if matrix:
            pipeline[language] = {
                "extends": ".base_ssi_job",
                "tags": ["runner:$runner"],
                "stage": language,
                "allow_failure": True,
                "dependencies": [],
                "variables": {"TEST_LIBRARY": language,},
                "parallel": {"matrix": matrix},
            }
    pipeline["stages"].append("parse_docker_ssi_results")
    return pipeline


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", required=True, type=str, choices=["json", "yaml"], help="json or yaml")
    parser.add_argument("--output-file", required=False, type=str)
    parser.add_argument("--language", required=False, type=str, help="Only generate config for single language")

    args = parser.parse_args()
    if args.language:
        languages = [args.language]
    else:
        languages = ["java", "python", "nodejs", "dotnet", "ruby", "php"]

    pipeline = generate_gitlab_pipeline(languages)

    output = (
        json.dumps(pipeline, sort_keys=False)
        if args.format == "json"
        else yaml.dump(pipeline, sort_keys=False, default_flow_style=False)
    )
    print(output)
    if args.output_file is not None:
        with open(args.output_file, "w") as f:
            f.write(output)


if __name__ == "__main__":
    main()
