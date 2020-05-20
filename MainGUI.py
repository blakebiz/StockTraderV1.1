import sys
import random
from PyQt5 import QtWidgets
from PyQt5 import QtCore

import BotInfoGUI
import stockPopUpGUI

class Test():
    def __init__(self, data, storage):
        self.id = 'bot #' + str(random.randint(0, 10000))
        while self.id in storage.nums:
            self.id = 'bot #' + str(random.randint(0, 10000))
        storage.nums.append(self.id)
        self.stockInfo = data


class Storage():
    def __init__(self):
        self.nums = []

class IndicSelectWindow(QtWidgets.QDialog):
    def __init__(self, stocks, parent=None):
        try:
            super().__init__(parent=parent)
            self.setWindowTitle('Overview of Bots')
            self.resize(500, 400)
            self.layout = QtWidgets.QHBoxLayout(self)
            self.scrollArea = QtWidgets.QScrollArea(self)
            self.scrollArea.setWidgetResizable(True)
            self.scrollAreaWidgetContents = QtWidgets.QWidget()
            self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
            self.scrollArea.setWidget(self.scrollAreaWidgetContents)
            self.layout.addWidget(self.scrollArea)
            self.openBots = dict()
            print(1)
            pushButtons = dict()
            for i in range(len(stocks)):
                for j in range(len(stocks[i])):
                    if i in pushButtons:
                        pushButtons[i][j] = button = QtWidgets.QPushButton()
                        self.setText(button, stocks[i][j].id)
                        button.clicked.connect(self.openBot(stocks[i][j].stockInfo, stocks[i][j].id))
                        self.gridLayout.addWidget(button, i, j)
                    else:
                        button = QtWidgets.QPushButton()
                        self.setText(button, stocks[i][j].id)
                        button.clicked.connect(self.openBot(stocks[i][j].stockInfo, stocks[i][j].id))
                        pushButtons[i] = {j: button}
                        self.gridLayout.addWidget(button, i, j)
            thread = self.thread()
            thread.start()
        except Exception as e:
            print('error in MainGUI:', e)
    def openBot(self, data, id):
        def inner():
            try:
                newWindow = BotInfoGUI.Ui_MainWindow(data, id, parent=self)
                newWindow.show()
                self.openBots[id] = newWindow
            except Exception as e:
                print(e)
        return inner

    def updateBot(self, stocks, id):
        try:
            self.openBots[id].updateStocks(stocks)
        except KeyError:
            pass


    # GUI FUNCTIONS
    def setText(self, label, text):
        try:
            _translate = QtCore.QCoreApplication.translate
            label.setText(_translate("Form", str(text)))
        except Exception as e:
            print('error in setText:', e)

def formatBots(bots):
    from copy import deepcopy
    sCopy = sorted(deepcopy(bots), key=lambda bot: bot.id, reverse=True)
    stoinks = []
    n = 0
    while len(sCopy) > 0:
        i = 0
        while i < 5:
            if len(sCopy) <= 0:
                break
            elif i == 0:
                stoinks.append([sCopy.pop()])
            else:
                stoinks[n].append(sCopy.pop())
            i += 1
        n += 1
    return stoinks

def get_test_info():
    myBots = []
    storage = Storage()
    bots = stockPopUpGUI.test1()
    for _ in bots:
        myBots.append(Test(bots, storage))
    return formatBots(myBots)

def main(testing=True):
    if testing:
        data = get_test_info()
    else:
        import botStorage
        data = botStorage.Storage()
    app = QtWidgets.QApplication(sys.argv)
    w = IndicSelectWindow(data)
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

