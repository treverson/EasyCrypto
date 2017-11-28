import inspect
import json
import os

from sqlalchemy import create_engine
from sqlalchemy.exc import ArgumentError, OperationalError
from sqlalchemy.orm import sessionmaker

from module_db import DBmodels
from module_db.DBmodels import Base
from utilities import logger

class DBControl:

    def __init__(self):

        self.__create_logger()
        self.__secure_create_engine()
        self.__configure_sessionmaker()

    def is_correct_class(self, object_to_map):
        """ Checks if object is an instance of one of the classes in the DBmodels.py
        """

        names = inspect.getmembers(DBmodels, inspect.isclass)
        DBmodels_classes = tuple(x[1] for x in names)

        for DBmodels_class in DBmodels_classes:
            if isinstance(object_to_map, DBmodels_class):
                return True
        return False

    def load_basic_db_structure(self, clean=False):
        """ Creates the most basic structure of database

        The structure is loaded from db.txt, which holds a JSON

        Parameter clean allows to remove all records from the base
        if a fresh start is needed
        """

        if clean:
            self.__clear_all_tables()

        self.__logger.info("Loading basic database structure")
        path = os.path.dirname(os.path.abspath(__file__))
        files = os.listdir(path+"/data")
        for file in files:
            self.__load_object_from_json("{}/data/{}".format(path, file))

        self.__logger.info("Loading basic database structure successful")

    def map_object(self, object_to_map):
        """ Maps received object to the database

        Object must be an instance of one of the classes in DBmodels.py
        """

        if not self.is_correct_class(object_to_map):
            self.__logger.error("Object to be mapped is of wrong type")

        session = self.__Session()
        session.add(object_to_map)
        session.commit()
        session.query(object_to_map.__class__).all()

        session.close()

    def get_objects_of_class(self, class_to_get, attribs={}):
        """ Selects objects from database

        class_to_get - specifies the table
        attribs - results of query are filtered by this dict
        """

        session = self.__Session()
        results = session.query(class_to_get)

        results = self.__get_filtered_results(results, class_to_get, attribs)

        session.close()

        return results

    def remove_object(self, class_to_remove, attribs):
        """ Removes specific object from database

        class_to_remove - specifies the table
        attribs - records holding attributes given in attribs will be removed
        """

        session = self.__Session()

        results = session.query(class_to_remove)
        results = self.__get_filtered_results(results, class_to_remove, attribs)

        for result in results:
            session.delete(result)

        session.commit()
        session.close()

    def __create_logger(self):

        self.__logger = logger.create_logger("module_db")

    # <editor-fold desc="Connection setup code">
    def __secure_create_engine(self):

        try:

            self.__try_connection()

        except (ArgumentError, OperationalError):

            self.__logger.error("Could not connect to the database")

            self.__create_db()
            self.__create_tables()

            self.__try_connection()

    def __try_connection(self):

        self.__logger.info("Setting up connection to the database")

        password = self.__load_password()
        self.__engine = create_engine("postgresql://postgres:"+password+"@localhost/easycrypto")
        self.is_connected()

        self.__logger.info("Connected to the database")

    def __create_db(self):

        self.__logger.info("Creating database EasyCrypto")
        password = self.__load_password()
        engine = create_engine("postgresql://postgres:"+password+"@localhost/postgres")
        conn = engine.connect()
        conn.execute("commit")
        conn.execute("create database EasyCrypto")
        conn.close()
        self.__logger.info("Creation of EasyCrypto successful ")

    def is_connected(self):
        """Checks if connection to the db is possible

        Returns truth value whether connection has been created
        """

        conn = self.__engine.connect()
        return conn is not None

    def __create_tables(self):

        self.__logger.info("Creating tables in database")
        Base.metadata.create_all(self.__engine)
        self.__logger.info("Successfully created tables in database")

    def __configure_sessionmaker(self):

        self.__logger.info("Configuring sessionmaker")
        self.__Session = sessionmaker(bind=self.__engine)
        self.__logger.info("Successfully configured sessionmaker")

    def __load_password(self):

        self.__logger.info("Loading database password")

        path = os.path.dirname(os.path.abspath(__file__))
        with open("{}/pass.txt".format(path), "r") as f:
            password = f.read()

        self.__logger.info("Loading database password successful")
        return password
    # </editor-fold>

    def __load_object_from_json(self, file_name):

        with open(file_name, "r") as f:
            data = json.load(f)

        website = DBmodels.Website()
        DBmodels.load_args(website, data["Website"])
        self.map_object(website)

        for action_data in data["Action"]:
            action = DBmodels.Action()
            DBmodels.load_args(action, action_data)
            action.website_id = website.website_id
            self.map_object(action)

        if "Parameter" not in data:
            return
        
        parameter = DBmodels.Parameter()
        DBmodels.load_args(parameter, data["Parameter"])
        self.map_object(parameter)

        specification = DBmodels.Specification()

        action_address = data["Specification"]["action_address"]
        action_id = self.get_objects_of_class(DBmodels.Action, {"address": action_address})[0].action_id

        parameter_name = data["Specification"]["parameter_name"]
        parameter_id = self.get_objects_of_class(DBmodels.Parameter, {"name": parameter_name})[0].parameter_id

        specification.action_id = action_id
        specification.parameter_id = parameter_id
        self.map_object(specification)

    def __clear_all_tables(self):

        self.__logger.info("Clearing all database tables")
        Base.metadata.drop_all(bind=self.__engine)
        Base.metadata.create_all(bind=self.__engine)
        self.__logger.info("Clearing all database tables successful")

    def __get_filtered_results(self, results, class_to_get, attribs):

        for attr, value in attribs.items():
            if isinstance(value, list):
                results = results.filter(getattr(class_to_get, attr).in_(value))
            else:
                results = results.filter(getattr(class_to_get, attr) == value)
        results = results.all()
        return results