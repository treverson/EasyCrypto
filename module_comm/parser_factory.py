from module_db.db_models import load_args, Website, Ticker
from module_db.db_control import DBControl


class PoloniexParser:

    def __init__(self, bot):

        self.db_control = DBControl()
        self.bot = bot

    def process(self, data, action, parameters):

        if action == "ticker":
            parsed = self.__ticker(data, parameters)

            if parsed is not None:
                self.bot.stop()
                self.__save_ticker(parsed)

        elif action == "trollbox": #not supported by Poloniex
            parsed = self.__trollbox(data)
            self.bot.stop()

    def __ticker(self, data, parameters):

        formatted_data = '{0}: {1} A:{2} B:{3} {4}% V:{5} H:{8} L:{9}'.format(*data)

        if parameters["currency_pair"] in formatted_data:

            attribs = {"name": self.__str__()}
            website_data = self.bot.db_control.get_objects_of_class(Website, attribs)
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

            return ticker

        return None

    def __trollbox(self, data):

        return data

    def __save_ticker(self, DTO):

        self.db_control.map_object(DTO)

    def __str__(self):

        return "Poloniex"


class BittrexParser:

    def __init__(self, bot):

        self.db_control = DBControl()
        self.bot = bot

    def process(self, data, action, parameters):

        if action == "public/getcurrencies":

            print(data.deliverBody())
            self.__protocol.stop()
            print("koniec")

    def __str__(self):

        return "Bittrex"

class ParserFactory:

    __parsers = {
        "Poloniex":  PoloniexParser,
        "Bittrex":   BittrexParser
    }

    def get_parsers(self):

        return self.__parsers.keys()

    def create(self, parser_name):

        return self.__parsers[parser_name]
