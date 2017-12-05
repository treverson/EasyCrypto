

class BotPool:

    def __init__(self):

        self.__bot_pool = []

    def add(self, bot):

        self.__bot_pool.append(bot)
        bot.start()
