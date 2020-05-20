
from PyQt5 import QtCore, QtGui, QtWidgets

import stockSelecPopUp


class Ui_MainWindow(QtWidgets.QDialog):
    def __init__(self, cStocks, id, parent=None):
        self.id = id
        self.openStocks = dict()
        # MainWindow.setObjectName("MainWindow")
        # MainWindow.resize(532, 299)
        # self.centralwidget = QtWidgets.QWidget(MainWindow)
        # self.centralwidget.setObjectName("centralwidget")
        super().__init__(parent=parent)
        self.setWindowTitle(str(id) + ' Overview')
        self.resize(530, 280)
        self.layout = QtWidgets.QHBoxLayout(self)
        self.scrollArea = QtWidgets.QScrollArea(self)
        # self.scrollArea.setGeometry(QtCore.QRect(0, 0, 531, 271))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        # self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 529, 269))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.layout.addWidget(self.scrollArea)


        self.pushButton_2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_2.setGeometry(QtCore.QRect(150, 40, 110, 19))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_11 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_11.setGeometry(QtCore.QRect(290, 210, 110, 20))
        self.pushButton_11.setObjectName("pushButton_11")
        self.pushButton_10 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_10.setGeometry(QtCore.QRect(140, 210, 110, 20))
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton_7 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_7.setGeometry(QtCore.QRect(80, 170, 110, 20))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_8.setGeometry(QtCore.QRect(210, 170, 120, 20))
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_9.setGeometry(QtCore.QRect(350, 170, 110, 20))
        self.pushButton_9.setObjectName("pushButton_9")
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_2.setGeometry(QtCore.QRect(0, 130, 530, 16))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton.setGeometry(QtCore.QRect(20, 40, 111, 19))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_6 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_6.setGeometry(QtCore.QRect(350, 80, 100, 19))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_3 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_3.setGeometry(QtCore.QRect(280, 40, 110, 19))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_4.setGeometry(QtCore.QRect(410, 40, 100, 19))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_5.setGeometry(QtCore.QRect(90, 80, 100, 19))
        self.pushButton_5.setObjectName("pushButton_5")
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label.setGeometry(QtCore.QRect(0, 10, 530, 20))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_4.setGeometry(QtCore.QRect(20, 10, 491, 20))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_5.setGeometry(QtCore.QRect(20, 130, 491, 20))
        self.label_5.setObjectName("label_5")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # Link Buttons
        self.pushButton_7.clicked.connect(self.current_stock_details(cStocks))

        self.retranslateUi()


    def retranslateUi(self):
        self.pushButton_2.setText("Deactivate Bot")
        self.pushButton_11.setText("Original Balance")
        self.pushButton_10.setText("Current Balance")
        self.pushButton_7.setText("Current Stock Details")
        self.pushButton_8.setText("Past Transactions")
        self.pushButton_9.setText("Original Stock Details")
        self.label_2.setText("Information")
        self.pushButton.setText("Activate Bot")
        self.pushButton_6.setText("Remove Stocks")
        self.pushButton_3.setText("Duplicate Bot")
        self.pushButton_4.setText("Delete Bot")
        self.pushButton_5.setText("Add Stocks")
        self.label.setText("   Functionality")
        self.label_4.setText("_________________________________________________________________________________")
        self.label_5.setText("_________________________________________________________________________________")



    def current_stock_details(self, data):
        def inner():
            try:
                newWindow = stockSelecPopUp.IndicSelectWindow(data, self.id, parent=self)
                newWindow.show()
                self.openStocks[self.id] = newWindow
            except Exception as e:
                print(e)
        return inner

    def updateStocks(self, stocks):
        try:
            self.openStocks[id].updateStocks(stocks, self.id)
        except KeyError:
            pass


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())
