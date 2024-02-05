from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QCompleter
from Ui_addDialog import Ui_Dialog
from PyQt5.QtCore import pyqtSignal, QStringListModel,Qt
import os
import time

class addDialog(QMainWindow, Ui_Dialog):
    addedNew=pyqtSignal()
    def __init__(self,query, parent=None):
        super(addDialog,self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('添加图书信息')

        self.location=''
        self.tagList=[]
        self.addedTagSet=set()
        self.query=query

        self.getAttrs()

        self.completer_a_tag_edit = QCompleter()
        self.completer_a_tag_edit.setModel(QStringListModel(self.tagList))
        self.completer_a_tag_edit.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer_a_tag_edit.setFilterMode(Qt.MatchRecursive)
        self.lineEdit_a_tag.setCompleter(self.completer_a_tag_edit)
        self.stringListModel_tag = QStringListModel()
        self.listView_a_tags.setModel(self.stringListModel_tag)
        self.comboBox_a_status.addItems(["未完结","已完结"])
        self.comboBox_a_read.addItems(["未读", "已读", "在读", "想读"])
        self.spinBox_a_score.setMaximum(5)
        self.spinBox_a_score.setMinimum(0)

        self.pushButton_a_addTag.clicked.connect(self.onAddAddTagBtnClicked)
        self.pushButton_a_rmTag.clicked.connect(self.onAddRmTagBtnClicked)
        self.pushButton_a_clearTag.clicked.connect(self.onAddClearTagClicked)
        self.pushButton_a_confirm.clicked.connect(self.onAddConfirmBtnClicked)
        self.pushButton_a_clear.clicked.connect(self.clear)
        self.pushButton_a_openLocal.clicked.connect(self.onAddOpenLocationBtnClicked)

    def getAttrs(self):
        if self.query.exec("select tag_name from tags"):
            while self.query.next():
                self.tagList.append(self.query.value(0))

    def onAddOpenLocationBtnClicked(self):
        if os.path.isfile(self.location):
            loc=os.path.split(self.location)[0]
        elif os.path.isdir(self.location):
            loc=self.location
        else:
            loc = "/"
        fileName, _ = QFileDialog.getOpenFileName(self, "选择图书", loc)
        self.lineEdit_a_fileLocation.setText(fileName)

    def onAddAddTagBtnClicked(self):
        inTag=self.lineEdit_a_tag.text()
        if inTag.strip()=='':
            return
        self.addedTagSet.add(inTag)
        self.stringListModel_tag.setStringList(self.addedTagSet)
        self.lineEdit_a_tag.clear()

    def onAddRmTagBtnClicked(self):
        row=self.listView_a_tags.currentIndex().row()
        if row==-1:
            return
        tag2rm=self.stringListModel_tag.itemData(self.stringListModel_tag.index(row))[Qt.DisplayRole]
        self.addedTagSet.remove(tag2rm)
        self.stringListModel_tag.setStringList(self.addedTagSet)

    def onAddClearTagClicked(self):
        self.addedTagSet.clear()
        self.stringListModel_tag.setStringList(self.addedTagSet)

    def onAddConfirmBtnClicked(self):
        location=self.lineEdit_a_fileLocation.text()
        bookName=self.lineEdit_add_book_name.text()
        author=self.lineEdit_add_author.text()
        score=self.spinBox_a_score.value()
        status=self.comboBox_a_status.currentText()
        readStatus=self.comboBox_a_read.currentText()
        website=self.lineEdit_add_website.text()
        updatedChapter=self.lineEdit_a_updated_chapter.text()
        lastUpdateDate=self.lineEdit_a_last_update_date.text()
        review=self.plainTextEdit_a_review.toPlainText()
        bookSql=f"insert into books( url, name, author, rating, status,read_status,updated_chapter,last_update_date, website, comment) values ('{location}','{bookName}','{author}',{score},'{status}','{readStatus}','{updatedChapter}','{lastUpdateDate}','{website}','{review}')"
        try:
            self.query.exec(bookSql)
            self.query.exec("select LAST_INSERT_ROWID() from books")
            self.query.first()
            bookId=self.query.value(0)
            for tag in self.addedTagSet:
                self.query.exec(f"select tag_id from tags where tag_name='{tag}'")
                if self.query.first():
                    tagId=self.query.value(0)
                else:
                    self.query.exec(f"insert into tags(tag_name) values ('{tag}')")
                    self.query.exec("select LAST_INSERT_ROWID() from tags")
                    self.query.first()
                    tagId=self.query.value(0)
                self.query.exec(f"insert into book_tag(book_id, tag_id) VALUES ({bookId},{tagId})")
        except:
            QMessageBox.critical(self,"错误",f"数据库操作失败：{self.query.lastError().text()};\n 错误的SQL：{self.query.lastQuery()}",QMessageBox.Ok)
            return
        self.clear()
        self.label_a_info.setText(time.asctime()+f": 已添加{bookName}")
        self.addedNew.emit()

    def clear(self):
        self.lineEdit_a_fileLocation.clear()
        self.lineEdit_add_book_name.clear()
        self.lineEdit_add_author.clear()
        self.lineEdit_add_website.clear()
        self.lineEdit_a_updated_chapter.clear()
        self.lineEdit_a_last_update_date.clear()
        self.plainTextEdit_a_review.clear()


