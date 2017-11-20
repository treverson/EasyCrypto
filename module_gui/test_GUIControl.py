from unittest import TestCase

from GUIcontrol import GUIControl


class TestGUIControl(TestCase):

    def test_show(self):

        with self.assertRaises(SystemExit) as cm:
            self.guiControl = GUIControl()

        self.assertEqual(cm.exception.code, 0)