

class PoloniexParser:

    def ticker(self, data, parameters):

        data = '{0}: {1} A:{2} B:{3} {4}% V:{5} H:{8} L:{9}'.format(*data)
        if parameters["currency_pair"] in data:
            return data

        return None

    def __str__(self):

        return "Poloniex"

class ParserFactory:

    __parsers = {
        "Poloniex":  PoloniexParser
    }

    def get_parsers(self):

        return self.__parsers.keys()

    def create(self, parser_name):

        return self.__parsers[parser_name]
