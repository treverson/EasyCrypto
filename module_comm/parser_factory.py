import json

from module_db.db_models import load_args, Website, Ticker
from module_db.db_control import DBControl


class PoloniexWAMPParser:

    def __init__(self, bot):

        self.db_control = DBControl()
        self.bot = bot

    def process(self, data, action, parameters):

        if action == "ticker":
            parsed = self.__ticker(data, parameters)

            if parsed is not None:
                self.__save_ticker(parsed)

    def __ticker(self, data, parameters):

        formatted_data = '{0}: {1} A:{2} B:{3} {4}% V:{5} H:{8} L:{9}'.format(*data)

        if parameters["currency_pair"] in formatted_data:

            attribs = {"name": get_parser_name(self.__str__())}
            website_data = self.db_control.get_objects_of_rsclass(Website, attribs)
            website_id = [website.website_id for website in website_data][0]

            ticker_data = {
                "website_id": website_id,
                "currency_pair": parameters["currency_pair"],
                "last_price": data[1],
                "lowest_ask": data[2],
                "highest_bid": data[3]
            }

            ticker = Ticker()
            load_args(ticker, ticker_data)

            self.__save_ticker(ticker)
            return ticker

        return None

    def __save_ticker(self, DTO):

        self.db_control.map_object(DTO)

    def __str__(self):

        return "Poloniex WAMP"


class PoloniexRESTParser:

    def __init__(self, bot):

        self.db_control = DBControl()
        self.bot = bot

    def process(self, data, action, parameters):

        if action == "returnTicker":
            parsed = self.__returnTicker(data, parameters)

            if parsed is not None:
                self.__save_ticker(parsed)

    def __returnTicker(self, data, parameters):

        data = data.decode("utf-8").replace("'", "\"")
        data = json.loads(data)

        if parameters["currency_pair"] in data:

            data = data[parameters["currency_pair"]]
            attribs = {"name": get_parser_name(self.__str__())}
            website_data = self.db_control.get_objects_of_class(Website, attribs)
            website_id = [website.website_id for website in website_data][0]

            ticker_data = {
                "website_id": website_id,
                "currency_pair": parameters["currency_pair"],
                "last_price": data["last"],
                "lowest_ask": data["lowestAsk"],
                "highest_bid": data["highestBid"]
            }

            ticker = Ticker()
            load_args(ticker, ticker_data)

            self.__save_ticker(ticker)
            return ticker

        return None

    def __save_ticker(self, DTO):

        self.db_control.map_object(DTO)

    def __str__(self):

        return "Poloniex REST"


class BittrexRESTParser:

    def __init__(self, bot):

        self.db_control = DBControl()
        self.bot = bot

    def process(self, data, action, parameters):

        if action == "public/getcurrencies":

            print(data.decode("utf-8"))

    def __str__(self):

        return "Bittrex REST"


class ParserFactory:

    __parsers = {
        "Poloniex REST":  PoloniexRESTParser,
        "Poloniex WAMP":  PoloniexWAMPParser,
        "Bittrex REST":   BittrexRESTParser
    }

    def get_parsers(self):

        return self.__parsers.keys()

    def create(self, parser_name):

        return self.__parsers[parser_name]


def get_parser_name(full_name):

    return full_name.split(" ")[0]