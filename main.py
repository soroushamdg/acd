from app import *
import sys



class Main(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)








if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = Main()
    myapp.show()
    sys.exit(app.exec_())