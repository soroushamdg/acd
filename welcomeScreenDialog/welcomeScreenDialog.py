# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Design\qtDesigner\welcomeScreenDialog\welcomeScreenDialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!
import logging

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from menuBar import appinfo
from welcomeScreenDialog import welcomeScreenThreads


class Ui_welcomeScreenDialog(QtWidgets.QDialog):
    errorflag = False
    retstatus = None
    def __init__(self,parent):
        super(Ui_welcomeScreenDialog, self).__init__(parent)

        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setObjectName("welcomeScreenDialog")
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.resize(300, 550)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(300, 550))
        self.setMaximumSize(QtCore.QSize(300, 550))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/media/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setStyleSheet("QDialog{\n"
"background:rgb(0, 0, 0);\n"
"}\n"
"QPushButton{background:#121212;border: 1px solid #f8f8f8;border-radius:15px;\n"
"color:white;\n"
"font: 12pt \"Poppins\";padding:3px 6px}\n"
"\n"
"QPushButton:hover{background:#484848;}\n"
"QPushButton:pressed{background:#000000;}")
        self.versionNumberLabel = QtWidgets.QLabel(self)
        self.versionNumberLabel.setGeometry(QtCore.QRect(10, 320, 281, 21))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        self.versionNumberLabel.setFont(font)
        self.versionNumberLabel.setStyleSheet("color:#f8f8f8;")
        self.versionNumberLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.versionNumberLabel.setObjectName("versionNumberLabel")
        self.checkingdepLabel = QtWidgets.QLabel(self)
        self.checkingdepLabel.setGeometry(QtCore.QRect(60, 350, 231, 31))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(10)
        self.checkingdepLabel.setFont(font)
        self.checkingdepLabel.setStyleSheet("color:#f8f8f8;")
        self.checkingdepLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.checkingdepLabel.setObjectName("checkingdepLabel")
        self.checkingdebStatusLabel = QtWidgets.QLabel(self)
        self.checkingdebStatusLabel.setEnabled(False)
        self.checkingdebStatusLabel.setGeometry(QtCore.QRect(10, 350, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(12)
        self.checkingdebStatusLabel.setFont(font)
        self.checkingdebStatusLabel.setStyleSheet("color:#f8f8f8;")
        self.checkingdebStatusLabel.setText("")
        self.checkingdebStatusLabel.setPixmap(QtGui.QPixmap(":/media/success-label.png"))
        self.checkingdebStatusLabel.setScaledContents(True)
        self.checkingdebStatusLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.checkingdebStatusLabel.setObjectName("checkingdebStatusLabel")
        self.settingConfigStatusLabel = QtWidgets.QLabel(self)
        self.settingConfigStatusLabel.setEnabled(False)
        self.settingConfigStatusLabel.setGeometry(QtCore.QRect(10, 390, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(12)
        self.settingConfigStatusLabel.setFont(font)
        self.settingConfigStatusLabel.setStyleSheet("color:#f8f8f8;")
        self.settingConfigStatusLabel.setText("")
        self.settingConfigStatusLabel.setPixmap(QtGui.QPixmap(":/media/success-label.png"))
        self.settingConfigStatusLabel.setScaledContents(True)
        self.settingConfigStatusLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.settingConfigStatusLabel.setObjectName("settingConfigStatusLabel")
        self.settingConfigLabel = QtWidgets.QLabel(self)
        self.settingConfigLabel.setGeometry(QtCore.QRect(60, 390, 231, 31))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(10)
        self.settingConfigLabel.setFont(font)
        self.settingConfigLabel.setStyleSheet("color:#f8f8f8;")
        self.settingConfigLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.settingConfigLabel.setObjectName("settingConfigLabel")
        self.changesLogLabel = QtWidgets.QLabel(self)
        self.changesLogLabel.setGeometry(QtCore.QRect(10, 430, 281, 21))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(9)
        self.changesLogLabel.setFont(font)
        self.changesLogLabel.setStyleSheet("color:#f8f8f8;")
        self.changesLogLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.changesLogLabel.setObjectName("changesLogLabel")
        self.changesLogTextEdit = QtWidgets.QPlainTextEdit(self)
        self.changesLogTextEdit.setGeometry(QtCore.QRect(10, 450, 281, 51))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        self.changesLogTextEdit.setFont(font)
        self.changesLogTextEdit.setDocumentTitle("")
        self.changesLogTextEdit.setReadOnly(True)
        self.changesLogTextEdit.setPlainText("")
        self.changesLogTextEdit.setBackgroundVisible(False)
        self.changesLogTextEdit.setObjectName("changesLogTextEdit")
        self.DialogButtonBox = QtWidgets.QDialogButtonBox(self)
        self.DialogButtonBox.setGeometry(QtCore.QRect(11, 512, 281, 28))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.DialogButtonBox.setFont(font)
        self.DialogButtonBox.setStyleSheet("")
        self.DialogButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.DialogButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.DialogButtonBox.setObjectName("DialogButtonBox")
        self.welcome2acdLabel = QtWidgets.QLabel(self)
        self.welcome2acdLabel.setGeometry(QtCore.QRect(10, 280, 281, 50))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(18)
        self.welcome2acdLabel.setFont(font)
        self.welcome2acdLabel.setStyleSheet("color:#f8f8f8;")
        self.welcome2acdLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.welcome2acdLabel.setObjectName("welcome2acdLabel")



        self.wcdLogoAnimatedGifLabel = QtWidgets.QLabel(self)
        self.wcdLogoAnimatedGifLabel.setGeometry(QtCore.QRect(10, 10, 281, 261))
        self.wcdLogoAnimatedGifLabel.setMaximumSize(QtCore.QSize(300, 300))
        self.wcdLogoAnimatedGifLabel.setText("")
        self.wcdLogoAnimatedGifLabel.setScaledContents(False)
        self.wcdLogoAnimatedGifLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.wcdLogoAnimatedGifLabel.setObjectName("wcdLogoAnimatedGifLabel")
        movie = QtGui.QMovie(":/media/animated_logo.gif")
        self.wcdLogoAnimatedGifLabel.setMovie(movie)
        movie.start()

        self.retranslateUi(self)
        self.DialogButtonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.reject)

        self.DialogButtonBox.setDisabled(True)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.define_thread()
        self.start_thread()

    def raise_dialog(self,title,message,description,needretry=False):
        try:
            msg = QMessageBox()
            msg.setText(message)
            msg.setInformativeText(description)
            msg.setWindowTitle(title)
            if needretry:
                self.raise_errorflag()
                msg.setStandardButtons(QMessageBox.Retry | QMessageBox.Cancel)
                self.configurationTaskThread.quit()
                self.configurationTaskThread.terminate()
                self.configurationTaskThread.wait()
            else:
                msg.setStandardButtons(QMessageBox.Close)
                self.configurationTaskThread.quit()
            retval = msg.exec()
            if retval == QMessageBox.Retry:
                self.errorflag = False
                self.define_thread()
                self.start_thread()
            elif retval == QMessageBox.Cancel or QMessageBox.Close:
                self.retstatus= 'CANCEL'
                self.close()


        except Exception as msg:
            logging.debug('error'+msg)

    def raise_errorflag(self):
        self.errorflag = True

    def check_dependencies_status(self,status):
        if status:
            self.checkingdebStatusLabel.setEnabled(True)
        else:
            self.checkingdebStatusLabel.setDisabled(True)

    def setting_basic_config_status(self,status):
        if status:
            self.settingConfigStatusLabel.setEnabled(True)
        else:
            self.settingConfigStatusLabel.setDisabled(True)

    def configuration_finished(self):
        if not self.errorflag:
            self.retstatus = 'COMPLETED'
            self.DialogButtonBox.setEnabled(True)

    def define_thread(self):
        self.configurationTaskThread = welcomeScreenThreads.configurationThread()
        self.configurationTaskThread.check_dependencies_status.connect(self.check_dependencies_status)
        self.configurationTaskThread.setting_basic_config_status.connect(self.setting_basic_config_status)
        self.configurationTaskThread.raise_dialog.connect(self.raise_dialog)
        self.configurationTaskThread.raise_errorflag.connect(self.raise_errorflag)
        self.configurationTaskThread.finished.connect(self.configuration_finished)

    def start_thread(self):
        self.configurationTaskThread.start()

    def retranslateUi(self, welcomeScreenDialog):
        _translate = QtCore.QCoreApplication.translate
        welcomeScreenDialog.setWindowTitle(_translate("welcomeScreenDialog", "Welcome to ACD"))
        self.versionNumberLabel.setText(_translate("welcomeScreenDialog", f"Version {appinfo.VERSION}"))
        self.checkingdepLabel.setText(_translate("welcomeScreenDialog", "Checking dependencies"))
        self.settingConfigLabel.setText(_translate("welcomeScreenDialog", "Setting basic config"))
        self.changesLogLabel.setText(_translate("welcomeScreenDialog", "Changes log:"))
        self.welcome2acdLabel.setText(_translate("welcomeScreenDialog", "Welcome to ACD"))
import welcomeScreenDialog.welcomeDialogResources_rc
