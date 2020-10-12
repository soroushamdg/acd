from app import *
import sys
from menuBar import appinfo, expert, help
from courseExtraFileDownloadDialog import courseExtraFileDownloadDialog
from welcomeScreenDialog import welcomeScreenDialog
class Main(QtWidgets.QMainWindow):

    def setMenuBarInformation(self):
        #          SET APP MENU BAR INFO
        self.ui.appVersion.setText("v" + appinfo.VERSION)
        self.ui.actionACD_v2.setText("ACD v" + appinfo.VERSION)
        self.ui.actionBuildNumber.setText(f"Build {appinfo.BUILD_NUMBER}")
        self.ui.actionEngineVersion.setText(f"Engine v{appinfo.ENGINE_VERSION}")
        self.ui.actionOS.setText(f"OS : {expert.running_platform}\n{expert.system}\n{expert.architect}")
        self.ui.actionCPU.setText(f"CPU : {expert.processor}")
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

    def showdialog(self):
        dialog = courseExtraFileDownloadDialog.Ui_courseExtraFilesDownloadTypeDialog(parent=self)
        res = dialog.exec_()
        print(res)

    def showwelcomedialog(self):
        dialog = welcomeScreenDialog.Ui_welcomeScreenDialog(parent=self)
        dialog.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = Main()
    myapp.show()
    myapp.showwelcomedialog()
    myapp.showdialog()
    sys.exit(app.exec_())