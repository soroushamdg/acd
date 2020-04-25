# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mafuckingui.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!
import subprocess
import concurrent.futures
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QInputDialog,QLineEdit,QListWidget
import time
from pyLog.pylog import log
import sys,os
import options
from bytes_downloaded_info import bytes_downloaded

def check_ffmpeg(bin_path,command):
    ffmpeg_dir = bin_path + ''
    try:
        print(ffmpeg_dir + command)
        output = subprocess.check_output(ffmpeg_dir + command)
    except:
        print("error in running command in ffmpeg.")
        return False
    else:
        return True

#first import options and set and load all data, then import backend options
try:
    options.load_options()
except:
    log.log(__name__,"can't load options file.")
    log.close_file()
    sys.exit()
else:
    #setting options for backend
    from backend import options as back_options
    back_options.define_temp_path(options.options['main_exe_path'])
    back_options.define_export_path(options.options['main_exe_path'])

found_ffmpeg = False
ffmpeg_working = False
database_found = False
selected_school_dict = {}

executor = concurrent.futures.ThreadPoolExecutor()
in_downloading_process = False
class Ui_MainWindow(QtWidgets.QWidget):
    global database_found,ffmpeg_working,found_ffmpeg
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(918, 402)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(918, 402))
        MainWindow.setMaximumSize(QtCore.QSize(918, 402))
        font = QtGui.QFont()
        font.setFamily("Microsoft JhengHei UI")
        font.setPointSize(-1)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("_acd_logo_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("background-color : #1e1e2c;\n"
"color : #f8f8f8;\n"
"/* font-family :\"Microsoft JhengHei UI\", \"Arial\"; */\n"
"font-size : 16px;")
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 891, 321))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout.setSpacing(12)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.horizontalLayoutWidget)
        self.groupBox.setStyleSheet("")
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 30, 171, 16))
        self.label.setObjectName("label")
        self.findFFMPEGButton = QtWidgets.QPushButton(self.groupBox)
        self.findFFMPEGButton.setGeometry(QtCore.QRect(10, 60, 191, 31))
        self.findFFMPEGButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.findFFMPEGButton.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(228, 228, 228, 255), stop:1 rgba(255, 255, 255, 255));\n"
"color:2d2d44;\n"
"border-radius : 10px;")
        self.findFFMPEGButton.setObjectName("findFFMPEGButton")
        self.findFFMPEGButton.clicked.connect(self.openFileNameDialog)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 110, 171, 16))
        self.label_2.setObjectName("label_2")
        self.findDataBaseFileButton = QtWidgets.QPushButton(self.groupBox)
        self.findDataBaseFileButton.setGeometry(QtCore.QRect(10, 140, 191, 31))
        self.findDataBaseFileButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.findDataBaseFileButton.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(228, 228, 228, 255), stop:1 rgba(255, 255, 255, 255));\n"
"color:2d2d44;\n"
"border-radius : 10px;")
        self.findDataBaseFileButton.setObjectName("findDataBaseFileButton")
        self.stage1DoneButton = QtWidgets.QPushButton(self.groupBox)
        self.stage1DoneButton.setGeometry(QtCore.QRect(60, 270, 91, 31))
        self.stage1DoneButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.stage1DoneButton.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(228, 228, 228, 255), stop:1 rgba(255, 255, 255, 255));\n"
