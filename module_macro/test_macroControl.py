from unittest import TestCase, mock
from macro_control import MacroControl

class TestMacroControl(TestCase):

    def setUp(self):

        self.macro_control = MacroControl()

    def test_use_command(self):

        command = {
            "name": "test",
            "protocol": "WAMP",
            "address": "test.com",
            "action": "test_action",
            "parameters": {"a": 1}
        }

        self.assertRaises(AttributeError, self.macro_control.use_command, command)
