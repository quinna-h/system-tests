# Unless explicitly stated otherwise all files in this repository are licensed under the the Apache License Version 2.0.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2022 Datadog, Inc.

from utils import weblog, interfaces, context, missing_feature, released, scenario


@released(cpp="?", golang="?", java="?", dotnet="?", nodejs="?", php="?", ruby="?")
@missing_feature(context.library == "python" and context.weblog_variant != "flask-poc", reason="Missing on weblog")
@scenario("INTEGRATIONS")
class Test_Dbm:
    """Verify behavior of DBM propagation"""

    def setup_trace_payload(self):
        self.r_execute = weblog.get("/dbm", params={"integration": "psycopg", "cursor_method": "execute"})
        self.r_many = weblog.get("/dbm", params={"integration": "psycopg", "cursor_method": "executemany"})

    def test_trace_payload(self):
        def validator(span):
            if span.get("span_type") != "sql":
                return

            meta = span.get("meta", {})
            assert "_dd.dbm_trace_injected" in meta

            return True

        # test psycopg execute()
        interfaces.library.add_assertion(self.r_execute.status_code == 200)
        interfaces.library.add_span_validation(self.r_execute, validator=validator, is_success_on_expiry=True)

        # test psycopg executemany()
        interfaces.library.add_assertion(self.r_many.status_code == 200)
        interfaces.library.add_span_validation(self.r_many, validator=validator, is_success_on_expiry=True)

    def test_dbm_payload(self):
        # TODO: Add schema for validation of dbm payload agent/backend
        # TODO: Add check for dbm payload agent/backend ensure that the expected trace data
        pass
