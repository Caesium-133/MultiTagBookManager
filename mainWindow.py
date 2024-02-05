from Ui_mainWindow import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QCompleter
from PyQt5.QtCore import Qt, QStringListModel, QUrl
from PyQt5 import QtSql
from PyQt5.QtSql import QSqlQuery, QSqlTableModel, QSqlRelationalTableModel, QSqlRelation, QSqlRelationalDelegate
from PyQt5.QtGui import QDesktopServices
import re
import os
import math
from Filter import Filter
import subprocess
from win32com.shell import shell, shellcon
import pathlib
import sqlite3
import sys

bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
path_to_sql = os.path.abspath(os.path.join(bundle_dir, 'bm.sql'))


class mainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("电子书管理")

        self.dbFile = "./data/books.db"
        self.db = None
        self.bookAttrs = ['图书id', '地址', '书名', '作者', '评分', '状态','阅读状态', '已更章节数', '上次更新日期', '来源', '评论']
        self.colList = []
        self.bookTagAttrs = ['book_id', 'tag_id']
        self.tagAttrs = ['tag_id', 'tag_name']
        self.tagList = []
        self.filterTagList = []
        self.currentBookId = None
        self.currentTagRow = None
        self.currentPage = 0
        self.totalPage = 0
        self.cntPerPage = 18

        self.db_connect()
        self.sqlTableModel = QSqlTableModel()
        self.sqlRelaTableModel = QSqlRelationalTableModel()
        self.query = QSqlQuery()
        self.tableBasicSql = 'SELECT book_id, url, name, author, rating, status,read_status,updated_chapter,last_update_date, website, comment FROM books '
        self.filters = Filter(self.query)
        self.tableSql = self.tableBasicSql
        self.tableSortField = 'book_id'
        self.tableSortDirect = "desc"

        self.getAttrs()
        self.selectAllBooks()

        # self.spinBox_m_po_cnt_per_page.setValue(self.cntPerPage)
        # self.spinBox_m_po_cnt_per_page.setMinimum(1)
        self.spinBox_m_po_jump_page.setMinimum(1)
        self.comboBox_m_sort_field.addItems(self.bookAttrs)
        self.comboBox_n_sort_direct.addItems(["升序", "降序"])
        self.completer_m_to_edit = QCompleter()
        self.completer_m_to_edit.setModel(QStringListModel(self.tagList))
        self.completer_m_to_edit.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer_m_to_edit.setFilterMode(Qt.MatchRecursive)
        self.lineEdit_m_to_new_tag.setCompleter(self.completer_m_to_edit)
        self.comboBox_m_f_status.addItems(["全部", "未完结", "已完结"])
        self.comboBox_m_f_read.addItems(["全部","未读","已读","在读","想读"])
        self.spinBox_m_f_score_from.setValue(0)
        self.spinBox_m_f_score_to.setValue(5)
        self.comboBox_m_f_tag.addItems(self.tagList)
        self.stringListModelTagFilter = QStringListModel()
        self.listView_m_f_tags.setModel(self.stringListModelTagFilter)

        self.pushButton_m_search.clicked.connect(self.onMainSearchBtnClicked)
        self.tableView_m_item_list.clicked.connect(
            lambda: self.onMainItemTableViewClicked(self.tableView_m_item_list.currentIndex().row()))
        self.pushButton_m_opt_confirm_update.clicked.connect(self.onMainOptConfirmBtnClicked)
        self.pushButton_m_opt_cancel_update.clicked.connect(self.onMainOptCancelBtnClicked)
        self.pushButton_m_opt_open_location.clicked.connect(self.onMainOpenDirBtnClicked)
        self.pushButton_m_opt_open_file.clicked.connect(self.onMainOpenFileBtnClicked)
        self.pushButton_m_opt_delete_item.clicked.connect(lambda: self.onMainDelRowBtnClicked(ask=True, rowCheck=True))
        self.pushButton_m_opt_delete_file.clicked.connect(self.onMainDelFileBtnClicked)
        self.pushButton_m_po_previous_page.clicked.connect(self.onMainPrevPageBtnClicked)
        self.pushButton_m_po_next_page.clicked.connect(self.onMainNextPageBtnClicked)
        self.pushButton_m_po_jump.clicked.connect(self.onMainJumpBtnClicked)
        self.filters.filterQueryError.connect(lambda: self.queryError("filter"))
        self.pushButton_m_sort_confirm.clicked.connect(self.onMainSortConfirmBtnClicked)
        # self.pushButton_m_po_comfirm_cnt_per_page.clicked.connect(self.onMainCntPerPageBtnClicked)
        self.pushButton_m_to_add.clicked.connect(self.onMainAddTagBtnClicked)
        self.pushButton_m_to_del.clicked.connect(self.onMainDelTagBtnClicked)
        self.pushButton_m_f_addTag.clicked.connect(self.onMainFilterTagAddBtnClicked)
        self.pushButton_m_f_clearTag.clicked.connect(self.onMainFilterTagClearBtnClicked)
        self.pushButton_m_f_rmTag.clicked.connect(self.onMainFilterTagRmBtnClicked)
        self.pushButton_m_f_filter.clicked.connect(self.onMainFilterConfirmBtnClicked)

    def db_connect(self):
        if not os.path.exists(self.dbFile):
            os.makedirs("data")
            conn = sqlite3.connect(self.dbFile)
            c = conn.cursor()
            with open(path_to_sql, 'r', encoding='utf-8') as sql_file:
                c.executescript(sql_file.read())
            conn.commit()
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(self.dbFile)
        if not self.db.open():
            QMessageBox.critical(self, title='数据库打开失败', text=self.db.lastError().text(), buttons=QMessageBox.Ok)

    def getAttrs(self):
        # cols
        if self.query.exec("select * from books"):
            self.colList = []
            for i in range(self.query.record().count()):
                self.colList.append(self.query.record().fieldName(i))
        else:
            self.queryError("getAttrs")

        # tags
        if self.query.exec("select tag_name from tags"):
            while self.query.next():
                self.tagList.append(self.query.value(0))

    def queryError(self, str=''):
        QMessageBox.critical(self, f"错误:{str}",
                             f"数据库操作失败：{self.query.lastError().text()};\n 错误的SQL：{self.query.lastQuery()}",
                             QMessageBox.Ok)

    def noMoreThanOneQuery(self, sql: str, where=''):
        if self.query.exec(sql):
            if self.query.first():
                return True
            else:
                return False
        else:
            self.queryError(where)

    def selectAllBooks(self):
        self.tableView_m_item_list.setModel(self.sqlTableModel)
        self.sqlTableModel.setTable('books')
        self.sqlTableModel.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        for num in range(len(self.bookAttrs)):
            self.sqlTableModel.setHeaderData(num, Qt.Horizontal, self.bookAttrs[num])
        # self.sqlTableModel.setSort(0, Qt.DescendingOrder)

        # self.tableView_m_item_list.setSortingEnabled(True)
        self.tableView_m_item_list.setAutoScroll(True)
        self.tableView_m_item_list.setAlternatingRowColors(True)
        self.tableView_m_item_list.horizontalHeader().setStyleSheet("QHeaderView::section{background:white;}")

        self.updateSqlTableModel()

    def updateSqlTableModel(self):
        self.sqlTableModel.select()
        self.updateTotalPage()
        self.jump2page(self.currentPage)

    def onMainSearchBtnClicked(self):
        scs = self.lineEdit_m_search.text()
        if not scs:
            self.filters.searchContents = []
        else:
            self.filters.searchContents = scs.split()
        self.generateTableSql()
        self.sqlTableModel.setQuery(QSqlQuery(self.pageSql()))
        self.updateSqlTableModel()

    # 标签操作===============================================================================

    def showTags(self, bookId: int):
        self.sqlRelaTableModel.setEditStrategy(QSqlRelationalTableModel.EditStrategy.OnFieldChange)
        self.sqlRelaTableModel.setTable("book_tag")
        self.sqlRelaTableModel.setHeaderData(0, Qt.Horizontal, "id")
        self.sqlRelaTableModel.setHeaderData(1, Qt.Horizontal, "图书id")
        self.sqlRelaTableModel.setHeaderData(2, Qt.Horizontal, "标签")
        self.sqlRelaTableModel.setRelation(2, QSqlRelation("tags", "tag_id", "tag_name"))
        self.sqlRelaTableModel.setFilter(f"book_id={bookId}")
        self.tableView_m_tag.setModel(self.sqlRelaTableModel)
        self.tableView_m_tag.setItemDelegate(QSqlRelationalDelegate(self.tableView_m_tag))
        self.tableView_m_tag.resizeColumnToContents(1)
        self.tableView_m_tag.hideColumn(0)
        self.sqlRelaTableModel.select()

    def onMainItemTableViewClicked(self, row):
        self.currentBookId = self.sqlTableModel.itemData(self.sqlTableModel.index(row, self.bookAttrs.index("图书id")))[
            Qt.DisplayRole]
        self.showTags(self.currentBookId)

    def onMainAddTagBtnClicked(self):
        inputTag = self.lineEdit_m_to_new_tag.text()
        if inputTag == '':
            QMessageBox.information(self, "提示", "请输入tag名", QMessageBox.Ok)
            return
        self.noMoreThanOneQuery(f"select tag_id from tags where tag_name='{inputTag}'", f"getIdOf{inputTag}")
        if self.query.first():
            tagId = self.query.value(0)
            if self.currentBookId is None:
                QMessageBox.information(self, "提示", f"已有此标签，id为{tagId},若要给某本书添加标签请先点击该书", QMessageBox.Ok)
            else:
                # unique constraint
                self.noMoreThanOneQuery(f"insert into book_tag(book_id,tag_id) values ({self.currentBookId},{tagId})")
        else:
            choice = QMessageBox.information(self, "注意", "这是个新标签，确定添加吗？", QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.Yes:
                self.noMoreThanOneQuery(f"insert into tags(tag_name) values ('{inputTag}')")
                if self.currentBookId:
                    self.noMoreThanOneQuery(f"select tag_id from tags where tag_name='{inputTag}'")
                    tagId = self.query.value(0)
                    self.noMoreThanOneQuery(
                        f"insert into book_tag(book_id,tag_id) values ({self.currentBookId},{tagId})")
        self.sqlRelaTableModel.select()

    def onMainDelTagBtnClicked(self):
        if self.currentBookId is None:
            return
        row = self.tableView_m_tag.currentIndex().row()
        if row == -1:
            QMessageBox.information(self, "提示", "用法：先选定图书，再点击需要删除的标签", QMessageBox.Ok)
            return
        selectedTag = self.sqlRelaTableModel.itemData(self.sqlRelaTableModel.index(row, 2))[Qt.DisplayRole]
        self.noMoreThanOneQuery(
            f"delete from book_tag where book_id={self.currentBookId} and tag_id=(select tag_id from tags where tag_name='{selectedTag}')")
        self.sqlRelaTableModel.select()

    # 主表操作================================================================================
    def onMainOptConfirmBtnClicked(self):
        if self.sqlTableModel.submitAll():
            QMessageBox.information(self, "提示", "图书表修改成功", QMessageBox.Ok)
            self.updateSqlTableModel()
        else:
            QMessageBox.critical(self, "错误", "图书表修改失败：" + self.sqlTableModel.lastError().text(), QMessageBox.Ok)
            # 在OnManualSubmit模式下，当submitAll()失败时，已经提交的更改不会从缓存中清除。这允许事务回滚并重新提交，而不会丢失数据。

    def onMainOptCancelBtnClicked(self):
        if self.sqlTableModel.revertAll():
            QMessageBox.information(self, "提示", "已取消", QMessageBox.Ok)
            self.updateSqlTableModel()

    def generateTableSql(self, count=False):
        if count:
            prefix = "select count(*) from books "
        else:
            prefix = self.tableBasicSql
        if self.filters.isEmpty():
            sql = prefix + f" order by `{self.tableSortField}` {self.tableSortDirect} "
        else:
            sql = prefix + " where 1=1 "
            if self.filters.searchContents:
                sql = sql + " and " + self.filters.getSearchContentSql(self.colList)
            if self.filters.status is not None:
                sql = sql + f" and status='{self.filters.status}' "
            if self.filters.readStatus is not None:
                sql=sql+f" and read_status='{self.filters.readStatus}'"
            if self.filters.score:
                sql = sql + f" and rating>={self.filters.score[0]} and rating<={self.filters.score[1]} "
            if self.filters.tags:
                sql = sql + f" and " + self.filters.getTagFilterSql()
            sql = sql + f" order by `{self.tableSortField}` {self.tableSortDirect} "
        if count:
            return sql
        else:
            self.tableSql = sql
            return self.tableSql

    def deleteRow(self, rowCheck=True):
        row = self.tableView_m_item_list.currentIndex().row()
        if rowCheck and row == -1:
            QMessageBox.information(self, "提示", "要删除哪一条呢？请点击它的任意一个格子", QMessageBox.Ok)
            return
        self.sqlTableModel.removeRow(row)

    def onMainDelRowBtnClicked(self, ask=True, rowCheck=True):
        choice = QMessageBox.Yes
        if ask:
            choice = QMessageBox.question(self, '注意', '确定要删除该项吗？', QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            try:
                self.deleteRow(rowCheck)
                self.sqlTableModel.submitAll()
                self.updateSqlTableModel()
            except:
                QMessageBox.critical(self, "错误", self.sqlTableModel.lastError(), QMessageBox.Ok)
                return
        else:
            return

    def deleteFile(self):
        row = self.tableView_m_item_list.currentIndex().row()
        if row == -1:
            QMessageBox.information(self, "提示", "要删除哪个文件呢？请点击它的任意一个格子", QMessageBox.Ok)
            return
        location = self.sqlTableModel.itemData(self.sqlTableModel.index(row, self.bookAttrs.index("地址")))[
            Qt.DisplayRole]
        if location is None:
            QMessageBox.information(self, "提示", "找不到地址", QMessageBox.Ok)
            return
        if re.match("[ht,f]tp", location, re.I):
            QMessageBox.information(self, "提示", "文件在网络上，无法从本地删除", QMessageBox.Ok)
            return
        try:
            # os.remove(location)
            shell.SHFileOperation((0, shellcon.FO_DELETE, location, None,
                                   shellcon.FOF_SILENT | shellcon.FOF_ALLOWUNDO | shellcon.FOF_NOCONFIRMATION,
                                   None, None))  # 删除文件到回收站
            choice = QMessageBox.information(self, "提示", "已删除！删除本条记录？", QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.Yes:
                self.onMainDelRowBtnClicked(ask=False, rowCheck=False)
        except OSError as e:
            QMessageBox.critical(self, "错误", "文件删除失败：" + e.strerror, QMessageBox.Ok)
            return

    def onMainDelFileBtnClicked(self):
        choice = QMessageBox.question(self, '注意', '确定要删除该文件吗？', QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            try:
                self.deleteFile()
                try:
                    self.sqlTableModel.submitAll()
                    self.updateSqlTableModel()
                except:
                    QMessageBox.critical(self, "错误", self.sqlTableModel.lastError(), QMessageBox.Ok)
                    return
            except:
                return
        else:
            return

    def onMainOpenDirBtnClicked(self):
        row = self.tableView_m_item_list.currentIndex().row()
        if row == -1:
            QMessageBox.information(self, "提示", "要打开哪一条呢？请点击它的任意一个格子", QMessageBox.Ok)
            return
        location = self.sqlTableModel.itemData(self.sqlTableModel.index(row, self.bookAttrs.index("地址")))[
            Qt.DisplayRole]
        if location is None:
            QMessageBox.information(self, "提示", "找不到地址", QMessageBox.Ok)
            return
        if re.match("^[ht,f]tp", location, re.I):
            QDesktopServices.openUrl(QUrl(location))
        else:
            subprocess.Popen(r'explorer /select,"' + str(pathlib.Path(location)) + '"')

    def onMainOpenFileBtnClicked(self):
        row = self.tableView_m_item_list.currentIndex().row()
        if row == -1:
            QMessageBox.information(self, "提示", "要打开哪一条呢？请点击它的任意一个格子", QMessageBox.Ok)
            return
        location = self.sqlTableModel.itemData(self.sqlTableModel.index(row, self.bookAttrs.index("地址")))[
            Qt.DisplayRole]
        if location is None:
            QMessageBox.information(self, "提示", "找不到地址", QMessageBox.Ok)
            return
        if re.match("[ht,f]tp", location, re.I):
            QDesktopServices.openUrl(QUrl(location))
        else:
            # location=str(pathlib.Path(location))
            if os.path.isfile(location):
                if not QDesktopServices.openUrl(QUrl(QUrl.fromLocalFile(location))):
                    print(location)
                    QMessageBox.information(self, "错误", "文件路径可能不正确\n请检查是否为空或者地址格式是否错误", QMessageBox.Ok)
            else:
                QMessageBox.information(self, "错误", "路径非文件", QMessageBox.Ok)

    # 页码操作================================================================================
    def pageSql(self):
        return self.tableSql + f" limit {self.currentPage * self.cntPerPage},{self.cntPerPage} "

    def jump2page(self, page: int):
        self.currentPage = page
        self.generateTableSql()
        self.sqlTableModel.setQuery(QSqlQuery(self.pageSql()))
        self.label_m_po_page_ye.setText(f"{page + 1}页")

    def updateTotalPage(self):
        self.query.exec(self.generateTableSql(count=True))
        if self.query.first():
            totalCnt = int(self.query.value(0))
        else:
            self.queryError("totalpage")
            return
        tp = math.ceil(float(totalCnt) / float(self.cntPerPage))
        self.label_m_po_total_page_cnt.setText(f"{tp}页")
        self.totalPage = tp
        self.spinBox_m_po_jump_page.setMaximum(tp)

    def onMainPrevPageBtnClicked(self):
        self.currentPage -= 1
        if self.currentPage < 0:
            self.currentPage = 0
        self.jump2page(self.currentPage)

    def onMainNextPageBtnClicked(self):
        self.currentPage += 1
        if self.currentPage >= self.totalPage - 1:
            self.currentPage = self.totalPage - 1
        self.jump2page(self.currentPage)

    def onMainJumpBtnClicked(self):
        toPage = self.spinBox_m_po_jump_page.value() - 1
        self.jump2page(toPage)

    # TODO 每页显示x个
    def onMainCntPerPageBtnClicked(self):
        lastCpp = self.cntPerPage
        self.cntPerPage = self.spinBox_m_po_cnt_per_page.value()
        if self.currentPage == 0:
            self.jump2page(0)
        else:
            offset = self.currentPage * lastCpp
            self.jump2page(math.ceil(offset / self.cntPerPage) - 1)

    # 排序操作===============================================================================
    def onMainSortConfirmBtnClicked(self):
        self.tableSortField = self.colList[self.comboBox_m_sort_field.currentIndex()]
        if self.comboBox_n_sort_direct.currentText() == "升序":
            self.tableSortDirect = "asc"
        else:
            self.tableSortDirect = "desc"
        self.jump2page(0)

    # 筛选操作===============================================================================
    def onMainFilterTagAddBtnClicked(self):
        selectedTag = self.comboBox_m_f_tag.currentText()
        if selectedTag in self.filterTagList:
            return
        self.filterTagList.append(selectedTag)
        self.stringListModelTagFilter.setStringList(self.filterTagList)
        self.comboBox_m_f_tag.clear()
        self.comboBox_m_f_tag.addItems(sorted(list(set(self.tagList) - set(self.filterTagList))))

    def onMainFilterTagClearBtnClicked(self):
        self.filterTagList = []
        self.stringListModelTagFilter.setStringList(self.filterTagList)
        self.comboBox_m_f_tag.clear()
        self.comboBox_m_f_tag.addItems(self.tagList)

    def onMainFilterTagRmBtnClicked(self):
        row = self.listView_m_f_tags.currentIndex().row()
        if row == -1:
            QMessageBox.information(self, "提示", "点击要移除的标签", QMessageBox.Ok)
        tag2rm = self.stringListModelTagFilter.itemData(self.stringListModelTagFilter.index(row))[Qt.DisplayRole]
        self.filterTagList.remove(tag2rm)
        self.stringListModelTagFilter.setStringList(self.filterTagList)
        self.comboBox_m_f_tag.addItem(tag2rm)

    def onMainFilterConfirmBtnClicked(self):
        curstatus = self.comboBox_m_f_status.currentText()
        if curstatus=="全部":
            self.filters.status=None
        else:
            self.filters.status=curstatus
        curReadStatus=self.comboBox_m_f_read.currentText()
        if curReadStatus=="全部":
            self.filters.readStatus=None
        else:
            self.filters.readStatus=curReadStatus
        scoreMin = self.spinBox_m_f_score_from.value()
        scoreMax = self.spinBox_m_f_score_to.value()
        self.filters.score = [scoreMin, scoreMax]
        self.filters.tags.clear()
        for i in range(self.stringListModelTagFilter.rowCount()):
            self.filters.tags.append(
                self.stringListModelTagFilter.itemData(self.stringListModelTagFilter.index(i))[Qt.DisplayRole])
        self.generateTableSql()
        self.sqlTableModel.setQuery(QSqlQuery(self.pageSql()))
        self.updateSqlTableModel()

    def onAddAddedNew(self):
        self.getAttrs()
        self.jump2page(self.currentPage)
        self.comboBox_m_f_tag.clear()
        self.comboBox_m_f_tag.addItems(self.tagList)

    def testSlot(self):
        print("signal")

    def closeEvent(self, QCloseEvent):
        self.db.close()
