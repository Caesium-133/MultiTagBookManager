# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_addDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(553, 505)
        self.label_a_fileLocation = QtWidgets.QLabel(Dialog)
        self.label_a_fileLocation.setGeometry(QtCore.QRect(30, 20, 72, 15))
        self.label_a_fileLocation.setObjectName("label_a_fileLocation")
        self.lineEdit_a_fileLocation = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_a_fileLocation.setGeometry(QtCore.QRect(20, 40, 411, 31))
        self.lineEdit_a_fileLocation.setObjectName("lineEdit_a_fileLocation")
        self.pushButton_a_openLocal = QtWidgets.QPushButton(Dialog)
        self.pushButton_a_openLocal.setGeometry(QtCore.QRect(440, 40, 93, 28))
        self.pushButton_a_openLocal.setObjectName("pushButton_a_openLocal")
        self.groupBox_a_cat = QtWidgets.QGroupBox(Dialog)
        self.groupBox_a_cat.setGeometry(QtCore.QRect(20, 90, 141, 111))
        self.groupBox_a_cat.setObjectName("groupBox_a_cat")
        self.comboBox_a_firstCat = QtWidgets.QComboBox(self.groupBox_a_cat)
        self.comboBox_a_firstCat.setGeometry(QtCore.QRect(10, 20, 121, 22))
        self.comboBox_a_firstCat.setObjectName("comboBox_a_firstCat")
        self.comboBox_a_secondCat = QtWidgets.QComboBox(self.groupBox_a_cat)
        self.comboBox_a_secondCat.setGeometry(QtCore.QRect(10, 50, 121, 22))
        self.comboBox_a_secondCat.setObjectName("comboBox_a_secondCat")
        self.comboBox_a_thirdCat = QtWidgets.QComboBox(self.groupBox_a_cat)
        self.comboBox_a_thirdCat.setGeometry(QtCore.QRect(10, 80, 121, 22))
        self.comboBox_a_thirdCat.setObjectName("comboBox_a_thirdCat")
        self.label_a_score = QtWidgets.QLabel(Dialog)
        self.label_a_score.setGeometry(QtCore.QRect(20, 280, 31, 16))
        self.label_a_score.setObjectName("label_a_score")
        self.pushButton_a_addTag = QtWidgets.QPushButton(Dialog)
        self.pushButton_a_addTag.setGeometry(QtCore.QRect(370, 110, 41, 28))
        self.pushButton_a_addTag.setObjectName("pushButton_a_addTag")
        self.label_a_tag = QtWidgets.QLabel(Dialog)
        self.label_a_tag.setGeometry(QtCore.QRect(250, 90, 72, 15))
        self.label_a_tag.setObjectName("label_a_tag")
        self.spinBox_a_score = QtWidgets.QSpinBox(Dialog)
        self.spinBox_a_score.setGeometry(QtCore.QRect(60, 280, 71, 22))
        self.spinBox_a_score.setObjectName("spinBox_a_score")
        self.pushButton_a_rmTag = QtWidgets.QPushButton(Dialog)
        self.pushButton_a_rmTag.setGeometry(QtCore.QRect(440, 180, 93, 28))
        self.pushButton_a_rmTag.setObjectName("pushButton_a_rmTag")
        self.pushButton_a_confirm = QtWidgets.QPushButton(Dialog)
        self.pushButton_a_confirm.setGeometry(QtCore.QRect(400, 460, 61, 28))
        self.pushButton_a_confirm.setObjectName("pushButton_a_confirm")
        self.pushButton_a_clear = QtWidgets.QPushButton(Dialog)
        self.pushButton_a_clear.setGeometry(QtCore.QRect(470, 460, 61, 28))
        self.pushButton_a_clear.setObjectName("pushButton_a_clear")
        self.comboBox_a_status = QtWidgets.QComboBox(Dialog)
        self.comboBox_a_status.setGeometry(QtCore.QRect(60, 320, 81, 22))
        self.comboBox_a_status.setObjectName("comboBox_a_status")
        self.label_a_status = QtWidgets.QLabel(Dialog)
        self.label_a_status.setGeometry(QtCore.QRect(20, 320, 31, 16))
        self.label_a_status.setObjectName("label_a_status")
        self.pushButton_a_clearTag = QtWidgets.QPushButton(Dialog)
        self.pushButton_a_clearTag.setGeometry(QtCore.QRect(440, 220, 93, 28))
        self.pushButton_a_clearTag.setObjectName("pushButton_a_clearTag")
        self.listView_a_tags = QtWidgets.QListView(Dialog)
        self.listView_a_tags.setGeometry(QtCore.QRect(240, 140, 181, 211))
        self.listView_a_tags.setObjectName("listView_a_tags")
        self.lineEdit_a_tag = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_a_tag.setGeometry(QtCore.QRect(250, 110, 113, 21))
        self.lineEdit_a_tag.setObjectName("lineEdit_a_tag")
        self.label_a_shuming = QtWidgets.QLabel(Dialog)
        self.label_a_shuming.setGeometry(QtCore.QRect(20, 210, 72, 15))
        self.label_a_shuming.setObjectName("label_a_shuming")
        self.label_add_zuozhe = QtWidgets.QLabel(Dialog)
        self.label_add_zuozhe.setGeometry(QtCore.QRect(20, 240, 72, 15))
        self.label_add_zuozhe.setObjectName("label_add_zuozhe")
        self.lineEdit_add_book_name = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_add_book_name.setGeometry(QtCore.QRect(60, 210, 161, 21))
        self.lineEdit_add_book_name.setObjectName("lineEdit_add_book_name")
        self.lineEdit_add_author = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_add_author.setGeometry(QtCore.QRect(60, 240, 161, 21))
        self.lineEdit_add_author.setObjectName("lineEdit_add_author")
        self.label_add_wangzhan = QtWidgets.QLabel(Dialog)
        self.label_add_wangzhan.setGeometry(QtCore.QRect(20, 360, 72, 15))
        self.label_add_wangzhan.setObjectName("label_add_wangzhan")
        self.lineEdit_add_website = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_add_website.setGeometry(QtCore.QRect(60, 360, 161, 21))
        self.lineEdit_add_website.setObjectName("lineEdit_add_website")
        self.label_a_gengxinzhangjie = QtWidgets.QLabel(Dialog)
        self.label_a_gengxinzhangjie.setGeometry(QtCore.QRect(20, 400, 72, 15))
        self.label_a_gengxinzhangjie.setObjectName("label_a_gengxinzhangjie")
        self.label_a_shangcigegnxinriqi = QtWidgets.QLabel(Dialog)
        self.label_a_shangcigegnxinriqi.setGeometry(QtCore.QRect(10, 430, 91, 16))
        self.label_a_shangcigegnxinriqi.setObjectName("label_a_shangcigegnxinriqi")
        self.lineEdit_a_updated_chapter = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_a_updated_chapter.setGeometry(QtCore.QRect(90, 400, 131, 21))
        self.lineEdit_a_updated_chapter.setObjectName("lineEdit_a_updated_chapter")
        self.lineEdit_a_last_update_date = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_a_last_update_date.setGeometry(QtCore.QRect(110, 430, 111, 21))
        self.lineEdit_a_last_update_date.setObjectName("lineEdit_a_last_update_date")
        self.label_a_pinglun = QtWidgets.QLabel(Dialog)
        self.label_a_pinglun.setGeometry(QtCore.QRect(240, 360, 72, 15))
        self.label_a_pinglun.setObjectName("label_a_pinglun")
        self.plainTextEdit_a_review = QtWidgets.QPlainTextEdit(Dialog)
        self.plainTextEdit_a_review.setGeometry(QtCore.QRect(240, 380, 281, 71))
        self.plainTextEdit_a_review.setObjectName("plainTextEdit_a_review")
        self.label_a_info = QtWidgets.QLabel(Dialog)
        self.label_a_info.setGeometry(QtCore.QRect(110, 10, 421, 16))
        self.label_a_info.setText("")
        self.label_a_info.setObjectName("label_a_info")
        self.label_a_yueduzhuangtai = QtWidgets.QLabel(Dialog)
        self.label_a_yueduzhuangtai.setGeometry(QtCore.QRect(20, 470, 72, 15))
        self.label_a_yueduzhuangtai.setObjectName("label_a_yueduzhuangtai")
        self.comboBox_a_read = QtWidgets.QComboBox(Dialog)
        self.comboBox_a_read.setGeometry(QtCore.QRect(90, 470, 131, 22))
        self.comboBox_a_read.setObjectName("comboBox_a_read")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_a_fileLocation.setText(_translate("Dialog", "文件路径"))
        self.pushButton_a_openLocal.setText(_translate("Dialog", "浏览"))
        self.groupBox_a_cat.setTitle(_translate("Dialog", "分类"))
        self.label_a_score.setText(_translate("Dialog", "评分"))
        self.pushButton_a_addTag.setText(_translate("Dialog", "添加"))
        self.label_a_tag.setText(_translate("Dialog", "标签"))
        self.pushButton_a_rmTag.setText(_translate("Dialog", "移除标签"))
        self.pushButton_a_confirm.setText(_translate("Dialog", "确定"))
        self.pushButton_a_clear.setText(_translate("Dialog", "清除"))
        self.label_a_status.setText(_translate("Dialog", "状态"))
        self.pushButton_a_clearTag.setText(_translate("Dialog", "清空标签"))
        self.label_a_shuming.setText(_translate("Dialog", "书名"))
        self.label_add_zuozhe.setText(_translate("Dialog", "作者"))
        self.label_add_wangzhan.setText(_translate("Dialog", "网站"))
        self.label_a_gengxinzhangjie.setText(_translate("Dialog", "更新章节"))
        self.label_a_shangcigegnxinriqi.setText(_translate("Dialog", "上次更新日期"))
        self.label_a_pinglun.setText(_translate("Dialog", "评论"))
        self.label_a_yueduzhuangtai.setText(_translate("Dialog", "阅读状态"))