"color:2d2d44;\n"
"border-radius : 10px;")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("ok.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stage1DoneButton.setIcon(icon1)
        self.stage1DoneButton.setObjectName("stage1DoneButton")
        self.horizontalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.horizontalLayoutWidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(10, 25, 171, 16))
        self.label_3.setAutoFillBackground(False)
        self.label_3.setStyleSheet("font-size:16px;")
        self.label_3.setObjectName("label_3")
        self.schoolsComboBox = QtWidgets.QComboBox(self.groupBox_2)
        self.schoolsComboBox.setGeometry(QtCore.QRect(10, 49, 191, 31))
        self.schoolsComboBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.schoolsComboBox.setStyleSheet("background-color:#f8f8f8;\n"
"color:#2d2d44;\n"
"padding : 5px;\n"
"border-radius : 10px;")
        self.schoolsComboBox.setObjectName("schoolsComboBox")
        self.schoolsComboBox.currentIndexChanged.connect(self.select_university_by_combox)
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(10, 130, 191, 41))
        self.label_4.setAutoFillBackground(False)
        self.label_4.setStyleSheet("font-size:16px;")
        self.label_4.setLineWidth(1)
        self.label_4.setMidLineWidth(1)
        self.label_4.setScaledContents(True)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.usernameInputField = QtWidgets.QLineEdit(self.groupBox_2)
        self.usernameInputField.setGeometry(QtCore.QRect(10, 180, 191, 31))
        self.usernameInputField.setAutoFillBackground(False)
        self.usernameInputField.setStyleSheet("border-radius : 15px;\n"
"background-color : #f8f8f8;\n"
"color : #2d2d44;\n"
"padding-left:10px;\n"
"font-size:12px;")
        self.usernameInputField.setObjectName("usernameInputField")
        self.passwordInputField = QtWidgets.QLineEdit(self.groupBox_2)
        self.passwordInputField.setGeometry(QtCore.QRect(10, 220, 191, 31))
        self.passwordInputField.setAutoFillBackground(False)
        self.passwordInputField.setStyleSheet("border-radius : 15px;\n"
"background-color : #f8f8f8;\n"
"color : #2d2d44;\n"
"padding-left:10px;\n"
"font-size:12px;")
        self.passwordInputField.setText("")
        self.passwordInputField.setFrame(True)
        self.passwordInputField.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordInputField.setObjectName("passwordInputField")
        self.stage2DoneButton = QtWidgets.QPushButton(self.groupBox_2)
        self.stage2DoneButton.setGeometry(QtCore.QRect(60, 270, 91, 31))
        self.stage2DoneButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.stage2DoneButton.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(228, 228, 228, 255), stop:1 rgba(255, 255, 255, 255));\n"
"color:2d2d44;\n"
"border-radius : 10px;")
        self.stage2DoneButton.setIcon(icon1)
        self.stage2DoneButton.setObjectName("stage2DoneButton")
        self.stage2DoneButton.clicked.connect(self.check_stage_2)
        self.requestSchoolButton = QtWidgets.QPushButton(self.groupBox_2)
        self.requestSchoolButton.setGeometry(QtCore.QRect(10, 90, 191, 31))
        self.requestSchoolButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.requestSchoolButton.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(228, 228, 228, 255), stop:1 rgba(255, 255, 255, 255));\n"
"color:2d2d44;\n"
"border-radius : 10px;")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("it.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.requestSchoolButton.setIcon(icon2)
        self.requestSchoolButton.setObjectName("requestSchoolButton")
        self.horizontalLayout.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.horizontalLayoutWidget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.addCoursesLinkButton = QtWidgets.QPushButton(self.groupBox_3)
        self.addCoursesLinkButton.setGeometry(QtCore.QRect(170, 40, 31, 31))
        self.addCoursesLinkButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.addCoursesLinkButton.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(228, 228, 228, 255), stop:1 rgba(255, 255, 255, 255));\n"
"color:2d2d44;\n"
"border-radius : 10px;")
        self.addCoursesLinkButton.setObjectName("addCoursesLinkButton")
        self.addCoursesLinkButton.clicked.connect(self.add_link_button)
        self.removeCourseLinkButton = QtWidgets.QPushButton(self.groupBox_3)
        self.removeCourseLinkButton.setGeometry(QtCore.QRect(170, 90, 31, 31))
        self.removeCourseLinkButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.removeCourseLinkButton.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(228, 228, 228, 255), stop:1 rgba(255, 255, 255, 255));\n"
"color:2d2d44;\n"
"border-radius : 10px;")
        self.removeCourseLinkButton.setObjectName("removeCourseLinkButton")
        self.removeCourseLinkButton.clicked.connect(self.remove_selected_item)
        self.coursesList = QtWidgets.QListWidget(self.groupBox_3)
        self.coursesList.setGeometry(QtCore.QRect(10, 30, 151, 181))
        self.coursesList.setStyleSheet("background-color:#f8f8f8;\n"
"color:#2d2d44;\n"
"border-radius : 5px;")
        self.coursesList.setObjectName("coursesList")
        self.coursesList.clicked.connect(self.selected_link_from_list)
        self.startCourseButtonLink = QtWidgets.QPushButton(self.groupBox_3)
        self.startCourseButtonLink.setGeometry(QtCore.QRect(10, 230, 61, 31))
        self.startCourseButtonLink.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.startCourseButtonLink.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(228, 228, 228, 255), stop:1 rgba(255, 255, 255, 255));\n"
