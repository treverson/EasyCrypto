from unittest import TestCase
from DBcontrol import DBControl


from module_db import DBmodels
from module_db.DBmodels import Base, load_args
from DBmodels import Website

import sqlalchemy
import json


class TestControl(TestCase):

    def setUp(self):

        self.dbControl = DBControl()

    def test_constructor(self):

        assert self.dbControl is not None
        assert self.dbControl.is_connected() is True

    def test_is_correct_class(self):

        o = DBmodels.Website(name="Example")
        assert self.dbControl.is_correct_class(o) is True

        class Foo:
            pass
        o = Foo()
        assert self.dbControl.is_correct_class(o) is False

    def test_db_operations(self):

        o = DBmodels.Website(name="Example")
        self.assertRaises(sqlalchemy.exc.IntegrityError, self.dbControl.map_object, o)

        o = DBmodels.Website(name="Test", address="Test", protocol="Test")
        self.dbControl.map_object(o)
        result = self.dbControl.get_objects_of_class(DBmodels.Website, attribs={"name": "Test"})
        assert len(result) >= 1
        test_len = len(result)

        self.dbControl.remove_object(o.__class__, {"name": o.name})
        result = self.dbControl.get_objects_of_class(DBmodels.Website, attribs={"name": o.name})
        assert len(result) == test_len - 1

    def test_load_basic_db_structure(self):

        self.dbControl.load_basic_db_structure(clean=True)


