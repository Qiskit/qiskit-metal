# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# Zlatko Minev

import numpy as np
from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide2.QtGui import QBrush, QColor, QFont, QIcon, QPixmap
from PySide2.QtWidgets import QTableView

from ...utility._handle_qt_messages import slot_catch_error
from ...utility._toolbox_qt import blend_colors
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .table_view_all_components import QTableView_AllComponents


class QTableModel_AllComponents(QAbstractTableModel):
    """
    Design compoentns Table model that shows the names of the compoentns and
    their class names etc.

    This class extends the `QAbstractTableModel` class.

    MVC class
    See https://doc.qt.io/qt-5/qabstracttablemodel.html

    Can be accessed with
        t = gui.ui.tableComponents
        model = t.model()
        index = model.index(1,0)
        model.data(index)
    """
    __timer_interval = 500  # ms

    def __init__(self,
                 gui,
                 logger,
                 parent=None,
                 tableView: 'QTableView_AllComponents' = None):
        """
        Args:
            gui (MetalGUI): the GUI (Default: None)
            logger (logger): the logger
            parent (QWidget): Parent widget (Default: None).
            tableView (QTableView_AllComponents): the table view (Default: None).
        """
        super().__init__(parent=parent)
        self.logger = logger
        self.gui = gui
        self._tableView = tableView  # the view used to preview this model, used to refresh
        self.columns = [
            'Name', 'QComponent class', 'QComponent module', 'Build status',
            'id'
        ]
        self._row_count = -1

        self._create_timer()

    @property
    def design(self):
        """Retrusn the design"""
        return self.gui.design

    def _create_timer(self):
        """
        Refresh the model number of rows, etc. there must be a smarter way?
        """
        self._timer = QtCore.QTimer(self)
        self._timer.start(self.__timer_interval)
        self._timer.timeout.connect(self.refresh_auto)

    def refresh(self):
        """Force refresh.   Completly rebuild the model."""
        self.modelReset.emit()

    def refresh_auto(self):
        """
        Update row count etc.
        """
        # We could not do if the widget is hidden - TODO: speed performace?

        # TODO: This should probably just be on a global timer for all changes detect
        # and then update all accordingly
        new_count = self.rowCount()

        # if the number of rows have changed
        if self._row_count != new_count:
            #self.logger.info('Number of components changed')

            # When a model is reset it should be considered that all
            # information previously retrieved from it is invalid.
            # This includes but is not limited to the rowCount() and
            # columnCount(), flags(), data retrieved through data(), and roleNames().
            # This will loose the current selection.
            # TODO: This seems overkill to just change the total number of rows?
            self.modelReset.emit()

            # for some reason the horozontal header is hidden even if i call this in init
            self._tableView.horizontalHeader().show()

            self._row_count = new_count
            self.update_view()

    def update_view(self):
        """Updates the view"""
        if self._tableView:
            self._tableView.resizeColumnsToContents()

    def rowCount(self, parent: QModelIndex = None):
        """Returns the number of rows

        Args:
            parent (QModelIndex): Unused (Default: None).

        Returns:
            int: the number of rows
        """
        if self.design:  # should we jsut enforce this
            num = int(len(self.design.qlibrary))
            if num == 0:
                self._tableView.show_placeholder_text()
            else:
                self._tableView.hide_placeholder_text()
            return num
        else:
            self._tableView.show_placeholder_text()
            return 0

    def columnCount(self, parent: QModelIndex = None):
        """Returns the number of columns

        Args:
            parent (QModelIndex): Unused (Default: None).

        Returns:
            int: the number of columns
        """
        return len(self.columns)

    def headerData(self,
                   section,
                   orientation: Qt.Orientation,
                   role=Qt.DisplayRole):
        """ Set the headers to be displayed.

        Args:
            section (int): section number
            orientation (Qt orientation): section orientation
            role (Qt display role): display role (Default: DisplayRole)

        Returns:
            str: the header data, or None if not found
        """

        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section < len(self.columns):
                    # print(self.columns[section])
                    return self.columns[section]

        elif role == Qt.FontRole:
            if section == 0:
                font = QFont()
                font.setBold(True)
                return font

    def flags(self, index):
        """ Set the item flags at the given index. Seems like we're
        implementing this function just to see how it's done, as we
        manually adjust each tableView to have NoEditTriggers.

        Args:
            index (QModelIndex): the index

        Returns:
            Qt flags: Flags from Qt
        """
        # https://doc.qt.io/qt-5/qt.html#ItemFlag-enum

        if not index.isValid():
            return Qt.ItemIsEnabled

        return Qt.ItemFlags(
            QAbstractTableModel.flags(self, index) |
            Qt.ItemIsSelectable)  # | Qt.ToolTip)  # ItemIsEditable

    # @slot_catch_error()
    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        """ Depending on the index and role given, return data. If not
        returning data, return None (PySide equivalent of QT's
        "invalid QVariant").

        Returns:
            str: data
        """

        if not index.isValid() or not self.design:
            return

        component_name = list(self.design.qlibrary.keys())[index.row()]

        if role == Qt.DisplayRole:

            if index.column() == 0:
                return str(component_name)
            elif index.column() == 1:
                return str(
                    self.design.qlibrary[component_name].__class__.__name__)
            elif index.column() == 2:
                return str(
                    self.design.qlibrary[component_name].__class__.__module__)
            elif index.column() == 3:
                return str(self.design.qlibrary[component_name].status)
            elif index.column() == 4:
                return str(self.design.qlibrary[component_name].id)

        # The font used for items rendered with the default delegate. (QFont)
        elif role == Qt.FontRole:
            if index.column() == 0:
                font = QFont()
                font.setBold(True)
                return font

        elif role == Qt.BackgroundRole:

            component = self.design.qlibrary[component_name]
            if component.status != 'good':  # Did the component fail the build
                #    and index.column()==0:
                if not self._tableView:
                    return QBrush(QColor('#FF0000'))
                table = self._tableView
                color = table.palette().color(table.backgroundRole())
                color = blend_colors(color, QColor('#FF0000'), r=0.6)
                return QBrush(color)

        elif role == Qt.DecorationRole:

            if index.column() == 0:
                component = self.design.qlibrary[component_name]
                if component.status != 'good':  # Did the component fail the build
                    return QIcon(":/basic/warning")

        elif role == Qt.ToolTipRole or role == Qt.StatusTipRole:
            component = self.design.qlibrary[component_name]
            text = f"""Component name= "{component.name}" instance of class "{component.__class__.__name__}" from module "{component.__class__.__module__}" """
            return text
