

class ParserFactory:

    __parsers = {
        "poloniex":  PoloniexParser
    }

    def get_parsers(self):

        return self.__parsers.keys()

    def create(self, parser_name):

        return self.__parsers[parser_name]


class PoloniexParser:

    def parser(self, data):

        print("nice")