

class Bot:

    def __init__(
            self,
            protocol_class,
            parser_class,
            address,
            action,
            parameters):

        self.__protocol = protocol_class(address)
        self.__parser = parser_class()
        self.__action = action
        self.__parameters = parameters

    def do(self):

        self.__protocol.do(self.__action)