from PyQt5 import QtCore, QtGui, QtWidgets

from catchingScreenDialog import catchingScreenDialog


class catchDialogThread(QtCore.QThread):
    CONTINUE = True

    def __init__(self,dialog_parent):
        QtCore.QThread.__init__(self)
        self.catchingDialog = catchingScreenDialog.Ui_catchingScreenDialog(parent = dialog_parent)

    def __del__(self):
        self.wait()

    def run(self):
        while(self.CONTINUE):
            print('showing dialog')
            self.catchingDialog.exec_()
