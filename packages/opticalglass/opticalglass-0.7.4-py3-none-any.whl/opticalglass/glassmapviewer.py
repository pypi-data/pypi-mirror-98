#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2018 Michael J. Hayford
""" desktop application for viewing glass catalog data

.. Created on Wed Jan  3 12:50:03 2018

.. codeauthor: Michael J. Hayford
"""
import logging
import sys

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout,
                             QVBoxLayout, QGridLayout, QSizePolicy, QGroupBox,
                             QCheckBox, QRadioButton, QTableView, QLabel)
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QMimeData
from PyQt5.QtGui import QDrag

from matplotlib.backends.backend_qt5agg \
     import (FigureCanvasQTAgg as FigureCanvas,
             NavigationToolbar2QT as NavigationToolbar)

from opticalglass.glassmap import GlassMapFigure, GlassMapDB


def init_UI(gui_parent, fig):
    main_widget = QWidget()
    layout = QHBoxLayout(main_widget)

    gm = PlotCanvas(gui_parent, fig)
    layout.addWidget(gm)

    gui_parent.addToolBar(Qt.BottomToolBarArea,
                          NavigationToolbar(gm, gui_parent))

    rightBar = QVBoxLayout()
    layout.addLayout(rightBar)

    plotPartialsBar = QHBoxLayout()
    plotTypeGroup = createPlotTypeBox(gui_parent, fig)
    plotPartialsBar.addWidget(plotTypeGroup)

    partialsGroup = createPartialsBox(gui_parent, fig)
    plotPartialsBar.addWidget(partialsGroup)
    rightBar.addLayout(plotPartialsBar)

    catalogGroup = createCatalogGroupBox(gui_parent, fig)
    rightBar.addWidget(catalogGroup)

    pick_model = PickModel(fig)
    gmt = PickTable(gui_parent, pick_model)
    rightBar.addWidget(gmt)

    return main_widget, pick_model


def createPlotTypeBox(gui_parent, fig):
    groupBox = QGroupBox("Plot Type", gui_parent)
    groupBox.setMaximumWidth(190)

    index_btn = QRadioButton("Refractive Index")
    index_btn.setChecked(True)
    index_btn.toggled.connect(lambda:
                              on_plot_type_toggled(fig, index_btn))
    partial_btn = QRadioButton("Partial Dispersion")
    partial_btn.toggled.connect(lambda:
                                on_plot_type_toggled(fig, partial_btn))
    buchdahl_btn = QRadioButton("Buchdahl Coefficients")
    buchdahl_btn.toggled.connect(lambda:
                                 on_plot_type_toggled(fig, buchdahl_btn))
    buchdahl_disp_btn = QRadioButton("Buchdahl Dispersion\nCoefficients")
    buchdahl_disp_btn.toggled.connect(
        lambda: on_plot_type_toggled(fig, buchdahl_disp_btn))

    vbox = QVBoxLayout()
    vbox.addWidget(index_btn)
    vbox.addWidget(partial_btn)
    vbox.addWidget(buchdahl_btn)
    vbox.addWidget(buchdahl_disp_btn)

    groupBox.setLayout(vbox)

    return groupBox


def createPartialsBox(gui_parent, fig):
    def on_ui_changed(fig, button):
        is_changed = False
        if button.text() == "Default range":
            if button.isChecked() is True:
                short = short_wl_default.text()
                long = long_wl_default.text()
                is_changed = True
        elif button.text() == "Blue range":
            if button.isChecked() is True:
                short = short_wl_blue.text()
                long = long_wl_blue.text()
                is_changed = True
        elif button.text() == "Red range":
            if button.isChecked() is True:
                short = short_wl_red.text()
                long = long_wl_red.text()
                is_changed = True
        if is_changed:
            fig.partials = (short, long)
            fig.refresh()

    groupBox = QGroupBox("Partial Dispersion", gui_parent)
    groupBox.setMaximumWidth(190)

    F_d_btn = QRadioButton("Default range")
    F_d_btn.setChecked(True)
    F_d_btn.toggled.connect(lambda:
                            on_ui_changed(fig, F_d_btn))
    short_wl_default = QLabel()
    short_wl_default.setText('F')

    long_wl_default = QLabel()
    long_wl_default.setText('d')

    blue_btn = QRadioButton("Blue range")
    blue_btn.toggled.connect(lambda:
                             on_ui_changed(fig, blue_btn))
    short_wl_blue = QLabel()
    short_wl_blue.setText('g')

    long_wl_blue = QLabel()
    long_wl_blue.setText('F')

    red_btn = QRadioButton("Red range")
    red_btn.toggled.connect(lambda:
                            on_ui_changed(fig, red_btn))
    short_wl_red = QLabel()
    short_wl_red.setText('d')

    long_wl_red = QLabel()
    long_wl_red.setText('C')

    layout = QGridLayout()
    groupBox.setLayout(layout)
    layout.addWidget(F_d_btn, 0, 0)
    layout.addWidget(short_wl_default, 0, 1)
    layout.addWidget(long_wl_default, 0, 2)
    layout.addWidget(blue_btn, 1, 0)
    layout.addWidget(short_wl_blue, 1, 1)
    layout.addWidget(long_wl_blue, 1, 2)
    layout.addWidget(red_btn, 2, 0)
    layout.addWidget(short_wl_red, 2, 1)
    layout.addWidget(long_wl_red, 2, 2)

    return groupBox


