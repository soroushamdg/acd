import pickle
from time import sleep

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox, QInputDialog

import settings
from app import *
import sys
from menuBar import appinfo, expert, help,clearcache
from downloadACDialog import downloadACDialog
from mainThreads import startupConfigurations, acManager
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from clearbuffer import clear_buffer
from shiftIO import shiftioThread
# CONFIGURE LOGGING
import logging
logging.basicConfig(filename=settings.SETTINGS['LOG_PATH'],filemode='a',level=logging.INFO,datefmt='%d-%b-%y %H:%M:%S',format="%(levelname)s -- %(asctime)s -- %(name)s -- %(message)s")
import tldextract
tldextract.extract('https://google.com')
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
        self.ui.actionConvert_Threads_60.setText(f"Output bitrate : {settings.return_output_bitrate()}")
        self.ui.actionOutputFileType.setText(f"Output file format : {settings.return_output_format()}")
        self.ui.actionConvert_Threads_60.triggered.connect(self.menu_bar_set_ac_output_bitrate)
        self.ui.actionOutputFileType.triggered.connect(self.menu_bar_set_ac_output_format)
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
        self.shiftio_prepare_before_run()
        # ADOBE CONNECT QUEUE MANAGER
        self.acQueueList = acManager.acQueueManager()
        self.ui.acAddToQueueButton.clicked.connect(self.ac_add_to_queue_button_action)
        self.ui.acQueueListView.clicked.connect(self.ac_selected_item_from_list)
        self.ui.acRemoveFromQueueButton.clicked.connect(self.ac_remove_from_queue_button_action)
        self.ui.actionStart.triggered.connect(self.ac_start_download_action)
        self.ui.acStartQueueButton.clicked.connect(self.ac_start_download_action)

    def menu_bar_set_ac_output_bitrate(self):
        options_plain = ("30k",
                   "60k",
                   "90k",
                   "120k",
                   "150k",
                   "250k",
                   "500k",
                   "750k",
                   "1000k",
                   "1200k",
                   "1500k",
                   )
        options = ("30k - Weak",
                   "60k - Good (~=15 minutes to process in MKV)",
                   "90k - Better (~=16 minutes to process in MKV)",
                   "120k - Very good (~=17 minutes to process in MKV)",
                   "150k",
                   "250k",
                   "500k",
                   "750k",
                   "1000k",
                   "1200k",
                   "1500k",
                   )
        item, ok = QInputDialog.getItem(self,
                                       "Output bitrate",
                                        "Select outputs bitrate in list below. Higher bitrates take longer to process!",
                                        options, options_plain.index(settings.return_output_bitrate()), False)
        if ok and item:
            settings.set_output_bitrate(str(item.split("-")[0].rstrip()))
            self.ui.actionConvert_Threads_60.setText(f"Output bitrate : {settings.return_output_bitrate()}")

    def menu_bar_set_ac_output_format(self):
        options_plain = ("mp4",
                   "mkv")
        options = ("mp4 - Fast",
                   "mkv - Faster but usually FAILS!")
        item, ok = QInputDialog.getItem(self,
                                        "Output File Formant",
                                        "Please select oupputs file format from list below. Performance may change.",
                                        options, options_plain.index(settings.return_output_format()), False)
        if ok and item:
            settings.set_output_format(str(item.split("-")[0].rstrip()))
            self.ui.actionOutputFileType.setText(f"Output file format : {settings.return_output_format()}")

    def startupConfiguration(self):
        startupConfigurationTaskThread = startupConfigurations.StartupConfigurationThread(parent=self)
        startupConfigurationTaskThread.run()

    def raise_error_dialog(self,title,message,description=None):
        try:
            msg = QMessageBox()
            msg.setText(message)
            msg.setIcon(QMessageBox.Critical)
            if description:
                msg.setInformativeText(description)
            msg.setWindowTitle(title)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
        except Exception as msg:
            logging.debug('error'+msg)

    # AC ADOBE CONNECT TAB

    # AC STAGE 1 : LOGIN
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
            pickle.dump(self.driver1.get_cookies(), open(settings.engine_cookie_path(), 'wb'))
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
        attempts = 0
        while(attempts != 3):
            try:
                self.acBrowser.get(self.acLoginActionCurrentURL)
                self.acBrowser.delete_all_cookies()
                for cookie in pickle.load(open(settings.engine_cookie_path(), 'rb')):
                    self.acBrowser.add_cookie(cookie)

                self.acBrowser.get(self.acLoginActionCurrentURL)
            except:
                clear_buffer()
                attempts += 1
                pass
            else:
                clear_buffer()
                break
        else:
            self.acBrowser.close()
            self.acBrowser.quit()
            self.ac_login_failed()

        if self.acBrowser.title == self.acLoginActionCurrentTitle and self.acBrowser.current_url == self.acLoginActionCurrentURL:
            self.ac_login_succesfull()
        else:
            self.acBrowser.close()
            self.acBrowser.quit()
            self.ac_login_failed()
        waitMessage.close()
        return

    # AC STAGE 2 : QUEUE CONTROLLER
    def ac_start_queue_status(self,enable):
        if enable:
            self.ui.acStartQueueButton.setEnabled(True)
            self.ui.actionStart.setEnabled(True)
        else:
            self.ui.acStartQueueButton.setEnabled(False)
            self.ui.actionStart.setEnabled(False)

    def ac_clear_inputs(self):
        self.ui.acCourseURLInput.clear()
        self.ui.acFileNameInput.clear()
        self.ui.acMergeFilesCheckBox.setChecked(False)

    def ac_clear_ui_queue_list(self):
        self.ui.acQueueListView.clear()

    def ac_update_ui_queue_list(self):
        self.ac_clear_ui_queue_list()
        items = self.acQueueList.return_queue_list_filenames(True)
        if items:
            for index, item in items:
                self.ui.acQueueListView.addItem(f'{index+1} - {item}')
            self.ac_start_queue_status(enable=True)
            return
        else:
            self.ac_start_queue_status(enable=False)

    def ac_check_and_return_input_values(self):
        if self.ui.acCourseURLInput.text() and self.ui.acFileNameInput.text():
            return self.ui.acCourseURLInput.text(), self.ui.acFileNameInput.text()

    def ac_add_item_to_queue_manager(self, downloadassets = False):
        status = self.acQueueList.add_to_queue(course_url= self.ui.acCourseURLInput.text(),
                                      filename= self.ui.acFileNameInput.text(),
                                      merge_files= self.ui.acMergeFilesCheckBox.isChecked(),
                                      download_assets= downloadassets)
        if status == "DUPLICATE":
            self.raise_error_dialog('Duplicated item','Please enter different URL and filename.')

    def ac_add_to_queue_button_action(self):
        try:
            course_url, filename = self.ac_check_and_return_input_values()
        except Exception as msg:
            logging.debug(msg)
            logging.error('Error happened in getting input information.')
            self.raise_error_dialog('Error happend','Please check your inputs or restart the program.')
            self.ac_clear_inputs()
            return

        try:
            assert acManager.validate_input_url(loginurl=self.acLoginActionCurrentURL,courseurl=course_url),f'URL is not valid. {self.acLoginActionCurrentURL} != {course_url}'
        except Exception as msg:
            logging.debug(msg)
            logging.error(f'URL is not valid. {self.acLoginActionCurrentURL} != {course_url}')
            self.raise_error_dialog('Course URL not valid',f"Your course url should be on same domain.\nLogged into : {acManager.return_domain(self.acLoginActionCurrentURL)}\nCourse domain : {acManager.return_domain(course_url)}")
            self.ac_clear_inputs()
            return

        try:
            assert not acManager.check_if_filename_exists(filename=filename),f'File name already exists in exports folder. \nName : {filename}'
        except Exception as msg:
            logging.debug(msg)
            logging.error(f'File name already exists in exports folder. -> {filename}')
            self.raise_error_dialog('File already exists',f'File name already exists in exports folder. -> {filename}')
            self.ac_clear_inputs()
            return

        merge_files = self.ui.acMergeFilesCheckBox.isChecked()

        msg = QMessageBox()
        msg.setText('Download course assets?')
        msg.setIcon(QMessageBox.Question)
        msg.setInformativeText('Course assets are files that Hosts uploaded during meetings.\n (mp4, pdf supported.)')
        msg.setWindowTitle('Download Assets?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)
        downloadAssets = True if msg.exec() == QMessageBox.Yes else False

        try:
            self.ac_add_item_to_queue_manager(downloadassets=downloadAssets)
        except Exception as msg:
            logging.debug(msg)
            logging.error(f'Error in adding item to queue manager -> {course_url} | {filename}')
            self.raise_error_dialog('Error in adding item', f'Please check your inputs and try again.')
            self.ac_clear_inputs()
            return
        else:
            self.ac_update_ui_queue_list()
            self.ac_clear_inputs()

    def ac_selected_item_from_list(self):
        self.ui.acRemoveFromQueueButton.setEnabled(True)
        self.selected_link_in_list = self.ui.acQueueListView.currentItem().text()

    def ac_remove_from_queue_button_action(self):
        if self.selected_link_in_list:
            buttonReply = QMessageBox()
            buttonReply.setText("Remove course from Queue")
            buttonReply.setIcon(QMessageBox.Question)
            buttonReply.setInformativeText(
                'Are you sure you want to remove this item from queue?')
            buttonReply.setWindowTitle('Remove Item')
            buttonReply.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            buttonReply.setDefaultButton(QMessageBox.No)
            buttonReply = buttonReply.exec_()
            if buttonReply == QMessageBox.Yes:
                try:
                    index, filename = [item.replace(" ","") for item in str(self.selected_link_in_list).split('-')]
                    try:
                        index = int(index)
                        self.acQueueList.remove_from_queue(filename=filename,index=int(index)-1)
                    except:
                        self.acQueueList.remove_from_queue(filename=filename)

                    self.acQueueList.remove_from_queue(filename=filename,index=int(index)-1)
                    self.selected_link_in_list = None
                    self.ui.acRemoveFromQueueButton.setDisabled(True)
                    self.ac_update_ui_queue_list()
                except Exception as msg:
                    print(msg)
            else:
                print(3)
                self.selected_link_in_list = None
                return

    def ac_cleanup_after_download_dialog_close(self):
        self.ac_clear_inputs()
        self.ac_clear_ui_queue_list()
        self.acQueueList.queue_list.clear()
        self.ac_update_ui_queue_list()

    # AC STAGE 3 : QUEUE DOWNLOAD
    def ac_start_download_action(self):
        try:
            dialog = downloadACDialog.Ui_downloadACDialog(parent=self,acBrowser=self.acBrowser,acQueueListManager=self.acQueueList)
            res = dialog.exec_()
        except Exception as msg:
            print(msg)
        if dialog.retstatus == 'CANCEL':
            pass
        elif dialog.retstatus == 'COMPLETED':
            self.ac_cleanup_after_download_dialog_close()

    # SHIFT IO CONTROLLER
    def shiftio_prepare_before_run(self):
        self.ui.shiftIOIPAddressLabel.setText('Disconnected')
        try:
            self.ui.shiftIOStartButton.clicked.disconnect()
        except:
            pass
        self.ui.shiftIOStartButton.clicked.connect(self.shiftio_run_server)
        self.ui.shiftIOStartButton.setText('Start')
        self.ui.shiftIOStartButton.setEnabled(True)
        self.ui.shiftIOStatusLabel.setDisabled(True)

    def shiftio_thread_finished(self):
        pass

    def shiftio_run_server(self):
        self.ui.shiftIOStartButton.setText('Starting')
        self.ui.shiftIOStartButton.setEnabled(False)
        self.shiftIOControllerThread = shiftioThread.shiftIOServerThread()
        self.shiftIOControllerThread.finished.connect(self.shiftio_thread_finished)
        self.shiftIOControllerThread.start()
        sleep(1)
        if not self.shiftIOControllerThread.status:
            self.shiftIOControllerThread.stop_server()
            self.shiftIOControllerThread.quit()
            self.shiftIOControllerThread.terminate()
            self.shiftIOControllerThread.wait()
            self.shiftio_run_failed()
        else:
            self.shiftio_run_success()

    def shiftio_run_success(self):
        self.ui.shiftIOIPAddressLabel.setText(self.shiftIOControllerThread.main_ip+':'+str(self.shiftIOControllerThread.port))
        try:
            self.ui.shiftIOStartButton.clicked.disconnect()
        except:
            pass
        self.ui.shiftIOStartButton.clicked.connect(self.shiftio_stop_server)
        self.ui.shiftIOStartButton.setText('Stop')
        self.ui.shiftIOStartButton.setEnabled(True)
        self.ui.shiftIOStatusLabel.setEnabled(True)

        msg = QMessageBox()
        msg.setText('Shift I/O Started!')
        servers = f"\n".join([f"{add}:{self.shiftIOControllerThread.port}" for add in self.shiftIOControllerThread.ip_addresses]+[f"{self.shiftIOControllerThread.hostname}:{self.shiftIOControllerThread.port}"])
        msg.setInformativeText('You can connect to Shift I/O by below addresses :\n\n'+
                               servers+
                               '\n\n If you had problem connecting, please turn off your firewall.')
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Shift I/O Engine started")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def shiftio_run_failed(self):
        self.shiftio_prepare_before_run()

        msg = QMessageBox()
        msg.setText('Failed to start Shift I/O engine.')
        msg.setInformativeText('Please check your firewall and try again.')
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Shift I/O Engine failed")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def shiftio_stop_server(self):
        try:
            self.shiftIOControllerThread.stop_server()
            self.shiftIOControllerThread.quit()
            self.shiftIOControllerThread.terminate()
            self.shiftIOControllerThread.wait()
        except:
            pass
        else:
            self.shiftio_prepare_before_run()

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
                self.driver1.close()
                self.driver1.quit()
            except:
                pass
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
        # myapp.showdialog()

        sys.exit(app.exec_())
        sys.exit()
    except Exception as msg:
        logging.debug(msg)
        print(msg)
        sys.exit()