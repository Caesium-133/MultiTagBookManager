import sys
from mainWindow import mainWindow
from addDialog import addDialog


from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = mainWindow()
    mainWindow.show()
    ad=addDialog(query=mainWindow.query,parent=mainWindow)
    mainWindow.action_add.triggered.connect(ad.show)
    ad.addedNew.connect(mainWindow.onAddAddedNew)
    sys.exit(app.exec_())