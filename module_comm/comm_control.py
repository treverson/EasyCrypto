from module_comm.bot_pool import BotPool
from module_comm.bot import Bot
from module_comm.parser_factory import ParserFactory
from module_comm.protocol_factory import ProtocolFactory


class CommControl:

    def __init__(self):

        self.__bot_pool = BotPool()
        self.__protocol_factory = ProtocolFactory()
        self.__parser_factory = ParserFactory()

    def use_command(self, command):
        exchange_bot = self.__create_exchange_bot(command)
        self.__bot_pool.add(exchange_bot)

    def __create_exchange_bot(self, specification):

        protocol_class = self.__get_protocol_class(specification["protocol"])
        parser_class = self.__get_parser_class(specification["name"])

        exchange_bot = Bot(
            protocol_class,
            parser_class,
            specification["address"],
            specification["action"],
            specification["parameters"]
        )

        return exchange_bot

    def __get_protocol_class(self, protocol_name):

        if protocol_name in self.__protocol_factory.get_protocols():
            return self.__protocol_factory.create(protocol_name)
        else:
            raise AttributeError("No such protocol")

    def __get_parser_class(self, parser_name):

        if parser_name in self.__parser_factory.get_parsers():
            return self.__parser_factory.create(parser_name)
        else:
            raise AttributeError("No such parser")
