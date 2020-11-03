import pickle
import winsound
from time import sleep

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox

import settings
from app import *
import sys
from menuBar import appinfo, expert, help,clearcache
from downloadACDialog import downloadACDialog
from mainThreads import startupConfigurations, acManager
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from clearbuffer import clear_buffer

# CONFIGURE LOGGING
import logging
# logging.basicConfig(filename=settings.SETTINGS['LOG_PATH'],filemode='w',level=logging.DEBUG,datefmt='%d-%b-%y %H:%M:%S',format="%(levelname)s -- %(asctime)s -- %(name)s -- %(message)s")

class Main(QtWidgets.QMainWindow):
    driver1 = None
    acBrowser = None

    def reset_program(self):
        expert.reset_program()
        sys.exit()

    def setMenuBarInformation(self):
        # SET CLEAR CACHE MENU ACTION
        self.ui.actionClear_cache.triggered.connect(clearcache.clearcache)
        #          SET APP MENU BAR INFO
        self.ui.appVersion.setText("v" + appinfo.VERSION)
        self.ui.actionACD_v2.setText("ACD v" + appinfo.VERSION)
        self.ui.actionBuildNumber.setText(f"Build {appinfo.BUILD_NUMBER}")
        self.ui.actionEngineVersion.setText(f"Engine v{appinfo.ENGINE_VERSION}")
        self.ui.actionOS.setText(f"OS : {expert.running_platform}\n{expert.system}\n{expert.architect}")
        self.ui.actionCPU.setText(f"CPU : {expert.processor}")
        self.ui.actionReset.triggered.connect(self.reset_program)
        # SET APP "HELP" MENU ACTIONS
        self.ui.actionAparatHelpMenu.triggered.connect(help.open_aparat_link)
        self.ui.actionYoutubeHelpMenu.triggered.connect(help.open_youtube_link)
        self.ui.actionVirgoolHelpMenu.triggered.connect(help.open_virgool_link)
        self.ui.actionTelegramHelpMenu.triggered.connect(help.open_telegram_link)
        self.ui.actionContactDeveloperHelpMenu.triggered.connect(help.open_contact_developer_link)

    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setMenuBarInformation()
        self.startupConfiguration()
        QtWidgets.QApplication.processEvents()
        self.ac_disable_all_buttons_except_login()

        # ADOBE CONNECT QUEUE MANAGER
        self.acQueueList = acManager.acQueueManager()

    def startupConfiguration(self):
        startupConfigurationTaskThread = startupConfigurations.StartupConfigurationThread(parent=self)
        startupConfigurationTaskThread.run()

    def showdialog(self):
        dialog = downloadACDialog.Ui_downloadACDialog(parent=self,acBrowser=None,acQueueList=None)
        print('shown dialog')
        res = dialog.exec_()
        print(res)

    def raise_dialog(self,title,message,description,needretry=False):
        try:
            msg = QMessageBox(self)
            msg.setText(message)
            msg.setInformativeText(description)
            msg.setWindowTitle(title)
            if needretry:
                self.raise_errorflag()
                msg.setStandardButtons(QMessageBox.Retry | QMessageBox.Cancel)
                self.downloadTaskThread.quit()
                self.downloadTaskThread.terminate()
                self.downloadTaskThread.wait()
            else:
                msg.setStandardButtons(QMessageBox.Close)
                self.downloadTaskThread.quit()
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

    # ADOBE CONNECT TAB
    def ac_disable_all_buttons_except_login(self):
        self.ui.acCourseURLInput.setDisabled(True)
        try:
            self.ui.acLoginButton.clicked.disconnect()
        except:
            pass
        self.ui.acLoginButton.clicked.connect(self.ac_login_button_login_action)
        try:
            self.ui.actionLogin.triggered.disconnect()
        except:
            pass
        self.ui.actionLogin.triggered.connect(self.ac_login_button_login_action)
        self.ui.acFileNameInput.setDisabled(True)
        self.ui.acMergeFilesCheckBox.setDisabled(True)
        self.ui.acAddToQueueButton.setDisabled(True)
        self.ui.acRemoveFromQueueButton.setDisabled(True)
        self.ui.acStartQueueButton.setDisabled(True)
        self.ui.actionStart.setDisabled(True)

    def ac_login_awaiting(self):
        self.ui.acLoginButton.setText('Catch')
        self.ui.actionLogin.setText('Catch Adobe Connect')
        try:
            self.ui.acLoginButton.clicked.disconnect()
        except:
            pass
        self.ui.acLoginButton.clicked.connect(self.ac_login_button_await_action)

        try:
            self.ui.actionLogin.triggered.disconnect()
        except:
            pass
        self.ui.actionLogin.triggered.connect(self.ac_login_button_await_action)

        QtWidgets.QApplication.processEvents()



    def ac_login_succesfull(self):
        self.ui.acLoginButton.setText('OK!')
        self.ui.acLoginButton.setDisabled(True)
        self.ui.actionLogin.setDisabled(True)
        self.ui.acLoginStatusLabel.setEnabled(True)
        self.ui.acCourseURLInput.setDisabled(False)
        self.ui.acFileNameInput.setDisabled(False)
        self.ui.acMergeFilesCheckBox.setDisabled(False)
        self.ui.acAddToQueueButton.setDisabled(False)

    def ac_login_failed(self):
        self.ac_disable_all_buttons_except_login()
        self.ui.acLoginButton.setText('Login')
        self.ui.actionLogin.setText('Login Adobe Connect')
        try:
            self.ui.acLoginButton.clicked.disconnect()
        except:
            pass
        self.ui.acLoginButton.clicked.connect(self.ac_login_button_login_action)
        self.ui.acLoginButton.setDisabled(False)
        self.ui.acLoginStatusLabel.setEnabled(False)

    def ac_login_button_login_action(self):
        opts = Options()
        opts.add_argument("--disable-notifications")
        # opts.add_argument("user-data-dir=cachedD")
        opts.add_argument("--no-sandbox")
        self.driver1 = Chrome(options=opts, executable_path=settings.SETTINGS['ACD_ENGINE_PATH'])
        clear_buffer()
        self.driver1.get('https://google.com')
        self.ac_login_awaiting()
        QtWidgets.QApplication.processEvents()

    def ac_login_button_await_action(self):
        try:
            waitMessage = QMessageBox()
            waitMessage.setText("Catching")
            waitMessage.setInformativeText("Please wait...")
            waitMessage.setWindowTitle("Catching")
            waitMessage.setStandardButtons(QMessageBox.Ok)
            waitMessage.setDisabled(True)
            waitMessage.show()
            QtWidgets.QApplication.processEvents()
        except Exception as msg:
            print(msg)

        try:
            pickle.dump(self.driver1.get_cookies(), open(settings.SETTINGS['ENGINE_COOKIE_PATH'], 'wb'))
            self.acLoginActionCurrentURL = self.driver1.current_url
            self.acLoginActionCurrentTitle = self.driver1.title
            self.driver1.close()
            self.driver1.quit()
        except Exception as msg:
            print(msg)
        sleep(1)
        try:
            opts = Options()
            opts.add_argument("--headless")
            opts.add_argument("--disable-notifications")
            opts.add_argument('--no-sandbox')
            opts.add_argument('--verbose')
            opts.add_argument('--disable-logging')
            opts.add_experimental_option("prefs", {
                "download.default_directory": settings.SETTINGS['ENGINE_DUMP_PATH'],
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing_for_trusted_sources_enabled": False,
                "safebrowsing.enabled": False
            })
            opts.add_argument('--disable-gpu')
            opts.add_argument('--disable-software-rasterizer')
            self.acBrowser = Chrome(options=opts, executable_path=settings.SETTINGS['ACD_ENGINE_PATH'])
        except Exception as msg:
            print(msg)
        clear_buffer()
        self.acBrowser.get(self.acLoginActionCurrentURL)
        self.acBrowser.delete_all_cookies()
        for cookie in pickle.load(open(settings.SETTINGS['ENGINE_COOKIE_PATH'], 'rb')):
            self.acBrowser.add_cookie(cookie)

        self.acBrowser.get(self.acLoginActionCurrentURL)

        if self.acBrowser.title == self.acLoginActionCurrentTitle and self.acBrowser.current_url == self.acLoginActionCurrentURL:
            self.ac_login_succesfull()
            winsound.PlaySound("*", winsound.SND_ALIAS)
        else:
            self.acBrowser.close()
            self.acBrowser.quit()
            self.ac_login_failed()
        waitMessage.close()
        return

    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"
        try:
            reply = QMessageBox()
            reply.setText(quit_msg)
            reply.setIcon(QMessageBox.Question)
            reply.setWindowTitle("Exit ACD")
            reply.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            reply = reply.exec_()
        except Exception as msg:
            print(msg)
        if reply == QMessageBox.Yes:
            try:
                self.acBrowser.close()
                self.acBrowser.quit()
            except:
                pass
            event.accept()

        else:
            event.ignore()

if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        myapp = Main()
        myapp.show()

        sys.exit(app.exec_())
    except Exception as msg:
        logging.debug(msg)
        sys.exit()