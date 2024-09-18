from utils import context, interfaces, scenarios, weblog, bug, features


@scenarios.appsec_custom_rules
@features.waf_features
class Test_Exclusions:
    """Includes a version of the WAF supporting rule exclusion"""

    def setup_input_exclusion_negative_test(self):
        self.r_iexnt1 = weblog.get("/waf/", params={"excluded_key": "true"})
        self.r_iexnt2 = weblog.get("/waf/", params={"excluded_key": "true", "activate_exclusion": "false"})

    @bug(context.library <= "ruby@1.12.1", reason="APMRP-360")
    def test_input_exclusion_negative_test(self):
        interfaces.library.assert_waf_attack(self.r_iexnt1, pattern="true", address="server.request.query")
        interfaces.library.assert_waf_attack(self.r_iexnt2, pattern="true", address="server.request.query")

    def setup_input_exclusion_positive_test(self):
        self.r_iexpt = weblog.get("/waf/", params={"excluded_key": "true", "activate_exclusion": "true"})

    def test_input_exclusion_positive_test(self):
        interfaces.library.assert_no_appsec_event(self.r_iexpt)

    def setup_rule_exclusion_negative_test(self):
        self.r_rent1 = weblog.get("/waf/", params={"foo": "bbbb"})
        self.r_rent2 = weblog.get("/waf/", params={"foo": "bbbb", "activate_exclusion": "false"})

    def test_rule_exclusion_negative_test(self):
        interfaces.library.assert_waf_attack(self.r_rent1, pattern="bbbb", address="server.request.query")
        interfaces.library.assert_waf_attack(self.r_rent2, pattern="bbbb", address="server.request.query")

    def setup_rule_exclusion_positive_test(self):
        self.r_rept = weblog.get("/waf/", params={"foo": "bbbb", "activate_exclusion": "true"})

    @bug(context.library <= "ruby@1.12.1", reason="APMRP-360")
    def test_rule_exclusion_positive_test(self):
        interfaces.library.assert_no_appsec_event(self.r_rept)
