from PyQt5 import QtWidgets
from PyQt5 import QtCore
import stockPopUpGUI



class IndicSelectWindow(QtWidgets.QDialog):
    def __init__(self, stoinks, id, parent=None):
        try:
            super(IndicSelectWindow, self).__init__(parent=parent)
            self.setWindowTitle(str(id) + ' Stock Info')
            self.resize(500, 400)
            self.layout = QtWidgets.QHBoxLayout(self)
            self.scrollArea = QtWidgets.QScrollArea(self)
            self.scrollArea.setWidgetResizable(True)
            self.scrollAreaWidgetContents = QtWidgets.QWidget()
            self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
            self.scrollArea.setWidget(self.scrollAreaWidgetContents)
            self.layout.addWidget(self.scrollArea)
            pushButtons = []
            n = 0
            x = 0
            for stock in stoinks:
                button = QtWidgets.QPushButton()
                self.setText(button, stock)
                button.clicked.connect(self.connector(stoinks[stock], stock))
                if n == 0:
                    pushButtons.append([button])
                else:
                    pushButtons[x].append(button)
                self.gridLayout.addWidget(button, x, n)
                n += 1
                if n == 5:
                    n = 0
                    x += 1
        except Exception as e:
            print('error in stockSelecPopUp init:', e)
        # for i in range(len(stocks)):
        #     for j in range(len(stocks[i])):
        #         if i in pushButtons:
        #             pushButtons[i][j] = button = QtWidgets.QPushButton()
        #             self.setText(button, stocks[i][j].id)
        #             button.clicked.connect(self.openBot(stocks[i][j]))
        #             self.gridLayout.addWidget(button, i, j)
        #         else:
        #             button = QtWidgets.QPushButton()
        #             self.setText(button, stocks[i][j].id)
        #             button.clicked.connect(self.openBot(stocks[i][j].data))
        #             pushButtons[i] = {j: button}
        #             self.gridLayout.addWidget(button, i, j)



    def formatStocks(self, stocks):
        from copy import deepcopy
        sCopy = sorted(deepcopy(stocks))
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

    def connector(self, data, stock):
        def inner():
            newWindow = stockPopUpGUI.IndicSelectWindow(data, stock, parent=self)
            newWindow.show()
        return inner

    # GUI FUNCTIONS
    def setText(self, label, text):
        try:
            _translate = QtCore.QCoreApplication.translate
            label.setText(_translate("Form", str(text)))
        except Exception as e:
            print('error in setText:', e)