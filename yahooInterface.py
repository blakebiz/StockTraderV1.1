import yahooStocks, threading
from yahoo_fin import stock_info

def grabInfo(stocks, fields, histLength=None, superCharged=False):
    """

    stocks is a list of string stock symbols to grab info for

    fields is a list of strings regarding which info to grab and in what order, options are listed below.
    WARNING pass the strings in EXACTLY as they are listed below case-sensitive or the program will error.

    field options are: quote_table, history, live_price, analytics, income_statement, balance_sheet, and cash_flow

    """
    funcStorage = dict()
    if superCharged:
        threads = []
        for share in stocks:
            thread = threading.Thread(
                target=yahooStocks.Share(share, fields, histLength=histLength, superCharged=superCharged,
                                         storage=funcStorage).get_info)
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        return funcStorage
    for share in stocks:
        funcStorage[share] = yahooStocks.Share(share, fields, histLength=histLength).get_info()

    return funcStorage

def get_day_most_active(count=None):
    info = []
    if count == None:
        for itr1 in stock_info.get_day_most_active().iloc[:, 0]:
            info.append(itr1)
    else:
        counter = 0
        for itr1 in stock_info.get_day_most_active().iloc[:, 0]:
            if counter >= count:
                break
            else:
                info.append(itr1)
            counter += 1
    return info
