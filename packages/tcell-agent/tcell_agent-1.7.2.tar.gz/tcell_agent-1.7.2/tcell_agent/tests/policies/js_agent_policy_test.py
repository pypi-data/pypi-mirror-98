import unittest

from tcell_agent.policies.js_agent_policy import JsAgentPolicy
from tcell_agent.tests.support.builders import ConfigurationBuilder, ContextBuilder, NativeAgentBuilder
from tcell_agent.tests.support.free_native_agent import free_native_agent


class JsAgentPolicyTest(unittest.TestCase):
    def setUp(self):
        self.configuration = ConfigurationBuilder().build()
        self.native_agent = NativeAgentBuilder()
        self.tcell_context = ContextBuilder().build()

    def tearDown(self):
        free_native_agent(self.native_agent.agent_ptr)

    def test_classname(self):
        self.assertEqual(JsAgentPolicy.api_identifier, "jsagentinjection")

    def test_disabled_js_agent_policy(self):
        policies_rsp = self.native_agent.update_policies({
            "jsagentinjection": {
                "enabled": False,
                "api_key": "AQABBA",
                "excludes": [],
                "policy_id": "jsagentinjection-v1-1",
                "version": 1}})

        policy = JsAgentPolicy(self.native_agent, policies_rsp["enablements"], None)
        self.assertFalse(policy.jsagent_enabled)
        self.assertEqual(
            policy.get_js_agent_script_tag(self.tcell_context),
            None,
        )

    def test_enabled_js_agent_policy(self):
        policies_rsp = self.native_agent.update_policies({
            "jsagentinjection": {
                "enabled": True,
                "api_key": "AQABBA",
                "excludes": [],
                "policy_id": "jsagentinjection-v1-1",
                "version": 1}})

        policy = JsAgentPolicy(self.native_agent, policies_rsp["enablements"], None)
        self.assertTrue(policy.jsagent_enabled)
        self.assertEqual(
            policy.get_js_agent_script_tag(self.tcell_context),
            "<script src=\"{}\" tcellappid=\"{}\" tcellapikey=\"{}\" tcellbaseurl=\"{}\"></script>".format(
                self.configuration.js_agent_url,
                self.configuration.app_id,
                "AQABBA",
                self.configuration.tcell_api_url
            )
        )