def on_plot_type_toggled(fig, button):
    plot_display_type = fig.plot_display_type
    if button.text() == "Refractive Index":
        if button.isChecked() is True:
            plot_display_type = "Refractive Index"
    elif button.text() == "Partial Dispersion":
        if button.isChecked() is True:
            plot_display_type = "Partial Dispersion"
    elif button.text() == "Buchdahl Coefficients":
        if button.isChecked() is True:
            plot_display_type = "Buchdahl Coefficients"
    elif button.text() == "Buchdahl Dispersion\nCoefficients":
        if button.isChecked() is True:
            plot_display_type = "Buchdahl Dispersion Coefficients"

    fig.plot_display_type = plot_display_type
    fig.refresh()


def createCatalogGroupBox(gui_parent, fig):
    groupBox = QGroupBox("Glass Catalogs", gui_parent)

    check_box_list = []
    for i, gc in enumerate(fig.glass_db.catalogs):
        catalog, cat_name = gc
        checkBox = QCheckBox(cat_name)
        checkBox.setChecked(True)
        checkBox.stateChanged.connect(create_handle_checkbox(fig, i))
        check_box_list.append(checkBox)

    vbox = QVBoxLayout()
    for cb in check_box_list:
        vbox.addWidget(cb)

    groupBox.setLayout(vbox)

    return groupBox


def create_handle_checkbox(fig, cb_number):
    def handle_checkbox(state):
        checked = state == Qt.Checked
        fig.db_display[cb_number] = checked
        fig.updateVisibility(cb_number, checked)
    return handle_checkbox


class GlassMapViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = 'Glass Map Viewer'
        self.setWindowTitle(self.title)

        self.left = 50
        self.top = 150
        self.width = 1110
        self.height = 650
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.glass_db = GlassMapDB()
        self.db_display = [True]*len(self.glass_db.catalogs)
        self.plot_display_type = "Refractive Index"
        self.fig = GlassMapFigure(self.glass_db, db_display=self.db_display,
                                  plot_display_type=self.plot_display_type,
                                  refresh_gui=self.refresh_gui,
                                  )
        self._main, self.pick_model = init_UI(self, self.fig)
        self.setCentralWidget(self._main)

        self.fig.plot()

    def refresh_gui(self, **kwargs):
        self.pick_model.fill_table(self.fig.pick_list)


_pt_header = ["Catalog", "Glass", "Nd", "Vd", "P F,d"]
_pt_format = ["{:s}", "{:s}", "{:7.5f}", "{:5.2f}", "{:6.4f}"]


class PickTable(QTableView):
    def __init__(self, gui_parent, pick_model):
        super().__init__(gui_parent)
        self.setModel(pick_model)
        self.setAlternatingRowColors(True)
        self.setMinimumWidth(285)
        self.setMaximumWidth(345)
        self.setDragEnabled(True)
        self.pickRow = 0
        for i, w in enumerate([53, 100, 63, 52, 60]):
            self.setColumnWidth(i, w)

    def mousePressEvent(self, event):
        """Initiate glass drag and drop operation from here. """
        super().mousePressEvent(event)
        if (
                event.button() == Qt.LeftButton and
                self.model().rowCount(0) > 0):
            drag = QDrag(self)
            mimeData = QMimeData()
            si = self.indexAt(event.pos())
            pick_row = si.row()
            pick = self.model().pick_table[pick_row]
            # comma separated list: glass_name,catalog_name
            mimeData.setText(pick[1] + ',' + pick[0])
            drag.setMimeData(mimeData)

            drag.exec_(Qt.CopyAction)


class PickModel(QAbstractTableModel):
    def __init__(self, fig):
        super().__init__()
        self.fig = fig
        self.num_rows = 0
        self.pick_table = []
        self.pt_header = _pt_header

    def rowCount(self, index):
        return self.num_rows

    def columnCount(self, index):
        return len(self.pt_header)

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 4:
                    self.pt_header[section] = "P %s-%s" % self.fig.partials
                return self.pt_header[section]
            elif orientation == Qt.Vertical:
                return None
        else:
            return None

    def data(self, index, role):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            r = index.row()
            c = index.column()
            return self.pick_table[r][c]
        else:
            return None

    def fill_table(self, pick_list):
        self.pickRow = 0
        pick_table = []
        for item in pick_list:
            pick_table.append([f.format(v) for f, v in zip(_pt_format, item)])
        self.pick_table = pick_table

        if self.num_rows > 0:
            self.beginRemoveRows(QModelIndex(), 0, self.num_rows-1)
            self.removeRows(0, self.num_rows)
            self.endRemoveRows()

        self.num_rows = len(pick_table)
        if self.num_rows > 0:
            self.beginInsertRows(QModelIndex(), 0, self.num_rows-1)
            self.insertRows(0, self.num_rows)
            self.endInsertRows()


class PlotCanvas(FigureCanvas):
    def __init__(self, gui_parent, fig):
        super().__init__(fig)
        self.setParent(gui_parent)
        logging.debug("Canvas dpi: {}".format(fig.dpi))

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        fig.plot()


def main():
    logging.basicConfig(filename='opticalglass.log',
                        filemode='w',
                        format='%(asctime)s: %(message)s',
                        level=logging.DEBUG)
    logging.info("opticalglass started")
    qtapp = QApplication(sys.argv)
    qtwnd = GlassMapViewer()
    qtwnd.show()
    return qtapp.exec_()


if __name__ == '__main__':
    sys.exit(main())
