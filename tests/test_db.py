import pytest
import mock

from pytest_mock import mocker

from src.db import db_control, db_models


@pytest.fixture
def db():
    """Returns a default DBControl instance"""

    return db_control.DBControl()


def test_can_connect(db):

    assert db.is_connected()

@pytest.mark.parametrize("object,assertValue", [
    (db_models.Website(), True),
    (db_models.Action(), True),
    (db_models.Parameter(), True),
    (db_models.Specification(), True),
    (db_models.Ticker(), True),
    ('', False),
    (None, False),
])
def test_is_correct_class(db, object, assertValue):

    assert db.is_correct_class(object) == assertValue


def test_load_basic_db_structure(db):

    raise NotImplementedError("Don't know how to test")


def test_map_object(mocker, db):

    raise NotImplementedError("TODO - implement session decorator")
    mocker.patch.object(db.map_object, 'session')

    db.map_object(db_models.Website())

    assert db.map_object.session.add.called
    assert db.Session.commit.called
    assert db.Session.query.called
