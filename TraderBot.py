import json
import time
from threading import Thread
import datetime

import jsonpickle


class TradeBot:
    def __init__(self, stocks, strategyClass, storage, id=None, startMoney=1000,
                 moneyDivisions=5, printStatus=True, ignoreErrors=False, errorTime=5):
        """

        @params

        stocks must be a list of strings of stock symbols
        ----------------------------------------------------------------------------------------------------------------
        stategyClass must be a class object containing 3 functions, getInfo, buyStrategy, and sellStrategy

        getInfo must be a function that returns info that will be passed to the other functions
        buyStrategy must accept the result of getInfo and return a list of stocks to buy or a blank list if none
        sellStrategy must accept the result of getInfo and return a list of stocks to sell or a blank list if none
        ----------------------------------------------------------------------------------------------------------------
        Storage must be an instance of the Storage class from botStorage.py this is used to keep track of all of
        your bots along with their transaction information
        ----------------------------------------------------------------------------------------------------------------
        id I would suggest leaving as none as your bots ID will be a randomly generated 9 digit number
        (guaranteeing no conflicts with other bot id's) but if you would like to use your own id system feel free
        just beware of saving two bots under the same id, one will be deleted
        ----------------------------------------------------------------------------------------------------------------
        startMoney is the total amount of money your bot starts with, default is 1000 but set it to whatever you want
        if you'd like to customize how your bank looks you can pass in a list of integers for this parameter allowing
        you to customize how many divisions of money you have and the amount in each, for example:
        [100, 200, 300, 400, 100, 100, 490, 280, 280] etc.

        I strongly suggest simply declaring a starting amount and divisions and not using a list as you can't currently
        choose which stocks it buys more or less of but the option is there.
        ----------------------------------------------------------------------------------------------------------------
        moneyDivisions is the amount of portions your money will be split into. For example the default value is 5 and
        the default startMoney is 1000 so your starting bank will be [200, 200, 200, 200, 200] and the max amount of
        stocks your bot can hold at one time would be 5.
        ----------------------------------------------------------------------------------------------------------------
        printStatus if this variable is set to true then the print statements I have throughout the bot will display the
        status while it runs, set to False if you don't want this
        ----------------------------------------------------------------------------------------------------------------
        ignoreErrors if this is set to True then any errors occurring within the program will be caught and ignored.
        they will be printed to the screen and this bot will stop for errorTime seconds
        ----------------------------------------------------------------------------------------------------------------
        errorTime an int or float the amount of time the program will sleep for when an error occurs

        """

        self.storage = storage
        self.classInfo = str(type(strategyClass)).split()[1].split("'")[1].split('.')
        if id == None:
            id = storage.gen_id()
        self.id = id
        try:
            self.stratClassInit = strategyClass.initVars
        except NameError:
            pass
        self.strategyClass = strategyClass
        self.getInfo = strategyClass.getInfo
        self.stocks = stocks
        self.buyStrategy = strategyClass.buyStrategy
        self.sellStrategy = strategyClass.sellStrategy
        self.ignoreErrors = ignoreErrors
        self.errorTime = errorTime
        self.bought = []
        self.timesRan = 0
        self.loadTransactions()
        self.printStatus = printStatus
        if isinstance(startMoney, int):
            self.bank = []
            if startMoney > 0:
                portion = startMoney / moneyDivisions
                for itr1 in range(moneyDivisions):
                    self.bank.append(portion)
            else:
                raise Exception('startMoney must be > 0!')
        elif isinstance(startMoney, list):
            self.bank = startMoney
        else:
            raise TypeError("Invalid type given for startMoney, must be int or list")




    def main(self):
        # I do not plan on documenting any of this as honestly some of it is extremely in depth and confusing, ask Biz
        # if you have any questions on how it works and he'll explain it
        startTime = time.time()
        self.stockInfo = self.getInfo(self.stocks)
        if self.storage.gui != None:
            self.storage.gui.updateBot(self.stockInfo, self.id)
        buyInfo, sellInfo = self.gatherInfo() #buyInfo is a dict, sellInfo is [x,y] x= stockData, y=purchaseData
        if self.printStatus:
            print(self.id, ' bank at start:', self.bank)
            print(self.id, ' stocks before transactions:', self.bought)
        buyChoice = self.buyStrategy(buyInfo)
        sellChoice = self.sellStrategy(sellInfo)
        if self.printStatus:
            print(self.id, ' options of buying:', len(buyChoice))
        for itr1 in buyChoice:
            if len(self.bank) > 0:
                self.buyStock(buyChoice[itr1], itr1)
            else:
                if self.printStatus:
                    print(self.id, ' tried to purchase:', itr1, ', your bot has no money!')
                break
        for itr1 in sellChoice:
            self.sellStock(itr1)
        if self.transactions != []:
            self.exportTransactions()
        self.storage.export_bots()
        if self.printStatus:
            print(self.id, ' stocks after transactions:', self.bought)
            print(self.id, ' bank at end:', self.bank)
            print(self.id, ' main finished in:', time.time() - startTime)
            print('\n')
        self.timesRan += 1

    def runMain(self):
        if self.ignoreErrors:
            while self.running:
                try:
                    self.main()
                except Exception as e:
                    print(f'Error occurred while running bot: {e}')
                    time.sleep(self.errorTime)
        else:
            while self.running:
                self.main()

    def run(self):
        tempThread = Thread(target=self.runMain)
        self.running = True
        tempThread.start()

    def stop(self):
        self.running = False

    def buyStock(self, info, sym):
        boughtStock = Stock(sym, info, self.bank.pop(0), datetime.date.today())
        self.bought.append(boughtStock)
        if self.printStatus:
            print('Bought stock:', boughtStock.symbol)

    def sellStock(self, data):
        sym = data[1].symbol
        for itr1 in self.bought:
            if itr1.symbol == sym:
                if self.printStatus:
                    print("\nstock ", sym, ", ", itr1.shares, " sold for ", str(data[0]['live_price']), sep='')
                profit = (itr1.shares*data[0]['live_price']) - (itr1.shares*itr1.price)
                if self.printStatus:
                    print('originally bought at', itr1.price, 'total profit:', profit)
                print(data)
                self.transactions.append([sym, data[0], data[1].data])
                self.bank.append(itr1.shares * float(data[0]['live_price']))
                while itr1 in self.bought:
                    self.bought.remove(itr1)
        self.exportTransactions()



    def loadTransactions(self):
        try:
            with open(r'Bots\pastTransactions' + str(self.id) + '.json', 'r') as file:
                self.transactions = json.load(file)
        except:
            self.transactions = []

    def exportTransactions(self):
        with open(r'Bots\pastTransactions' + str(self.id) + '.json', 'w') as file:
            json.dump(self.transactions, file, indent=4)



    def gatherInfo(self):
        info = self.stockInfo.copy()
        buyInfo = dict()
        sellInfo = []
        for sym in info:
            notBought = True
            for bought in self.bought:
                if sym == bought.symbol:
                    sellInfo.append([info[sym], bought])
                    notBought = False
            if notBought:
                buyInfo[sym] = info[sym]


        return buyInfo, sellInfo

class Stock:
    def __init__(self, symbol, data, cash, purchTime):
        self.symbol = symbol
        self.data = data
        self.cash = cash
        self.date = purchTime
        self.price = data['live_price']
        self.shares = cash / self.price
        self.value = self.price * self.shares

    def __repr__(self):
        return self.symbol

    def __str__(self):
        return self.symbol

def formatTime(purchTime):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    retStr = str(months[purchTime.month - 1]) + ' '
    retStr += str(purchTime.day) + ', '
    retStr += str(purchTime.year)
    return retStr