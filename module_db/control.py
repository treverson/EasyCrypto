from sqlalchemy import create_engine
from sqlalchemy.exc import ArgumentError, OperationalError
from sqlalchemy.orm import sessionmaker

import models
from models import Base

import os
import logging
import inspect
import json

"""
TODO: 
- logger as decorator
"""

class Control:
    __engine = None
    __logger = None
    __Session = None

    def __init__(self):

        self.__create_logger()
        self.__secure_create_engine()
        self.__configure_sessionmaker()

    def __assure_log_dir_exists(self, path):

        if(not os.path.exists(path + "/../logs/")):
            os.makedirs(path + "/../logs/")

    def __create_logger(self):

        logger = logging.getLogger("module_db")
        path = os.path.dirname(os.path.abspath(__file__))
        self.__assure_log_dir_exists(path)
        hdlr = logging.FileHandler(path + "/../logs/module_db.log")

        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        hdlr.setFormatter(formatter)

        logger.addHandler(hdlr)
        logger.setLevel(logging.INFO)

        self.__logger = logger

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
        with open("pass.txt", "r") as f:
            password = f.read()

        self.__logger.info("Loading database password successful")
        return password
    # </editor-fold>

    def is_correct_class(self, object_to_map):
        """ Checks if object is an instance of one of the classes in the models.py
        """

        names = inspect.getmembers(models, inspect.isclass)
        models_classes = tuple(x[1] for x in names)

        for models_class in models_classes:
            if isinstance(object_to_map, models_class):
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
        with open("db.txt", "r") as f:
            data = json.load(f)

        website = models.Website()
        models.load_args(website, data["Website"])
        self.map_object(website)

        action = models.Action()
        models.load_args(action, data["Action"])
        action.website_id = website.website_id
        self.map_object(action)

        parameter = models.Parameter()
        models.load_args(parameter, data["Parameter"])
        self.map_object(parameter)

        specification = models.Specification()
        specification.action_id = action.action_id
        specification.parameter_id = parameter.parameter_id
        self.map_object(specification)

        self.__logger.info("Loading basic database structure successful")

    def __clear_all_tables(self):

        self.__logger.info("Clearing all database tables")
        Base.metadata.drop_all(bind=self.__engine)
        Base.metadata.create_all(bind=self.__engine)
        self.__logger.info("Clearing all database tables successful")

    def map_object(self, object_to_map):
        """ Maps received object to the database

        Object must be an instance of one of the classes in models.py
        """

        if not self.is_correct_class(object_to_map):
            self.__logger.error("Object to be mapped is of wrong type")

        session = self.__Session()
        session.add(object_to_map)
        session.commit()
        session.query(object_to_map.__class__).all()

        session.close()

    def __get_filtered_results(self, results, class_to_get, attribs):

        for attr, value in attribs.items():
            results = results.filter(getattr(class_to_get, attr) == value)
        results = results.all()
        return results

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

