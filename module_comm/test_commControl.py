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
            "name": "Poloniex",
            "protocol": "WAMP",
            "address": "wss://api.poloniex.com",
            "action": "ticker",
            "parameters": {"currency_pair": "USDT_BTC"}
        }

        self.macro_control.use_command(command)
