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

        Return row count of the pandas DataFrame
        """
        pass

    def data(self, index: QModelIndex, role=Qt.ItemDataRole):
        """Override metho from QAbstractTableModel.
        
        Retur data cell from the pandas DataFrame
        """
        pass

    def headerData(
        self, section: int, orientation: Qt.Orientation,
        role: Qt.ItemDataRole
    ) -> Any:
        """Override method from QAbstractTableModel.
        
        Return dframe index as vertical header data and columns as horizontal
        header data.
        """
        pass


def main():
    pass


if __name__ == "__main__":
    main()
