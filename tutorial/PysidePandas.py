#!/usr/bin/env python3
import sys
import pandas as pd
from PySide6.QtWidgets import QTableView, QApplication
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex

from typing import Any


class PandasModel(QAbstractTableModel):
    """A model to interface a Qt view with pandas dataframe."""

    def __init__(self, dframe: pd.DataFrame, parent=None):
        super(PandasModel, self).__init__(parent)
        self._dframe = dframe

    def rowCount(self, parent=QModelIndex()) -> int:
        """Override method from QAbstractTableModel.
        
        Return row count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._dframe)
        return 0

    def columnCount(self, parent=QModelIndex()) -> int:
        """Override method from QAbstractTableModel.

        Return column count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._dframe.columns)
        return 0

    def data(self, index: QModelIndex, role=Qt.ItemDataRole):
        """Override metho from QAbstractTableModel.
        
        Retur data cell from the pandas DataFrame
        """
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            return str(self._dframe.iloc[index.row(), index.column()])

    def headerData(
        self, section: int, orientation: Qt.Orientation,
        role: Qt.ItemDataRole
    ) -> Any:
        """Override method from QAbstractTableModel.
        
        Return dframe index as vertical header data and columns as horizontal
        header data.
        """
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._dframe.columns[section])

            if orientation == Qt.Vertical:
                return str(self._dframe.index[section])

        return None


def main():
    import os.path as path
    # import os
    cdir = path.dirname(path.abspath(__file__))
    datadir = path.split(cdir)[0]
    fname = path.join(datadir, "iris.csv")

    app = QApplication()
    

    df = pd.read_csv(fname)

    view = QTableView()
    view.resize(800, 500)
    view.horizontalHeader().setStretchLastSection(True)
    view.setAlternatingRowColors(True)
    view.setSelectionBehavior(QTableView.SelectRows)

    model = PandasModel(df)
    view.setModel(model)
    view.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
