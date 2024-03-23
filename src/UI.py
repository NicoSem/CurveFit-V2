import sys
import matplotlib
import re
from CurveFit import Fitter

matplotlib.use('Qt5Agg')

from PySide6.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QPushButton
from PySide6 import QtCore

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes1 = fig.add_subplot(111)
        
        super(MplCanvas, self).__init__(fig)


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Curve Fit V2")
        
        self.plotSection = MplCanvas(self, width=5, height=4, dpi=100)
        self.xEntries = []
        self.yEntries = []
        self.firstFit = True

        self.fitter = Fitter()

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
        deleteButton = QPushButton("Delete")
        deleteButton.clicked.connect(self.buttonClick)
        fitCurveButton = QPushButton("Fit")
        fitCurveButton.clicked.connect(self.buttonClick)
        clearButton = QPushButton("Clear")
        clearButton.clicked.connect(self.buttonClick)
        ValueEntryLayout.addWidget(xLabel)
        ValueEntryLayout.addWidget(self.xEntry)
        ValueEntryLayout.addWidget(yLabel)
        ValueEntryLayout.addWidget(self.yEntry)
        ValueEntryLayout.addWidget(valueEnterButton)
        ValueEntryLayout.addWidget(deleteButton)
        ValueEntryLayout.addWidget(fitCurveButton)
        ValueEntryLayout.addWidget(clearButton)

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
        
    def addEntry(self, x, y):
            self.fitter.addPoint(x, y)
            if len(self.xEntries) == 0:
                self.xEntries.append(x)
                self.yEntries.append(y)
            else:
                for i in range(0, len(self.xEntries)):
                    if x < self.xEntries[i]:
                        self.xEntries.insert(i, x)
                        self.yEntries.insert(i, y)
                        break
                    if i == len(self.xEntries) - 1:
                        self.xEntries.append(x)
                        self.yEntries.append(y)

    def buttonClick(self):

        if self.sender().text() == "Enter":
            if checkEntry(self.xEntry.text()) and checkEntry(self.yEntry.text()):

                self.numRows += 1
                self.valueTable.setRowCount(self.numRows)

                item = QTableWidgetItem()
                item.setData(QtCore.Qt.DisplayRole, float(self.xEntry.text()))
                self.valueTable.setItem(self.numRows - 1, 0, item)
                x = (float(self.xEntry.text()))

                item = QTableWidgetItem()
                item.setData(QtCore.Qt.DisplayRole, float(self.yEntry.text()))
                self.valueTable.setItem(self.numRows - 1, 1, item)
                y = (float(self.yEntry.text()))
                self.addEntry(x, y)

                self.valueTable.sortItems(0)
                
                self.plotSection.axes1.cla()
                self.plotSection.axes1.scatter(self.xEntries, self.yEntries)
                self.plotSection.draw()

        elif self.sender().text() == "Delete":
            self.xEntries.pop(self.valueTable.currentRow())
            self.yEntries.pop(self.valueTable.currentRow())
            self.fitter.points.pop(self.valueTable.currentRow())
            self.valueTable.removeRow(self.valueTable.currentRow())
            self.numRows -= 1
            self.valueTable.setRowCount(self.numRows)

        elif self.sender().text() == "Fit":
            self.result = self.fitter.fit()
            self.plotSection.axes1.cla()
            self.plotSection.axes1.scatter(self.xEntries, self.yEntries)
            self.plotSection.axes1.plot(self.xEntries, self.result.mapToY(self.xEntries), color='red')
            self.plotSection.draw()
            print("Done ", self.result)

        elif self.sender().text() == "Clear":
            self.xEntries.clear()
            self.yEntries.clear()
            self.fitter.points.clear()
            self.valueTable.clear()
            self.numRows = 0
            self.valueTable.setRowCount(self.numRows)
            self.valueTable.setRowCount(0)
            self.plotSection.axes1.cla()
            self.plotSection.draw()

            
            

def checkEntry(a):
    try:
        float(a)
        return True
    except ValueError:
        return False


app = QApplication(sys.argv)
w = MainWindow()
app.exec_()