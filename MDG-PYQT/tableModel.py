import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import pandas as pd


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        # print(data,"this is data")
        # rowHeight = self.fontMetrics().height()
        # self.verticalHeader().setDefaultSectionSize(rowHeight)

    def data(self, index, role):
        # if (index.column() == yourCellIndex and role == Qt.TextAlignmentRole) :
        #     return Qt.AlignCenter
        # else :
        #     return QVariant()
        
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]
    
    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])

    def resizeEvent(self, event):
        width = event.size().width()
        self.setColumnWidth(1, width * 0.25) # 25% Width Column
        self.setColumnWidth(2, width * 0.75) # 75% Width Column