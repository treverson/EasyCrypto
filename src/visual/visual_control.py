import matplotlib.pyplot as plt
import pandas as pd

from src.db.db_control import DBControl
from src.db.db_models import Ticker


class VisualControl:

    def __init__(self):

        self.__db_control = DBControl()
        self.__actions = {
            "show ticker": self.__show_ticker
        }

    def use_command(self, command):

        if command["action"] in self.__actions:
            self.__actions[command["action"]](command)
        else:
            print("nope")

    def __show_ticker(self, command):

        currency_pair = command["parameters"]["currency_pair"]

        ticker_data = self.__db_control.get_objects_of_class(Ticker, command["parameters"])
        ticker_data = [float(ticker.last_price) for ticker in ticker_data]
        ticker_data = pd.DataFrame(ticker_data, columns=[currency_pair])
        ticker_data["x"] = list(range(len(ticker_data)))
        plt.plot('x', currency_pair, data=ticker_data, linestyle='-', marker='o')
        plt.show()
