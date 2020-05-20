import datetime
import yahooInterface
import Server


class peakFuncs():
    """
    ---------------------------------------------------------------------------------------------------------------
    This class must contain 3 functions in order to work:

    getInfo must be a function that returns info that will be passed to the other functions
    ---------------------------------------------------------------------------------------------------------------
    buyStrategy must accept the result of getInfo and return a list of stocks to buy or a blank list if none
    ---------------------------------------------------------------------------------------------------------------
    sellStrategy must accept the result of getInfo and return a list of stocks to sell or a blank list if none
    ---------------------------------------------------------------------------------------------------------------

    ----------------------------------------------------------------------------------------------------------------
    IMPORTANT INFORMATION
    ----------------------------------------------------------------------------------------------------------------
    This is a sample class but you are not at all limited to one, I factored in wanting to test a wide variety of
    strategies so you can make as many of these classes as you want and place them in whatever files you want as
    long as you pass an instance of it upon initialization of the trade bot for that specific strategy.

    The only comdition for the class is it must have the 3 functions above and if it has vars passed on init it must
    save them as an variable of the class self.initVars shown below in __init__

    WARNING once you pass an instance of this class and make a bot, DO NOT delete or move the python file where the class
    is stored or the bot will break, it looks for this file to initialize the bot every time the bots need to load up on boot
    """

    def __init__(self, initVars):
        """
        ----------------------------------------------------------------------------------------------------------------
        WARNING if you want to change any values within the class slightly for testing purposes I suggest passing them
        in on initialization.
        ----------------------------------------------------------------------------------------------------------------
        WARNING if you do not set self.initVars = to your initVariables (init must only take 1 parameter so put your
        variables in a list if you need multiple, an example of how to use lists even for default values is shown
        below, for large amounts of init vars I suggest using a dictionary to keep track of which ones are being
        poassed in) if you do not set self.initVars = initVars then when you try to load your bot in it will error
        ----------------------------------------------------------------------------------------------------------------
        WARNING initVars must contain only json serializable datatypes, for example: int, str, bool, float, and null
        to learn more about what datatypes can be stored look up jsonpickle
        ----------------------------------------------------------------------------------------------------------------
        """
        self.initVars = initVars
        self.sellPct = initVars['sellPct']
        if 'dateRange' in initVars:
            self.dateRange = initVars['dateRange']
        else:
            self.dateRange = None
        if 'server' in initVars:
            self.server = initVars['server']
        else:
            self.server = None

    def getInfo(self, stocks):
        """

        ----------------------------------------------------------------------------------------------------------------
        stocks is a list of string stock symbols, to grab the info for a stock you can use any means you want but
        to make it easy I set up yahooInterface.py see it's documentation on instructions for how to use it
        ----------------------------------------------------------------------------------------------------------------

        ----------------------------------------------------------------------------------------------------------------
        GUIDE FOR GENERAL USE:
        This function needs to return a dictionary (Yes it MUST be a dictionary my program needs the symbols)
        ----------------------------------------------------------------------------------------------------------------
        The keys in the dictionary MUST be the string version of the stock symbol

        The values in the divtionary can be anything you want but it should contain all of the data your functions need
        in order to make a decision on whether you need to buy or sell, formatting for data is important, see below.
        ----------------------------------------------------------------------------------------------------------------
        The grabInfo function from yahooInterface.py returns the data in the exact format needed if you need an example
        of how the data will be formatted. If you plan on using my GUI your data needs to be in only dictionary or list
        containers, anything else will be displayed as whole not iterated through.
        ----------------------------------------------------------------------------------------------------------------
        """

        # WARNING YOU MUST BE ABLE TO INDEX THE RETURN VALUE value[stock]['live_price'] SO MAKE SURE YOU GRAB THE LIVE
        # PRICE WHETHER YOU NEED IT FOR YOUR PURPOSES OR NOT IT'S NEEDED FOR LOGGING INFORMATION
        if self.server is None:
            return yahooInterface.grabInfo(stocks, ['quote_table', 'history', 'live_price'], histLength=self.dateRange, superCharged=True)
        return self.server.request(stocks, ['quote_table', 'history', 'live_price'], histLength=self.dateRange)

    def buyStrategy(self, stocks):
        """
        ----------------------------------------------------------------------------------------------------------------
        stocks = {sym: data, sym: data, sym: data...}

        (example of potenetial data)
        data = {'quote_table': quote_table, 'history': history, 'live_price': live_price}

        stocks = dict of syms ==> (string)sym: {'quote_table': quote_table, 'history': history} (this is example data
        returned from my getInfo function, it's whatever's returned from your getInfo function)
        ----------------------------------------------------------------------------------------------------------------

        ---------------------------------------------------------------------------------------------------------------
        GUIDE FOR GENERAL USE:
        This function accepts the output from the getInfo function you define (any stocks you currently own will be
        removed from the list prior to being passed to the function so you don't have to worry about accounting for
        duplicates)
        ---------------------------------------------------------------------------------------------------------------
        You can do whatever you want within the function to make your decision but the function must return a dictionary
        of the exact same format as getInfo must return. Basically take any entries from the dictionary passed in and
        copy their key as a key in a new dictionary and their value as the value corresponding to the key
        for example: (string)sym: (list)stockData
        ---------------------------------------------------------------------------------------------------------------
        I STRONGLY advise copying my code for checking if the market is open into your functions, or at least taking
        into account that the general stock market is not open 24/7, my bot will run any time so if it is not market
        hours I just have my buy function return an empty list
        ---------------------------------------------------------------------------------------------------------------
        """

        # You can change anything below here (as long as you follow formatting rules above)

        # Below is an example of a basic "peak" buying strategy, I encourage you to make your own though as this one
        # is not the best. Good Luck!

        # -------------------------------------------------------------------------------------------------------------

        # Checking to see if the market is open, I strongly advise doing this!
        if not marketOpen():
            print('market closed nothing will be bought or sold')
            return dict()

        # Calls getChange (function shown below if you're curious) which returns a dictionary of {str(symbol): int(pct change)}
        pctgs = getChange(stocks)[1]
        # Initiates empty dictionary in which to store only positively growing stocks
        posi = dict()
        # iterates through the dictionary declared above
        for itr1 in pctgs:
            # if the percentage grown is > 0 then append it to the positive growth list
            if pctgs[itr1] > 0:
                posi[itr1] = pctgs[itr1]
        # sort the dictionary of positive values from greatest to least (WARNING THIS ONLY WORKS IN python 3.7+ use lists if using a lower version)
        posi = sorted(posi, key=lambda pctg: posi[pctg])
        # Initialize dictionary to store all stocks we want to purchase
        purchases = dict()
        for stockInd in posi:
            # gets current stock price
            stock_price = stocks[stockInd]['live_price']
            # gets the highest price the stocks been at for the week
            stock_high = sorted(stocks[stockInd]['history'], key=lambda info: info['high'])[0]['high']

            if stock_price > stock_high:  # stock price > stock high for given time range
                # Buy stock if change is positive and it's above it's high for given time range
                purchases[stockInd] = stocks[stockInd]
        return purchases

    def sellStrategy(self, stocks):
        """
        ---------------------------------------------------------------------------------------------------------------
        stocks is a list [[x,y], [x,y]...]
        ---------------------------------------------------------------------------------------------------------------
        x = data returned from self.getInfo()
        y = Stock class with original purchase data, for more info on Stock class see Stock class in TraderBot.py
        ---------------------------------------------------------------------------------------------------------------

        ---------------------------------------------------------------------------------------------------------------
        GENERAL USE GUIDE:
        ---------------------------------------------------------------------------------------------------------------
        This function accepts stocks (explained above) and must return a list of 3D lists. The first two elements must be
        x, then y from the above explanation but you must add a third element to the list, the current live price.
        This is so I can know how much the stock sold for and determine profit as well as log the info.

        An example of return format:
        return [[a,b,c], [a,b,c], ...] <=== stocks to be sold, if none return an empty list

        a = x from stocks (from above explanation)
        b = y from stocks (the instance of the Stock class, from above explanation) WARNING THIS MUST CONTAIN live_price
        """
        # Checking to see if the market is open, I strongly advise doing this!
        if not marketOpen():
            print('market closed nothing will be bought or sold')
            return dict()

        # creates a list of stocks to sell
        sellList = []
        # iterates through stocks, Stock is = [current data, Stock class data (original purchase)]
        for Stock in stocks:
            # sets stock = the current data
            stock = Stock[0]
            # if purchase price is > current value then sell
            if Stock[1].value > stock['live_price']:
                sellList.append(Stock)
            else:
                # grab all of the data from the day of purchase until today
                data5Filt = yahooInterface.grabInfo([Stock[1].symbol], ['history'],
                                                      histLength=(datetime.date.today() - Stock[1].date).days + 1)[Stock[1].symbol]
                # grab the current price
                curPrice = stock['live_price']
                # sort the data by it's "high's" or max price for the day
                data5Filt = sorted(data5Filt['history'], key=lambda info: info['high'])
                # figure out the growth, for example if you bought it at 10 and it's now 12 the growth would be 2
                growth = curPrice - Stock[1].value
                # figure out the max growth, this is the max the stock has grown since you bought it
                # for example if you bought the stock at 10, it went to 15 and is now at 12, the max growth would be 5
                maxGrowth = data5Filt[0]['high'] - Stock[1].value
                # check if the growth / maxGrowth is < the threshold to sell, for example if the stock was bought at
                # 10 it went to 15 and is now at 12 and you set your sell threshold to 50% on initialization of the class
                # then the stock would be sold because the growth (2) / max growth (5) would be 40% which is < 50%, your threshold
                if growth / maxGrowth < self.sellPct:
                    sellList.append(Stock)
        return sellList


def getChange(stocks):
    chg = dict()
    pctgs = dict()
    for stock in stocks:
        amt = stocks[stock]['quote_table']['Forward Dividend & Yield']
        if 'n/a' in amt.lower():
            chg[stock] = [0, 0]
            pctgs[stock] = 0
        else:
            amt = amt.split(' ')
            if amt[0][0] == '-':
                amt[0] = float(amt[0][1:]) * -1
            else:
                amt[0] = float(amt[0][1:])
            if amt[1][1] == '-':
                amt[1] = float(amt[1][2:-2]) * -1
            else:
                amt[1] = float(amt[1][2:-2])
            chg[stock] = amt
            pctgs[stock] = amt[1]
    return [chg, pctgs]

def marketOpen():
    today = datetime.datetime.now()
    hour = today.hour
    minutes = today.minute
    if today.weekday() == 5 or today.weekday() == 6:
        return False
    if hour == 9:
        if minutes < 30:
            return False
    elif hour > 16 or hour < 9:
        return False
    return True
