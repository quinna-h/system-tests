# Unless explicitly stated otherwise all files in this repository are licensed under the the Apache License Version 2.0.
# This product includes software developed at Datadog (https://www.datadoghq.com/).
# Copyright 2021 Datadog, Inc.

from utils import BaseTestCase, interfaces, context, missing_feature, coverage
from utils.interfaces._library.appsec_iast import VulnerabilityAsserts


# Weblog are ok for nodejs/express4 and java/spring-boot
@missing_feature(reason="Need to be implement in iast library")
@coverage.not_implemented  # TODO : the test logic must be written once we hve the RFC
class Test_Iast(BaseTestCase):
    """Verify the IAST features"""

    def test_insecure_hashing_all(self):
        """Test insecure hashing all algorithms"""
        r = self.weblog_get("/iast/insecure_hashing")
        interfaces.library.assert_trace_exists(r)

        interfaces.library.add_appsec_iast_validation(
            r,
            VulnerabilityAsserts()
            .filter_by_type("WEAK_HASH")
            .filter_by_location("com.datadoghq.system_tests.springboot.iast.utils.CryptoExamples", 33)
            .expect_exact_count(4)
            .expect_only_these_vulnerabilities()
            .validate,
        )

    def test_secure_hashing_sha256(self):
        """Test secure hashing sha256 algorithm (no vulnerability has to been reported)"""
        r = self.weblog_get("/iast/insecure_hashing?algorithmName=sha256")
        interfaces.library.assert_trace_exists(r)

        interfaces.library.add_appsec_iast_validation(
            r,
            VulnerabilityAsserts().expect_exact_count(0).expect_only_these_vulnerabilities().validate,
        )

    def test_insecure_hashing_sha1(self):
        """Test insecure hashing sha1 algorithm"""
        r = self.weblog_get("/iast/insecure_hashing?algorithmName=sha1")
        interfaces.library.assert_trace_exists(r)

        interfaces.library.add_appsec_iast_validation(
            r,
            VulnerabilityAsserts()
            .filter_by_type("WEAK_HASH")
            .filter_by_location("com.datadoghq.system_tests.springboot.iast.utils.CryptoExamples", 33)
            .filter_by_evidence("SHA-1")
            .expect_exact_count(1)
            .expect_only_these_vulnerabilities()
            .validate,
        )

    def test_insecure_hashing_md5(self):
        """Test insecure hashing md5 algorithm"""
        r = self.weblog_get("/iast/insecure_hashing?algorithmName=md5")
        interfaces.library.assert_trace_exists(r)

        interfaces.library.add_appsec_iast_validation(
            r,
            VulnerabilityAsserts()
            .filter_by_type("WEAK_HASH")
            .filter_by_evidence("MD5")
            .expect_exact_count(1)
            .expect_only_these_vulnerabilities()
            .validate,
        )

    def test_insecure_hashing_md4(self):
        """Test insecure hashing md4 algorithm"""
        r = self.weblog_get("/iast/insecure_hashing?algorithmName=md4")
        interfaces.library.assert_trace_exists(r)

        interfaces.library.add_appsec_iast_validation(
            r,
            VulnerabilityAsserts()
            .filter_by_type("WEAK_HASH")
            .filter_by_evidence("MD4")
            .expect_exact_count(1)
            .expect_only_these_vulnerabilities()
            .validate,
        )

    def test_insecure_hashing_md2(self):
        """Test insecure hashing md2 algorithm"""
        r = self.weblog_get("/iast/insecure_hashing?algorithmName=md2")
        interfaces.library.assert_trace_exists(r)

        interfaces.library.add_appsec_iast_validation(
            r,
            VulnerabilityAsserts()
            .filter_by_type("WEAK_HASH")
            .filter_by_evidence("MD2")
            .expect_exact_count(1)
            .expect_only_these_vulnerabilities()
            .validate,
        )