"color:2d2d44;\n"
"border-radius : 10px;")
        self.startCourseButtonLink.setObjectName("startCourseButtonLink")
        self.startCourseButtonLink.clicked.connect(self.start_downloading_button)
        self.failDownloadLCDNumber = QtWidgets.QLCDNumber(self.groupBox_3)
        self.failDownloadLCDNumber.setGeometry(QtCore.QRect(160, 230, 41, 23))
        self.failDownloadLCDNumber.setStyleSheet("font-size : 16px;\n"
"color : #ff5500;")
        self.failDownloadLCDNumber.setSmallDecimalPoint(True)
        self.failDownloadLCDNumber.setDigitCount(2)
        self.failDownloadLCDNumber.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        self.failDownloadLCDNumber.setProperty("value", 126.0)
        self.failDownloadLCDNumber.setObjectName("failDownloadLCDNumber")
        self.label_5 = QtWidgets.QLabel(self.groupBox_3)
        self.label_5.setGeometry(QtCore.QRect(90, 230, 61, 31))
        self.label_5.setObjectName("label_5")
        self.downloadProgressBar = QtWidgets.QProgressBar(self.groupBox_3)
        self.downloadProgressBar.setGeometry(QtCore.QRect(10, 280, 191, 23))
        self.downloadProgressBar.setAutoFillBackground(False)
        self.downloadProgressBar.setStyleSheet("")
        self.downloadProgressBar.setProperty("value", 0)
        self.downloadProgressBar.setTextVisible(False)
        self.downloadProgressBar.setOrientation(QtCore.Qt.Horizontal)
        self.downloadProgressBar.setInvertedAppearance(False)
        self.downloadProgressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.downloadProgressBar.setObjectName("downloadProgressBar")
        self.horizontalLayout.addWidget(self.groupBox_3)
        self.groupBox_4 = QtWidgets.QGroupBox(self.horizontalLayoutWidget)
        self.groupBox_4.setStyleSheet("background-color:#000000;")
        self.groupBox_4.setObjectName("groupBox_4")
        self.label_6 = QtWidgets.QLabel(self.groupBox_4)
        self.label_6.setGeometry(QtCore.QRect(34, 30, 141, 141))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("../../Desktop/acd_logo.jpg"))
        self.label_6.setScaledContents(True)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.groupBox_4)
        self.label_7.setGeometry(QtCore.QRect(20, 170, 171, 31))
        self.label_7.setStyleSheet("font-size : 24px;")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.groupBox_4)
        self.label_8.setGeometry(QtCore.QRect(20, 200, 171, 31))
        self.label_8.setStyleSheet("font-size : 15px;")
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.groupBox_4)
        self.label_9.setGeometry(QtCore.QRect(10, 281, 191, 20))
        self.label_9.setStyleSheet("font-size : 16px;")
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.githubButton = QtWidgets.QPushButton(self.groupBox_4)
        self.githubButton.setGeometry(QtCore.QRect(10, 240, 81, 31))
        self.githubButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.githubButton.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(228, 228, 228, 255), stop:1 rgba(255, 255, 255, 255));\n"
"color:2d2d44;\n"
"border-radius : 10px;")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("github.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.githubButton.setIcon(icon3)
        self.githubButton.setObjectName("githubButton")
        self.reportBugButton = QtWidgets.QPushButton(self.groupBox_4)
        self.reportBugButton.setGeometry(QtCore.QRect(100, 240, 101, 31))
        self.reportBugButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.reportBugButton.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(228, 228, 228, 255), stop:1 rgba(255, 255, 255, 255));\n"
