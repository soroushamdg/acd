from app import *
import sys
from menuDetails import appinfo, expert, help


class Main(QtWidgets.QMainWindow):

    def setMenuBarInformation(self):
        #          SET APP MENU BAR INFO
        self.ui.appVersion.setText("v" + appinfo.VERSION)
        self.ui.actionACD_v2.setText("ACD v" + appinfo.VERSION)
        self.ui.actionBuildNumber.setText(f"Build {appinfo.BUILD_NUMBER}")
        self.ui.actionEngineVersion.setText(f"Engine v{appinfo.ENGINE_VERSION}")
        self.ui.actionOS.setText(f"OS : {expert.running_platform}\n{expert.system}\n{expert.architect}")
        self.ui.actionCPU.setText(f"CPU : {expert.processor}")

    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setMenuBarInformation()






if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = Main()
    myapp.show()
    sys.exit(app.exec_())