# Unless explicitly stated otherwise all files in this repository are licensed under the the Apache License Version 2.0.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2022 Datadog, Inc.

from utils import BaseTestCase, interfaces, missing_feature


@missing_feature(library="cpp")
@missing_feature(library="golang")
@missing_feature(library="nodejs")
@missing_feature(library="java")
@missing_feature(library="php")
@missing_feature(library="python")
@missing_feature(library="ruby")
class Test_Basic(BaseTestCase):
    """ Make sure the spans endpoint is successful """

    def test_spans_generation(self):
        r = self.weblog_get("/spans")
        interfaces.library.assert_trace_exists(r)
