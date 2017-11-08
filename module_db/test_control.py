from unittest import TestCase
from control import Control, Base

from models import Website, load_args

import sqlalchemy
import json

class TestControl(TestCase):

    control = None

    def setUp(self):

        self.control = Control()

    def test_constructor(self):

        assert self.control is not None
        assert self.control.is_connected() is True

    def test_is_correct_class(self):

        o = Website(name="Example")
        assert self.control.is_correct_class(o) is True

        class Foo:
            pass
        o = Foo()
        assert self.control.is_correct_class(o) is False

    def test_db_operations(self):

        o = Website(name="Example")
        self.assertRaises(sqlalchemy.exc.IntegrityError, self.control.map_object, o)

        o = Website(name="Test", address="Test", protocol="Test")
        self.control.map_object(o)
        result = self.control.get_objects_of_class(Website, attribs={"name": "Test"})
        assert len(result) >= 1
        test_len = len(result)

        self.control.remove_object(o.__class__, {"name": o.name})
        result = self.control.get_objects_of_class(Website, attribs={"name": o.name})
        assert len(result) == test_len - 1



    def test_load_basic_db_structure(self):

        self.control.load_basic_db_structure(clean=True)


