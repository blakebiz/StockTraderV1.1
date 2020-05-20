import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import yahooInterface

class IndicSelectWindow(QtWidgets.QDialog):
    def __init__(self, stocks, stock, parent=None):
        try:
            super().__init__(parent=parent)
            self.setWindowTitle(str(stock) + ' Info')
            self.resize(500, 400)
            self.layout = QtWidgets.QHBoxLayout(self)
            self.scrollArea = QtWidgets.QScrollArea(self)
            self.scrollArea.setWidgetResizable(True)
            self.scrollAreaWidgetContents = QtWidgets.QWidget()
            self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
            self.scrollArea.setWidget(self.scrollAreaWidgetContents)
            self.layout.addWidget(self.scrollArea)
            objs = dict()
            i = 0
            for key in stocks:
                '''stocks= {
                live_price: 3.7699999809265137,
                quote_table: {'1y Target Est': 2.98, '52 Week Range': '1.1900 - 10.6400', 'Ask': '3.7900 x 40700', ...}
                history: [{'open': 6.0, 'high': 6.929999828338623, 'low': 5.349999904632568, 'close': 6.599999904632568, 'adj close': 6.599999904632568, 'volume': 66849000.0}, ...]
                analytics: {'Earnings Estimate': {'No. of Analysts': [5.0, 4.0, 11.0, 13.0], 'Avg. Estimate': [-0.26, -0.27, -1.41, -0.82], ...}, ...}
                income_statement: {'Total Revenue': ['6582332', '4951171', '0', '0'], 'Cost of Revenue': ['7057509', '5207047', '-', '0'], ...}
                balance_sheet: {'Current Assets': [None, None, None], 'Cash': [None, None, None], 'Cash And Cash Equivalents': ['3133847', '7505954', '581296'], ...}
                cash_flow: {'Net Income': ['-10695309', '-9597274', '-4984734', '-2536316'], 'Depreciation & amortization': ['-', '-', '167858', '46087'], ...}
                }
                '''
                label = QtWidgets.QLabel()
                label.setText(str(key))
                objs[key] = [label]
                self.gridLayout.addWidget(label, i, 0)
                notFirst = False
                if isinstance(stocks[key], dict):
                    for deepKey in stocks[key]:
                        if isinstance(stocks[key][deepKey], dict):
                            if notFirst:
                                lbl1 = QtWidgets.QLabel()
                                objs[key].append(lbl1)
                                self.gridLayout.addWidget(lbl1, i, 0)
                            else:
                                notFirst = True
                            button = QtWidgets.QPushButton()
                            button.clicked.connect(connector(stocks[key][deepKey], self))
                            self.setText(button, deepKey)
                            objs[key].append(button)
                            self.gridLayout.addWidget(button, i, 1)
                            i += 1
                        else:
                            if not notFirst:
                                lbl3 = QtWidgets.QLabel()
                                objs[key].append(lbl3)
                                self.gridLayout.addWidget(lbl3, i, 1)
                                notFirst = True
                            elif notFirst:
                                lbl4 = QtWidgets.QLabel()
                                lbl4.setText(str(deepKey))
                                objs[key].append(lbl4)
                                self.gridLayout.addWidget(lbl4, i, 0)
                                lbl5 = QtWidgets.QLabel()
                                lbl5.setText(str(stocks[key][deepKey]))
                                objs[key].append(lbl5)
                                self.gridLayout.addWidget(lbl5, i, 1)
                            i += 1

                elif key == 'history':
                    button = QtWidgets.QPushButton()
                    self.setText(button, 'View History')
                    objs[key].append(button)
                    self.gridLayout.addWidget(button, i, 1)
                else:
                    lbl = QtWidgets.QLabel()
                    lbl.setText(str(stocks[key]))
                    objs[key].append(lbl)
                    self.gridLayout.addWidget(lbl, i, 1)
                i += 1
                blankLbl1 = QtWidgets.QLabel()
                self.gridLayout.addWidget(blankLbl1, i, 0)
                blankLbl2 = QtWidgets.QLabel()
                self.gridLayout.addWidget(blankLbl2, i, 1)
                i += 1

        except Exception as e:
            if parent == None:
                print('error occured in main:', e)
            else:
                print('error occured in child main:', e)



        # GUI FUNCTIONS
    def setText(self, label, text):
        try:
            _translate = QtCore.QCoreApplication.translate
            label.setText(_translate("Form", str(text)))
        except Exception as e:
            print('error in setText:', e)


def connector(data, par):
    def myFunc():
        newWindow = IndicSelectWindow(data, parent=par)
        newWindow.show()
        # print(a)
        # print(b)
        # print(c)
        # print(a[b])
        # print(a[b][c])
    return myFunc

def main(myStoinks):

    app = QtWidgets.QApplication(sys.argv)
    w = IndicSelectWindow(myStoinks)
    w.show()
    sys.exit(app.exec_())

def test1():
    stocks = yahooInterface.get_day_most_active(9)
    info = yahooInterface.grabInfo(stocks,
                                   ['live_price', 'quote_table', 'history', 'analytics'],
                                   histLength=7)
    return info

if __name__ == '__main__':
    results = test1()
    for itr10 in results:
        main(results[itr10])
        break
    # print(results)
    # main(results[0])