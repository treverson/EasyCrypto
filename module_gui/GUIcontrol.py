import sys

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, QUrl

from GUImodels import ModelFactory
from GUIqmlControl import IndexChangedSlot
from module_db import DBcontrol, DBmodels
from utilities import logger, one_time


class GUIControl:

    def __init__(self):

        self.__models = {}
        self.__model_factory = ModelFactory()

        self.__create_logger()
        self.__create_db_control()
        self.__setup()

    def notify_website_clicked(self):

        self.__refresh_event_action()

    def notify_action_clicked(self):

        self.__refresh_event_parameter()

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

        sys.exit(self.app.exec_())

    def __attach_slots(self):
        root_context = self.__engine.rootContext()

        self.website_slot = IndexChangedSlot(callback=self.notify_website_clicked)
        root_context.setContextProperty("websiteSlot", self.website_slot)

        self.action_slot = IndexChangedSlot(callback=self.notify_action_clicked)
        root_context.setContextProperty("actionSlot", self.action_slot)

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
        button.refreshEvent.connect(self.__refresh_event_website)

        button = self.__engine.rootObjects()[0].findChild(QObject, "executeMouseArea")
        button.executeEvent.connect(self.__execute_event)

        self.__logger.info("Attaching slots to signals successful")

    def __add_models_to_context(self):

        self.__logger.info("Adding models to QML context")
        root_context = self.__engine.rootContext()

        for model_name in list(self.__models):
            root_context.setContextProperty(model_name, self.__models[model_name])

        self.__logger.info("Adding models to QML context successful")

    def __refresh_event_website(self):

        self.__load_website()
        self.__add_models_to_context()

    def __refresh_event_action(self):

        self.__load_action()
        self.__add_models_to_context()

    def __refresh_event_parameter(self):

        self.__load_parameters()
        self.__add_models_to_context()

    def __execute_event(self):
        print("działa - execute")

    def __load_website(self):

        self.__website_data = self.__db_control.get_objects_of_class(DBmodels.Website)
        website_names = [website.name for website in self.__website_data]

        website_model = self.__model_factory.create_model("WebsiteModel", {"name": website_names}, "name")
        self.__add_to_models({"websiteModel": website_model})

    def __load_action(self):

        selected_website = self.__website_data[self.website_slot.index]
        attribs = {"website_id": selected_website.website_id}

        self.__action_data = self.__db_control.get_objects_of_class(DBmodels.Action, attribs)
        action_addresses = [action.address for action in self.__action_data]

        action_model = self.__model_factory.create_model("ActionModel", {"address": action_addresses}, "address")
        self.__add_to_models({"actionModel": action_model})

    def __load_parameters(self):

        selected_action = self.__action_data[self.action_slot.index]
        attribs = {"action_id": selected_action.action_id}

        specification_data = self.__db_control.get_objects_of_class(DBmodels.Specification, attribs)
        parameter_id = [specification.parameter_id for specification in specification_data]
        attribs = {"parameter_id": parameter_id}

        parameter_data = self.__db_control.get_objects_of_class(DBmodels.Parameter, attribs)
        parameter_name = [parameter.name for parameter in parameter_data]
        parameter_type = [parameter.type for parameter in parameter_data]

        parameter_dict = {
            "name": parameter_name,
            "type": parameter_type
        }

        parameter_model = self.__model_factory.create_model("ParameterModel", parameter_dict, "name")
        self.__add_to_models({"parameterModel": parameter_model})

    def __add_to_models(self, new_models):

        for model_name in new_models:
            self.__models[model_name] = new_models[model_name]