import os
import sys

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, QUrl, pyqtSlot

from GUImodels import WebsiteModel, ActionModel
from GUIqmlControl import WebsiteSlot
from module_db import DBcontrol, DBmodels
from utilities import logger, one_time


class GUIControl:



    def __init__(self):

        self.__create_logger()
        self.__create_db_control()
        self.__setup()

    def __create_logger(self):

        self.__logger = logger.create_logger("module_gui")

    def __create_db_control(self):

        self.__db_control = DBcontrol.DBControl()

    def __setup(self):

        self.app = QGuiApplication(sys.argv)

        self.__engine = QQmlApplicationEngine()

        self.__attach_slots()
        self.__engine.load(QUrl.fromLocalFile("main.qml"))

        self.__update_buttons_state({"executeButton": 0, "refreshButton": 1, "quitButton": 1})
        self.__attach_events()

        root_context = self.__engine.rootContext()
        print(root_context.contextProperty("websiteSlot"))
        sys.exit(self.app.exec_())

    def __attach_slots(self):
        root_context = self.__engine.rootContext()
        self.website_slot = WebsiteSlot()
        root_context.setContextProperty("websiteSlot", self.website_slot)

    def __update_buttons_state(self, states):

        translator = {
            "executeButton": "executeMouseArea",
            "refreshButton": "refreshMouseArea",
            "quitButton": "quitMouseArea"
        }

        for state in states:

            state_name = translator[state]
            button = self.__engine.rootObjects()[0].findChild(QObject, state_name)
            button.setProperty("enabled", states[state] == 1)

    def __attach_events(self):

        self.__logger.info("Attaching slots to signals")
        button = self.__engine.rootObjects()[0].findChild(QObject, "refreshMouseArea")
        button.refreshEvent.connect(self.__refresh_event_print)

        button = self.__engine.rootObjects()[0].findChild(QObject, "executeMouseArea")
        button.executeEvent.connect(self.__execute_event_print)

        self.__logger.info("Attaching slots to signals successful")

    def __add_models_to_context(self):

        self.__logger.info("Adding models to QML context")
        root_context = self.__engine.rootContext()

        for model_name in self.__models:
            root_context.setContextProperty(model_name, self.__models[model_name])

        self.__logger.info("Adding models to QML context successful")

    def __refresh_event_print(self):
        print("działa - refresh")
        self.__models = self.__load_website()
        self.__add_models_to_context()

    def __execute_event_print(self):
        print("działa - execute")

    def __load_website(self):

        website_data = self.__db_control.get_objects_of_class(DBmodels.Website)
        website_names = [website.name for website in website_data]
        return {"websiteModel": WebsiteModel(names=website_names)}

    def __load_action(self):

        website = self.__engine.rootObjects()[0].findChild(QObject, "websiteListView")

        print(website.property("currentItem"))

        meta = website.metaObject()
        methods = [meta.property(i).name() for i in range(meta.propertyCount())]
        currentItem = meta.property(methods.index("currentItem"))
        print(currentItem.read())
        action_data = self.__db_control.get_objects_of_class(DBmodels.Action)
        action_addresses = [action.address for action in action_data]
        return {"actionModel": ActionModel(names=action_addresses)}






