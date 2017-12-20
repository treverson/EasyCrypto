class Bot:

    def __init__(
            self,
            protocol_class,
            parser_class,
            address,
            action,
            parameters):

        self.done = False
        self.address = address
        self.__protocol = protocol_class(url=self.address, bot=self)
        self.__parser = parser_class(bot=self)
        self.__action = action
        self.__parameters = parameters

    def run(self):

        self.__protocol.do(self.__action)

    def action(self, data):

        self.__parser.process(data, self.__action, self.__parameters)

    def stop(self):

        self.done = True
        self.__protocol.stop()

    def __str__(self):

        msg = "Bot {} on protocol {}, address: {}".format(
            self.__parser,
            self.__protocol,
            self.address
        )

        return msg
