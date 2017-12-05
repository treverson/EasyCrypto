import threading


class Bot(threading.Thread):

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
        self.__parser = parser_class()
        self.__action = action
        self.__parameters = parameters

    def run(self):

        self.__protocol.do(self.__action)

    def action(self, data):

        if self.__action == "ticker":
            parsed = self.__parser.ticker(data, self.__parameters)
            if parsed is not None:
                self.done = True
                print(parsed)
                self.__protocol.stop()

    def __str__(self):

        msg = "Bot {} on protocol {}, address: {}".format(
            self.__parser,
            self.__protocol,
            self.address
        )

        return msg