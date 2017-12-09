import threading
from module_db.db_control import DBControl

class Bot:

    def __init__(
            self,
            protocol_class,
            parser_class,
            address,
            action,
            parameters):

        threading.Thread.__init__(self)

        self.done = False
        self.address = address
        self.__protocol = protocol_class(url=self.address, bot=self)
        self.__parser = parser_class(bot=self)
        self.__action = action
        self.__parameters = parameters

        self.db_control = DBControl()

    def run(self):

        self.__protocol.do(self.__action)

    def action(self, data):

        if self.__action == "ticker":
            parsed = self.__parser.ticker(data, self.__parameters)
            if parsed is not None:

                self.done = True
                self.__protocol.stop()
                self.__save_ticker(parsed)

        elif self.__action == "trollbox":
            print("tutaj")
            parsed = self.__parser.trollbox(data)
            print(parsed)
            self.done = True
            self.__protocol.stop()


    def __save_ticker(self, DTO):

        self.db_control.map_object(DTO)

    def __str__(self):

        msg = "Bot {} on protocol {}, address: {}".format(
            self.__parser,
            self.__protocol,
            self.address
        )

        return msg