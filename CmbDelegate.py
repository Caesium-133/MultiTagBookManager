from PyQt5 import QtCore
from PyQt5.QtWidgets import QItemDelegate, QComboBox, QWidget
from PyQt5.QtCore import Qt


class CmbDelegate(QItemDelegate):
    def __init__(self, column, read: bool, parent=None):
        super(CmbDelegate, self).__init__(parent)
        self.column = column
        self.read = read

    def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> QWidget:
        if index.isValid() and index.column() == self.column:
            cmb = QComboBox(parent)
            #cmb.setEditable(True)
            cmb.installEventFilter(self)
            return cmb
        else:
            return super(CmbDelegate, self).createEditor(parent, option, index)

    def setEditorData(self, editor: QWidget, index: QtCore.QModelIndex) -> None:
        if index.isValid() and index.column() == self.column:
            nowstr = str(index.model().data(index, Qt.DisplayRole))
            editor.clear()
            if self.read:
                editor.addItems(["未读", "已读", "在读", "想读"])
            else:
                editor.addItems(["未完结", "已完结"])
            editor.setCurrentText(nowstr)
        else:
            super(CmbDelegate, self).setEditorData(editor, index)

    def setModelData(self, editor: QWidget, model: QtCore.QAbstractItemModel, index: QtCore.QModelIndex) -> None:
        if index.isValid() and index.column() == self.column:
            model.setData(index, editor.currentText())
        else:
            super(CmbDelegate, self).setModelData(editor, model, index)