"color:2d2d44;\n"
"border-radius : 10px;")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("bug.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.reportBugButton.setIcon(icon4)
        self.reportBugButton.setObjectName("reportBugButton")
        self.horizontalLayout.addWidget(self.groupBox_4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 918, 27))
        self.menubar.setObjectName("menubar")
        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName("menufile")
        self.menulinks = QtWidgets.QMenu(self.menubar)
        self.menulinks.setObjectName("menulinks")
        self.menuversion = QtWidgets.QMenu(self.menubar)
        self.menuversion.setObjectName("menuversion")
        self.menu_soroushamdg_made_it = QtWidgets.QMenu(self.menubar)
        self.menu_soroushamdg_made_it.setObjectName("menu_soroushamdg_made_it")
        self.menulanguage = QtWidgets.QMenu(self.menubar)
        self.menulanguage.setObjectName("menulanguage")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setStyleSheet("color:#f8f8f8;")
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionadd_new_link = QtWidgets.QAction(MainWindow)
        self.actionadd_new_link.setObjectName("actionadd_new_link")
        self.actionadd_new_link.setShortcut('ctrl+n')
        self.actionadd_new_link.triggered.connect(self.add_link_button)
        self.actionversion_1_0 = QtWidgets.QAction(MainWindow)
        self.actionversion_1_0.setObjectName("actionversion_1_0")
        self.actionopen_github_page = QtWidgets.QAction(MainWindow)
        self.actionopen_github_page.setObjectName("actionopen_github_page")
        self.actionexit = QtWidgets.QAction(MainWindow)
        self.actionexit.setObjectName("actionexit")
        self.actionstart_downloading = QtWidgets.QAction(MainWindow)
        self.actionstart_downloading.setObjectName("actionstart_downloading")
        self.actionstart_downloading.triggered.connect(self.start_downloading_button)
        self.actionstart_downloading.setShortcut('ctrl+m')
        self.actionopen_log_file = QtWidgets.QAction(MainWindow)
        self.actionopen_log_file.setObjectName("actionopen_log_file")
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.actionenglish = QtWidgets.QAction(MainWindow)
        self.actionenglish.setObjectName("actionenglish")
        self.menufile.addAction(self.actionexit)
        self.menulinks.addAction(self.actionadd_new_link)
        self.menulinks.addSeparator()
        self.menulinks.addAction(self.actionstart_downloading)
        self.menuversion.addAction(self.actionversion_1_0)
        self.menuversion.addSeparator()
        self.menuversion.addAction(self.actionopen_github_page)
        self.menuversion.addAction(self.actionopen_log_file)
        self.menulanguage.addAction(self.action)
        self.menulanguage.addAction(self.actionenglish)
        self.menubar.addAction(self.menufile.menuAction())
        self.menubar.addAction(self.menulinks.menuAction())
        self.menubar.addAction(self.menuversion.menuAction())
        self.menubar.addAction(self.menu_soroushamdg_made_it.menuAction())
        self.menubar.addAction(self.menulanguage.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        QtWidgets.QApplication.processEvents()
        self.selected_link_in_list = None
        # checking stages and stuff for after run.
        self.start_up()

        from backend import garson
        self.login_controller = garson.login_controller()
        self.course_object = garson.course
        self.courses = {}


    def search_and_check_for_engine(self):
        #check from settings file
        if 'driver_path' in options.options:
            back_options.driver_path = options.options['driver_path']
            try:
                from selenium.webdriver import Chrome
                from selenium.webdriver.chrome.options import Options
                opts = Options()
                opts.add_argument("--headless")
                ac_browser = Chrome(options=opts, executable_path=back_options.driver_path)
                ac_browser.quit()
                del ac_browser
                del opts
            except:
                log.log(__name__,"file saved in options doesn't work, can't run it.")
            else:
                return True
        else:
            pass

        #try to find it it self.
        try:
            open('\\'.join(os.path.realpath(__file__).split('\\')[:-2])+'\\'+'acd_engine.acde')
        except:
            log.log(__name__,"can't find acd_engine, openning dialog.")
            while(True):
                try:
                    fileName = QFileDialog.getOpenFileUrl(filter="Engine files (*.acde)")[0].url().split('///')[1]
                except:
                    self.show_message_box("error","can't open file dialog.")
                    return False
                else:
                    print(fileName)
                    if fileName == None or fileName == '' or not fileName:
                        self.show_message_box("error", "choose proper file.")
                        sys.exit()
                        continue
                    else:
                        #check if driver works
                        try:
                            from selenium.webdriver import Chrome
                            from selenium.webdriver.chrome.options import Options
                            opts = Options()
                            opts.add_argument("--headless")
                            ac_browser = Chrome(options=opts, executable_path=fileName)
                            ac_browser.quit()
                            del ac_browser
                            del opts
                        except:
                            log.log(__name__,"you chose wrong file, can't run it.")
                            self.show_message_box("error","you've selected wrong file.")
                            continue
                        else:
                            options.options['driver_path'] = fileName
                            options.save_options()
                            back_options.driver_path = fileName
                            return True
        else:
            fileName = '\\'.join(os.path.realpath(__file__).split('\\')[:-2])+'\\'+'acd_engine.acde'
            # check if driver works
            try:
                from selenium.webdriver import Chrome
                from selenium.webdriver.chrome.options import Options
                opts = Options()
                opts.add_argument("--headless")
                ac_browser = Chrome(options=opts, executable_path=fileName)
                ac_browser.quit()
                del ac_browser
                del opts
            except:
                log.log("error in launcing acd_engine.acde")
                self.show_message_box("error", "error in launcing acd_engine.acde")
                return False
            else:
                options.options['driver_path'] = fileName
                options.save_options()
                back_options.driver_path = fileName
                return True

    def load_university_database_into_combo(self):
        self.schoolsComboBox.addItems([item for item in sorted(options.urls_db.keys())])


    def select_university_by_combox(self):
        global selected_school_dict
        print(self.schoolsComboBox.currentText())
        selected_school_dict = options.urls_db[self.schoolsComboBox.currentText()]
        self.enable_disable_stages(['stage2'],[])


    def show_message_box(self,title,message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(title)
        msg.setInformativeText(message)
        msg.setWindowTitle("ADC Alert")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def openFileNameDialog(self):
        try:
            fileName = str(QFileDialog.getExistingDirectory())
        except:
            return
        else:
            if fileName == None or fileName == '':
                return

        if 'ffmpeg.exe' in os.listdir(fileName):
            options.options['ffmpeg_path'] = fileName + '/'
            options.save_options()
            self.check_stage_1()
            if ffmpeg_working:
                return True
            else:
                self.show_message_box("Couldn't run ffmpeg.exe",
                                      "Please reinstall it again.")
                return False
        else:
            self.show_message_box("Couldn't find ffmpeg.exe","Please redirect to bin folder where you can find ffmpeg.exe file.")
            return False

    #stage 1 stuff
    def check_stage_1(self):
        global database_found, ffmpeg_working, found_ffmpeg
        if 'ffmpeg_path' in options.options:
            back_options.ffmpeg_directory_bin = options.options['ffmpeg_path']
            found_ffmpeg = True
            if check_ffmpeg(back_options.ffmpeg_directory_bin,'ffmpeg -version'):
                ffmpeg_working = True
                self.enable_disable_stage_1(0)
            else:
                ffmpeg_working = False
        else:
            found_ffmpeg = False

        if options.load_database():
            database_found = True
        else:
            database_found = False

        if ffmpeg_working and found_ffmpeg and database_found:
            self.enable_disable_stages(['stage2'],['stage1','stage3'])
            self.enable_disable_stage_2(1,True)
            return True

        if any([not ffmpeg_working ,not found_ffmpeg]) and database_found:
            self.enable_disable_stages(['stage1'], ['stage2', 'stage3'])
            self.findDataBaseFileButton.setDisabled(True)
            return

        if all([not ffmpeg_working , not found_ffmpeg , not database_found]):
            self.enable_disable_stages(['stage1'], ['stage2', 'stage3'])
            return

        if all([ffmpeg_working , found_ffmpeg]) and not database_found:
            self.enable_disable_stages(['stage1'], ['stage2', 'stage3'])
            self.findFFMPEGButton.setDisabled(True)
            return

        if database_found:
            self.enable_disable_stages(['stage1'], ['stage2', 'stage3'])
            self.findDataBaseFileButton.setDisabled(True)
            return
        else:
            self.enable_disable_stages(['stage1'], ['stage2', 'stage3'])

    #stage 2 stuff
    def check_stage_2(self):
        executor.submit(self.stage2DoneButton.setText,"Logging in..")
        time.sleep(0.5)
        if not self.schoolsComboBox.currentText():
            self.show_message_box('Please choose your school','Please choose your university or school.')
            self.stage2DoneButton.setText("Login")
            return False
        if any([not self.usernameInputField.text(),not self.passwordInputField.text()]):
            self.show_message_box('Please fill in username and password', 'Please fill in username and password')
            self.stage2DoneButton.setText("Login")

            return False

        if self.schoolsComboBox.currentText() and self.usernameInputField.text() and self.passwordInputField.text():
            # login_thread = threading.Thread(target=self.login_controller.login_into_system,args=(selected_school_dict,self.usernameInputField.text(),self.passwordInputField.text()))
            QtWidgets.QApplication.processEvents()
            self.login_controller.login_into_system(selected_school_dict,self.usernameInputField.text(),self.passwordInputField.text())

            login_result = self.login_controller.logged_in

            if not login_result:
                self.show_message_box('Login failed!', 'Please check your university and username or password.')
                self.stage2DoneButton.setText("Login")
                return False
            else:
                self.show_message_box('Login successful!', 'Login was successful')
                self.enable_disable_stages(['stage3'],['stage1','stage2'])
                self.stage2DoneButton.setText("Successful")
                QtWidgets.QApplication.processEvents()
                return True
        else:
            self.show_message_box('There is something wrong:|', "can't find what:| contact me.")
            self.stage2DoneButton.setText("Login")
            return False

    #stage 3 stuff
    def add_link_to_list(self,course_link):
        if self.course_object(course_link):
            course = self.course_object(course_link)
            if course.is_link_valid:
                if course.file_name not in self.courses:
                    self.courses[course.file_name] = course
                    self.coursesList.addItem(course.file_name)
                    return True
                else:
                    self.show_message_box('Ooopsi',"You have added this link before.")
                    return False
            else:
                return False
        else:
            return False

    def add_link_button(self):
        text, okPressed = QInputDialog.getText(self,"Enter url(join-session url)", "URL:")
        if okPressed and text != '' and text:
            print(text)
            if self.add_link_to_list(text):
                self.show_message_box('Cool!','Link added successfully.')
            else:
                self.show_message_box('Error','Invalid link')
        self.check_start_download_stage()


    def selected_link_from_list(self):
        self.removeCourseLinkButton.setEnabled(True)
        self.selected_link_in_list = [item for item in self.coursesList.selectedItems()][0]
        print(self.selected_link_in_list)

    def remove_selected_item(self):
        buttonReply = QMessageBox.question(self, "ADC Alert", 'Are you sure you want to delete this link?"',
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            del self.courses[self.selected_link_in_list.text()]
            self.coursesList.takeItem(self.coursesList.row(self.selected_link_in_list))
            self.selected_link_in_list = None
            self.removeCourseLinkButton.setDisabled(True)
            QtWidgets.QApplication.processEvents()
        else:
            print('No clicked.')
        self.check_start_download_stage()

    def check_start_download_stage(self):
        if all([course.is_link_valid for course in self.courses.values()]) and self.login_controller.logged_in:
            self.startCourseButtonLink.setEnabled(True)
            self.actionstart_downloading.setEnabled(True)
            return True
        else:
            self.startCourseButtonLink.setDisabled(True)
            self.actionstart_downloading.setDisabled(True)
            return False

    def progress_percentage(self,jobs_done):
        return 100*jobs_done/(len(self.courses)*2)

    def get_and_show_downloaded_bytes(self,pre_message):
        print('getting download status.')
        while(in_downloading_process):
            QtWidgets.QApplication.processEvents()
            time.sleep(1)
            if bytes_downloaded > 1000:
                self.statusbar.showMessage(pre_message +' ' +  str(bytes_downloaded / 1000) + 'KBs downloaded')
            elif bytes_downloaded > 1000000:
                self.statusbar.showMessage(pre_message + ' ' + str(bytes_downloaded / 1000000) + 'MBs downloaded')
            elif bytes_downloaded< 1000:
                self.statusbar.showMessage(pre_message +' ' +  str(bytes_downloaded) + 'Bytes downloaded')
            else:
                self.statusbar.showMessage(pre_message +' ' +  str(bytes_downloaded / 1000000000) + 'GBs downloaded')
        else:
            if pre_message == 'clc':
                self.statusbar.clearMessage()
                return
            if pre_message:
                self.statusbar.showMessage(pre_message)

    def update_progress_bar_to_value(self,value):
        self.downloadProgressBar.setValue(int(self.progress_percentage(jobs_done=int(value))))

    def update_failsnumber_to_value(self,value):
        self.failDownloadLCDNumber.display(int(value))
    def show_finished_message_box(self,msg):
        self.show_message_box('Yohoo!',msg)

    def start_downloading_button(self):
        if self.check_start_download_stage():
            self.enable_disable_stages([], ['stage1', 'stage2', 'stage3'])
            self.downloadProgressBar.setEnabled(True)
            self.failDownloadLCDNumber.setEnabled(True)
            download_manager = download_tread(self.courses,self.check_start_download_stage())
            self.connect(download_manager, QtCore.SIGNAL("finished()"), self.clean_up_after_download)
            QtGui.QMain
    def clean_up_after_download(self):
        for course in self.courses.values():
            try:
                course.clear_cache_and_data()
            except:
                log.log(__name__,'error in cleaning cache.')
        self.failDownloadLCDNumber.display(0)
        self.courses.clear()
        self.coursesList.clear()
        self.downloadProgressBar.setValue(0)
        self.enable_disable_stages(['stage3'],['stage1','stage2'])
        QtWidgets.QApplication.processEvents()

    def start_up(self):
        self.check_stage_1()
        if not self.search_and_check_for_engine():
            sys.exit()
        else:
            log.log(__name__,'Driver launched and found successfully.')

        #fill combobox
        self.load_university_database_into_combo()

    def enable_disable_stage_1(self,toggle):
        if toggle == 1:
            self.findFFMPEGButton.setEnabled(True)
            self.findDataBaseFileButton.setEnabled(True)
            self.stage1DoneButton.setEnabled(True)
        else:
            self.findFFMPEGButton.setDisabled(True)
            self.findDataBaseFileButton.setDisabled(True)
            self.stage1DoneButton.setDisabled(True)

    def enable_disable_stage_2(self,toggle,stage_one_complete=False):
        if toggle == 1:
            self.schoolsComboBox.setEnabled(True)
            if stage_one_complete:
                self.usernameInputField.setEnabled(True)
                self.passwordInputField.setEnabled(True)
                self.stage2DoneButton.setEnabled(True)
        else:
            self.schoolsComboBox.setDisabled(True)
            self.usernameInputField.setDisabled(True)
            self.passwordInputField.setDisabled(True)
            self.stage2DoneButton.setDisabled(True)

    def enable_disable_stage_3(self,toggle):
        if toggle == 1:
            self.addCoursesLinkButton.setEnabled(True)
            self.coursesList.setEnabled(True)
            self.actionadd_new_link.setEnabled(True)
        else:
            self.addCoursesLinkButton.setDisabled(True)
            self.actionadd_new_link.setDisabled(True)
            self.actionstart_downloading.setDisabled(True)
            self.coursesList.setDisabled(True)
            self.downloadProgressBar.setDisabled(True)
            self.failDownloadLCDNumber.setDisabled(True)
            self.startCourseButtonLink.setDisabled(True)
            self.removeCourseLinkButton.setDisabled(True)

    def enable_disable_stages(self,enable,disable):
        if 'stage1' in enable:
            self.enable_disable_stage_1(1)

        if 'stage2' in enable:
            self.enable_disable_stage_2(1)

        if 'stage3' in enable:
            self.enable_disable_stage_3(1)

        if 'stage1' in disable:
            self.enable_disable_stage_1(0)

        if 'stage2' in disable:
            self.enable_disable_stage_2(0)

        if 'stage3' in disable:
            self.enable_disable_stage_3(0)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ACD - 1.0"))
        self.groupBox.setTitle(_translate("MainWindow", "stage 1"))
        self.label.setText(_translate("MainWindow", "1. Install FFMPEG"))
        self.findFFMPEGButton.setText(_translate("MainWindow", "find the folder"))
        self.label_2.setText(_translate("MainWindow", "2. ADC-WDB"))
        self.findDataBaseFileButton.setText(_translate("MainWindow", "find the file"))
        self.stage1DoneButton.setText(_translate("MainWindow", "Done"))
        self.groupBox_2.setTitle(_translate("MainWindow", "stage 2"))
        self.label_3.setText(_translate("MainWindow", "1. Choose your school"))
        self.label_4.setText(_translate("MainWindow", "2. Enter username and password"))
        self.usernameInputField.setPlaceholderText(_translate("MainWindow", "username"))
        self.passwordInputField.setPlaceholderText(_translate("MainWindow", "password"))
        self.stage2DoneButton.setText(_translate("MainWindow", "Login"))
        self.requestSchoolButton.setText(_translate("MainWindow", "request your school"))
        self.groupBox_3.setTitle(_translate("MainWindow", "stage 3"))
        self.addCoursesLinkButton.setText(_translate("MainWindow", "+"))
        self.removeCourseLinkButton.setText(_translate("MainWindow", "-"))
        self.startCourseButtonLink.setText(_translate("MainWindow", "start"))
        self.label_5.setText(_translate("MainWindow", "failed :"))
        self.downloadProgressBar.setFormat(_translate("MainWindow", "%p%"))
        self.groupBox_4.setTitle(_translate("MainWindow", "about ACD"))
        self.label_7.setText(_translate("MainWindow", "ACD"))
        self.label_8.setText(_translate("MainWindow", "version 1.0"))
        self.label_9.setText(_translate("MainWindow", "@soroushamdg made it."))
        self.githubButton.setText(_translate("MainWindow", "github"))
        self.reportBugButton.setText(_translate("MainWindow", "report"))
        self.menufile.setTitle(_translate("MainWindow", "file"))
        self.menulinks.setTitle(_translate("MainWindow", "links"))
        self.menuversion.setTitle(_translate("MainWindow", "expert"))
        self.menu_soroushamdg_made_it.setTitle(_translate("MainWindow", ""))
        self.menulanguage.setTitle(_translate("MainWindow", "language"))
        self.actionadd_new_link.setText(_translate("MainWindow", "add new link"))
        self.actionversion_1_0.setText(_translate("MainWindow", "version 1.0"))
        self.actionopen_github_page.setText(_translate("MainWindow", "open github page"))
        self.actionexit.setText(_translate("MainWindow", "exit"))
        self.actionstart_downloading.setText(_translate("MainWindow", "start downloading"))
        self.actionopen_log_file.setText(_translate("MainWindow", "open log file"))
        self.action.setText(_translate("MainWindow", "فارسی"))
        self.actionenglish.setText(_translate("MainWindow", "english"))


    def change_translation_to_english(self):
        options.options['selected_language'] = "en"
        self.retranslateUi()

    def change_translation_to_farsi(self):
        options.options['selected_language'] = "fa"
        self.retranslateUi()


class download_tread(QtCore.QThread):
    def __init__(self,_to_download_list,download_checked):
        self.courses = _to_download_list
        self.check_start_download_stage = download_checked
        QtCore.QThread.__init__(self)

    def __del__(self):
        self.wait()


    def start_download(self):
        global in_downloading_process
        time.sleep(0.5)
        if self.check_start_download_stage():
            jobs_done = 0
            failed = 0
            to_download_list = list(self.courses.values())
            for i in range(len(to_download_list) + 1):
                threads = []

                # add jobs to threads
                if i == 0:
                    t_download = threading.Thread(target=to_download_list[i].download_course)
                    threads.append(t_download)
                    msg = f'Downloading {to_download_list[i].file_name}'

                    in_downloading_process = True
                    self.emit(QtCore.SIGNAL('get_and_show_downloaded_bytes(QString)'), msg)

                    # to_download_list[i].download_course()
                elif i == len(to_download_list):
                    t_extract = threading.Thread(target=to_download_list[i - 1].extract_course)
                    msg = f'Extracting {to_download_list[i - 1].file_name}'
                    in_downloading_process = False
                    self.emit(QtCore.SIGNAL('get_and_show_downloaded_bytes(QString)'), msg)
                    threads.append(t_extract)
                    # to_download_list[i-1].extract_course()
                else:
                    t_download = threading.Thread(target=to_download_list[i].download_course)
                    threads.append(t_download)
                    t_extract = threading.Thread(target=to_download_list[i - 1].extract_course)
                    threads.append(t_extract)
                    msg = f'Downloading {to_download_list[i].file_name} + Extracting {to_download_list[i - 1].file_name}'
                    self.emit(QtCore.SIGNAL('get_and_show_downloaded_bytes(QString)'), msg)

                log.log(__name__, f'added jobs to threads. round {i + 1}')
                # starting threads
                for thread in threads:
                    thread.start()

                # waiting to finish

                for thread in threads:
                    thread.join()

                self.emit(QtCore.SIGNAL('get_and_show_downloaded_bytes(QString)'), 'clc')

                # checking which is done which not.
                if i == 0:
                    if to_download_list[i].downloaded:
                        jobs_done += 1
                    else:
                        failed += 1
                elif i == len(to_download_list):
                    if to_download_list[i - 1].downloaded and to_download_list[i - 1].extracted:
                        jobs_done += 2
                    elif to_download_list[i - 1].downloaded and not to_download_list[i - 1].extracted:
                        failed += 1
                    else:
                        pass
                else:
                    if to_download_list[i].downloaded:
                        jobs_done += 1
                    if to_download_list[i - 1].downloaded and to_download_list[i - 1].extracted:
                        jobs_done += 2
                    elif to_download_list[i - 1].downloaded and not to_download_list[i - 1].extracted:
                        failed += 1
                    else:
                        pass

                self.emit(QtCore.SIGNAL('update_progress_bar_to_value(QString)'), str(jobs_done))
                self.emit(QtCore.SIGNAL('update_failsnumber_to_value(QString)'), str(failed))

            in_downloading_process = False
            self.emit(QtCore.SIGNAL('show_finished_message_box(QString)'), str(failed))
            self.emit(QtCore.SIGNAL('update_failsnumber_to_value(QString)'), str(failed))
            self.emit(QtCore.SIGNAL('show_finished_message_box(QString)'), str(f'{len(to_download_list) - failed} course(s) download and extracting finished!'))

            return

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    def exit_app():
        app.exec_()
        log.log(__name__, "Application closed.")
        log.close_file()

    sys.exit(exit_app())
