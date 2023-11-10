import sys
import matplotlib
import re

matplotlib.use('Qt5Agg')

from PySide6.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QPushButton
from PySide6 import QtCore

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Curve Fit V2")
        
        self.plotSection = MplCanvas(self, width=5, height=4, dpi=100)
        self.xEntries = []
        self.yEntries = []


        self.valueTable = QTableWidget()
        self.valueTable.setColumnCount(2)
        self.valueTable.setHorizontalHeaderLabels(['x', 'y'])
        self.valueTable.verticalHeader().hide()
        self.numRows = 0


        layout = QHBoxLayout()


        valueEntrySection = QWidget()
        ValueEntryLayout = QHBoxLayout()
        xLabel = QLabel("x")
        self.xEntry = QLineEdit()
        yLabel = QLabel("y")
        self.yEntry = QLineEdit()
        valueEnterButton = QPushButton("Enter")
        valueEnterButton.clicked.connect(self.buttonClick)
        ValueEntryLayout.addWidget(xLabel)
        ValueEntryLayout.addWidget(self.xEntry)
        ValueEntryLayout.addWidget(yLabel)
        ValueEntryLayout.addWidget(self.yEntry)
        ValueEntryLayout.addWidget(valueEnterButton)
        valueEntrySection.setLayout(ValueEntryLayout)


        valuesSection = QWidget()
        valuesLayout = QVBoxLayout()
        valuesLayout.addWidget(valueEntrySection)
        valuesLayout.addWidget(self.valueTable)
        valuesSection.setLayout(valuesLayout)


        layout.addWidget(self.plotSection)
        layout.addWidget(valuesSection)


        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


        self.show()

    def buttonClick(self):

        def updateEntryPlot():
            print("updating plot")
            self.plotSection.axes.cla()
            self.plotSection.axes.scatter(self.xEntries, self.yEntries)
            self.plotSection.draw()


        if self.sender().text() == "Enter":
            if checkEntry(self.xEntry.text()) and checkEntry(self.yEntry.text()):

                self.numRows += 1
                self.valueTable.setRowCount(self.numRows)

                item = QTableWidgetItem()
                item.setData(QtCore.Qt.DisplayRole, float(self.xEntry.text()))
                self.valueTable.setItem(self.numRows - 1, 0, item)
                self.xEntries.append(float(self.xEntry.text()))

                item = QTableWidgetItem()
                item.setData(QtCore.Qt.DisplayRole, float(self.yEntry.text()))
                self.valueTable.setItem(self.numRows - 1, 1, item)
                self.yEntries.append(float(self.yEntry.text()))
                
                self.valueTable.sortItems(0)
                updateEntryPlot()
            

def checkEntry(a):
    try:
        float(a)
        return True
    except ValueError:
        return False


app = QApplication(sys.argv)
w = MainWindow()
app.exec_()