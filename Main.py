import TraderBot
import botStorage
import random
from testStratPeak import peakFuncs
import yahooInterface
import Server


def runTradeBot(testing=True, store=None):
    if testing:
        storage = botStorage.Storage(gui=False, load=False)  # Create a Storage to put the bots in, you may only have one of these but can store up to 1 billion bots in it so that shouldn't be an issue, if it is contact me I can fix it
        # ^^^^^^ if you would like to clear your Storage (this will not delete the pastTransactions json files you have to do that yourself) but it will make the Storage forget
        # ^^^^^^ any bots it currently has, pass False as an argument on declaration, for example: botStorage.Storage(False)
    else:
        storage = store

    if storage.bots == dict():  # This just checks if there are no bots at all in the Storage and if so adds the bots we just added to the instances list as new bots in Storage
        # ---------------------------------------------------------------------------------------------------------------
        # Grab some stocks to work with, in this case top 30 most active of the day
        stocks = yahooInterface.get_day_most_active(30)
        # ---------------------------------------------------------------------------------------------------------------
        instances = []  # Create an empty list to store instances of strategy class, each with a random sellPct and random histLength
        # Create a server, this allows all of the bots to request syncronously meaning data isn't grabbed more than once
        # This should improve speed/efficiency by at least 2x so I highly recommend it.
        server = Server.Server(refresh_rate=1, super_charged=True, auto_tune=True, inc=1)

        for itr1 in range(3):  # make 3 bots, can set this to however many you want
            instances.append(peakFuncs({'sellPct': random.randint(0, 100), 'dateRange': random.randint(1,5), 'server': server}))  # append an instance of the strategy class to list of instances
        for inst in instances:
            bot = TraderBot.TradeBot(stocks, inst, storage, moneyDivisions=10, ignoreErrors=True)  # This is an example of how to create a bot, for more info see TraderBot.TradeBot docstring
            storage.new_bot(bot)  # This is how to add an instance of a TradeBot to your Storage
    storage.run_bots()  # This is how to run all active bots in your Storage, activation and deactivation functionality not offered yet


if __name__ == '__main__':
    runTradeBot()
