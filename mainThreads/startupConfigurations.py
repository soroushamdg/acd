import sys

from PyQt5 import QtCore
from qtpy import QtWidgets

import settings,exeinfo
from welcomeScreenDialog import welcomeScreenDialog
from downloadEngineDialog import downloadEngineDialog,engineVersionCheck

class StartupConfigurationThread():
    def __init__(self,parent):
        self.parent = parent

    def showWelcomeDialog(self):
        dialog = welcomeScreenDialog.Ui_welcomeScreenDialog(parent=self.parent)
        with open('changelog.txt','r') as changestext:
            dialog.changesLogTextEdit.setPlainText(str(changestext.read()))
        dialog.exec_()
        QtWidgets.QApplication.processEvents()
        return dialog.retstatus

    def showEngineDownloaderDialog(self):
        dialog = downloadEngineDialog.Ui_downloadEngineDialog(parent=self.parent)
        dialog.exec_()
        QtWidgets.QApplication.processEvents()
        return dialog.retstatus

    def run(self):
        if exeinfo.BUILD_NUMBER > settings.ret_buildnumber() or not settings.settings_file_exists():
            # Show Welcome and Configuration Dialog.
            status = self.showWelcomeDialog()
            if status != 'COMPLETED':
                sys.exit()
        QtWidgets.QApplication.processEvents()
        if engineVersionCheck.needs_new_engine_download():
            # Show Engine Downloader and Configuration Dialog.
            status = self.showEngineDownloaderDialog()
            if status != 'COMPLETED':
                sys.exit()
        return