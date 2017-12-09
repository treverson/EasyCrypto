from module_db.db_models import load_args, Website, Ticker


class PoloniexParser:

    def __init__(self, bot):

        self.bot = bot

    def ticker(self, data, parameters):

        formatted_data = '{0}: {1} A:{2} B:{3} {4}% V:{5} H:{8} L:{9}'.format(*data)

        if parameters["currency_pair"] in formatted_data:

            attribs = {"name": self.__str__()}
            print(attribs)
            website_data = self.bot.db_control.get_objects_of_class(Website, attribs)
            print(website_data)
            website_id = [website.website_id for website in website_data][0]
            print(website_id)

            ticker_data = {
                "website_id": website_id,
                "currency_pair": parameters["currency_pair"],
                "last_price": data[1],
                "lowest_ask": data[2],
                "highest_bid": data[3]
            }
            print(ticker_data)
            ticker = Ticker()
            load_args(ticker, ticker_data)

            print(ticker.__dict__)
            return ticker

        return None

    def trollbox(self, data):

        return data

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
