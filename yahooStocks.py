import ssl
import time, threading
import urllib

from yahoo_fin import stock_info


def ignore_http(func):
    def wrapper(*args):
        passed = False
        error_count = 0
        while not passed:
            try:
                func(*args)
            except urllib.error.HTTPError:
                time.sleep(5)
                error_count += 1
            except ssl.SSLError:
                time.sleep(5)
                error_count += 1
            else:
                passed = True

    return wrapper


class Share():
    def __init__(self, symbol, fields, histLength=None, superCharged=False, storage=None):
        self.histLength=histLength
        self.stock = symbol
        inpDict = {'live_price': self.get_price, 'quote_table': self.get_data, 'history': self.get_history,
                   'analytics': self.get_analytics, 'income_statement': self.get_income_statement,
                   'balance_sheet': self.get_balance_sheet, 'cash_flow': self.get_cash_flow}
        self.orders = dict()
        for field in fields:
            self.orders[field] = inpDict[field]
        self.charged = superCharged
        if superCharged:
            self.stockStorage = storage
            self.storage = dict()
        else:
            self.storage = None

    def get_info(self):
        info = dict()
        if not self.charged:
            for order in self.orders:
                info[order] = self.orders[order]()
            return info
        else:
            threads = []
            for order in self.orders:
                thread = threading.Thread(target=self.orders[order])
                thread.start()
                threads.append(thread)
            wait_for_threads(threads)
            self.stockStorage[self.stock] = self.storage

    @ignore_http
    def get_history(self):
        '''if length is not specified, returns panda dataframe, else returns a list of however many days specified'''
        info = []
        data = stock_info.get_data(self.stock)
        headers = ['open', 'high', 'low', 'close', 'adj close', 'volume']
        if self.histLength != None:
            rows = data.iloc[:self.histLength]
            for itr2 in range(self.histLength):
                counter1 = 0
                rowData = dict()
                for itr1 in rows.iloc[itr2]:
                    if counter1 < 6:
                        rowData[headers[counter1]] = float(itr1)
                    counter1 += 1
                info.append(rowData)
        else:
            rows = data.iloc[:]
            for itr2 in range(len(rows)):
                counter1 = 0
                rowData = dict()
                for itr1 in rows.iloc[itr2]:
                    if counter1 < 6:
                        rowData[headers[counter1]] = float(itr1)
                    counter1 += 1
                info.append(rowData)
        if self.storage == None:
            return info
        else:
            self.storage['history'] = info

    @ignore_http
    def get_income_statement(self):
        if self.storage == None:
            return self.format1D(stock_info.get_income_statement(self.stock))
        else:
            self.storage['income_statement'] = self.format1D(stock_info.get_income_statement(self.stock))

    @ignore_http
    def get_balance_sheet(self):
        if self.storage == None:
            return self.format1D(stock_info.get_balance_sheet(self.stock))
        else:
            self.storage['balance_sheet'] = self.format1D(stock_info.get_balance_sheet(self.stock))

    @ignore_http
    def get_cash_flow(self):
        if self.storage == None:
            return self.format1D(stock_info.get_cash_flow(self.stock))
        else:
            self.storage['cash_flow'] = self.format1D(stock_info.get_cash_flow(self.stock))

    @ignore_http
    def get_analytics(self):
        if self.storage == None:
            return self.format2D(stock_info.get_analysts_info(self.stock))
        else:
            self.storage['analytics'] = self.format2D(stock_info.get_analysts_info(self.stock))

    @ignore_http
    def get_price(self):
        if not self.charged:
            return stock_info.get_live_price(self.stock)
        else:
            self.storage['live_price'] = stock_info.get_live_price(self.stock)

    @ignore_http
    def get_data(self):
        if self.storage == None:
            return stock_info.get_quote_table(self.stock)
        else:
            self.storage['quote_table'] = stock_info.get_quote_table(self.stock)

    @ignore_http
    def format2D(self, info):
        data = dict()
        for key in info:
            data[key] = self.format1D(info[key])
        return data

    @ignore_http
    def format1D(self, info):
        n = 0
        data = dict()
        keys = []
        while True:
            try:
                x = 0
                for itr1 in info.iloc[:, n]:
                    if n == 0:
                        keys.append(itr1)
                    elif n == 1:
                        data[keys[x]] = [itr1]
                    else:
                        data[keys[x]].append(itr1)
                    x += 1
                n += 1
            except IndexError:
                break
        return data



def wait_for_threads(threads):
    for thread in threads:
        thread.join()




