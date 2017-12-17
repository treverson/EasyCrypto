from unittest import TestCase, mock
from comm_control import CommControl

class TestCommControl(TestCase):

    def setUp(self):

        self.macro_control = CommControl()

    def test_use_command(self):

        command = {
            "name": "test",
            "protocol": "WAMP",
            "address": "test.com",
            "action": "test_action",
            "parameters": {"a": 1}
        }

        self.assertRaises(AttributeError, self.macro_control.use_command, command)


        command = {
            "name": "Bittrex",
            "protocol": "REST",
            "address": "https://bittrex.com/api/v1.1/",
            "action": "public/getcurrencies",
            "parameters": {}
        }

        self.macro_control.use_command(command)
