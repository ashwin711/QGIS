# -*- coding: utf-8 -*-

"""
***************************************************************************
    MultipleExternalInputDialog.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
                           (C) 2013 by CS Systemes d'information (CS SI)
    Email                : volayaf at gmail dot com
                           otb at c-s dot fr (CS SI)
    Contributors         : Victor Olaya  - basis from MultipleInputDialog
                           Alexia Mondot (CS SI) - new parameter
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""
from builtins import range

__author__ = 'Victor Olaya'
__date__ = 'August 2012'
__copyright__ = '(C) 2012, Victor Olaya'
# This will get replaced with a git SHA1 when you do a git archive
__revision__ = '$Format:%H$'

import os

from qgis.core import QgsSettings
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog, QAbstractItemView, QPushButton, QDialogButtonBox, QFileDialog
from qgis.PyQt.QtGui import QStandardItemModel, QStandardItem

pluginPath = os.path.split(os.path.dirname(__file__))[0]
WIDGET, BASE = uic.loadUiType(
    os.path.join(pluginPath, 'ui', 'DlgMultipleSelection.ui'))


class MultipleFileInputDialog(BASE, WIDGET):

    def __init__(self, options):
        super(MultipleFileInputDialog, self).__init__(None)
        self.setupUi(self)

        self.lstLayers.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.selectedoptions = options

        # Additional buttons
        self.btnAdd = QPushButton(self.tr('Add file'))
        self.buttonBox.addButton(self.btnAdd,
                                 QDialogButtonBox.ActionRole)
        self.btnRemove = QPushButton(self.tr('Remove file(s)'))
        self.buttonBox.addButton(self.btnRemove,
                                 QDialogButtonBox.ActionRole)
        self.btnRemoveAll = QPushButton(self.tr('Remove all'))
        self.buttonBox.addButton(self.btnRemoveAll,
                                 QDialogButtonBox.ActionRole)

        self.btnAdd.clicked.connect(self.addFile)
        self.btnRemove.clicked.connect(lambda: self.removeRows())
        self.btnRemoveAll.clicked.connect(lambda: self.removeRows(True))

        self.populateList()

    def populateList(self):
        model = QStandardItemModel()
        for option in self.selectedoptions:
            item = QStandardItem(option)
            model.appendRow(item)

        self.lstLayers.setModel(model)

    def accept(self):
        self.selectedoptions = []
        model = self.lstLayers.model()
        for i in range(model.rowCount()):
            item = model.item(i)
            self.selectedoptions.append(item.text())
        QDialog.accept(self)

    def reject(self):
        QDialog.reject(self)

    def addFile(self):
        settings = QgsSettings()
        if settings.contains('/Processing/LastInputPath'):
            path = settings.value('/Processing/LastInputPath')
        else:
            path = ''

        files, selected_filter = QFileDialog.getOpenFileNames(self,
                                                              self.tr('Select file(s)'), path, self.tr('All files (*.*)'))

        if len(files) == 0:
            return

        model = self.lstLayers.model()
        for filePath in files:
            item = QStandardItem(filePath)
            model.appendRow(item)

        settings.setValue('/Processing/LastInputPath',
                          os.path.dirname(files[0]))

    def removeRows(self, removeAll=False):
        if removeAll:
            self.lstLayers.model().clear()
        else:
            self.lstLayers.setUpdatesEnabled(False)
            indexes = sorted(self.lstLayers.selectionModel().selectedIndexes())
            for i in reversed(indexes):
                self.lstLayers.model().removeRow(i.row())
            self.lstLayers.setUpdatesEnabled(True)
