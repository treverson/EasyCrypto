from unittest import TestCase
from unittest.mock import Mock

from PyQt5.QtGui import QGuiApplication

from module_db import db_control
from gui_control import GUIControl


class TestGUIControl(TestCase):

    def setUp(self):

        self.control = GUIControl()

    def test_notify_website_clicked(self):

        self.control.__refresh_event_action = Mock()
        self.control.notify_website_clicked()
        self.assertTrue(self.control.__refresh_event_action.is_called())

    def test_notify_action_clicked(self):

        self.control.__refresh_event_parameter = Mock()
        self.control.notify_action_clicked()
        self.assertTrue(self.control.__refresh_event_parameter.is_called())

    """ the two tests below are used interchangeably,
    test_setup_default: test without launching window
    test_show: test with window
    
    to be removed after discovery of method for testing QML
    """
    def test_setup_default(self):

        pass
        #self.control.setup()

    def test_show(self):

        self.control.setup()

        with self.assertRaises(SystemExit) as cm:
            self.control.show()

        self.assertEqual(cm.exception.code, 0)