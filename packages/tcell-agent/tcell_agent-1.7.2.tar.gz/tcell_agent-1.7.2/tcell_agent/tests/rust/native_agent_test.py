import unittest

from mock import patch

from tcell_agent.config.configuration import set_config
from tcell_agent.loggers.python_logger import PythonLogger
from tcell_agent.rust.native_agent import NativeAgent, \
     PlaceholderNativeAgent, create_native_agent
from tcell_agent.tests.support.builders import ConfigurationBuilder, NativeAgentBuilder
from tcell_agent.tests.support.free_native_agent import free_native_agent


class CreateNativeAgentTest(unittest.TestCase):
    def setUp(self):
        ConfigurationBuilder().set_config()

    def tearDown(self):
        set_config(None)

    def test_missing_native_lib_create_native_agent(self):
        with patch("tcell_agent.rust.native_agent.get_native_lib",
                   return_value=None) as patched_get_native_lib:
            with patch.object(PythonLogger,
                              "log_message",
                              return_value=None) as patched_log_message:
                native_agent = NativeAgentBuilder()
                self.assertFalse(patched_log_message.called)
                self.assertTrue(patched_get_native_lib.called)
                self.assertEqual(type(native_agent), PlaceholderNativeAgent)

    def missing_configuration_file_create_native_agent(self):
        with patch.object(PythonLogger,
                          "log_message",
                          return_value=None) as patched_log_message:
            with patch.dict('os.environ', {'TCELL_AGENT_CONFIG': '/tmp/non-existent-file',
                                           'TCELL_AGENT_LOG_ENABLED': 'false'}):
                native_agent = create_native_agent()
                self.assertTrue(patched_log_message.called)
                args, kwargs = patched_log_message.call_args
                self.assertEqual(kwargs, {})
                self.assertEqual(args[0], "error")
                self.assertTrue(
                    "create_agent returned an error: Failed to build a valid agent configuration" in args[1]
                )
                self.assertEqual(args[2], "tcell_agent.rust.native_agent")
                self.assertEqual(type(native_agent), PlaceholderNativeAgent)

    def test_create_native_agent(self):

        with patch.object(PythonLogger,
                          "log_message",
                          return_value=None) as patched_log_message:
            native_agent = NativeAgentBuilder()
            self.assertFalse(patched_log_message.called)
            self.assertEqual(type(native_agent), NativeAgent)
            free_native_agent(native_agent.agent_ptr)
