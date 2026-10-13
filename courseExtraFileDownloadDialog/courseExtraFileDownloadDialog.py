# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Design\qtDesigner\courseDownloadFilesTypeDialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_courseExtraFilesDownloadTypeDialog(QtWidgets.QDialog):
    def __init__(self,parent):
        super(Ui_courseExtraFilesDownloadTypeDialog, self).__init__(parent)
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setObjectName("courseExtraFilesDownloadTypeDialog")
        self.resize(432, 273)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(432, 273))
        self.setMaximumSize(QtCore.QSize(432, 273))
        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 411, 251))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pdfCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pdfCheckBox.setFont(font)
        self.pdfCheckBox.setObjectName("pdfCheckBox")
        self.verticalLayout.addWidget(self.pdfCheckBox)
        self.mp4CheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.mp4CheckBox.setFont(font)
        self.mp4CheckBox.setObjectName("mp4CheckBox")
        self.verticalLayout.addWidget(self.mp4CheckBox)
        self.mp4FileNameInput = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.mp4FileNameInput.setEnabled(False)
        self.mp4FileNameInput.setObjectName("mp4FileNameInput")
        self.verticalLayout.addWidget(self.mp4FileNameInput)
        self.customFileCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.customFileCheckBox.setFont(font)
        self.customFileCheckBox.setObjectName("customFileCheckBox")
        self.verticalLayout.addWidget(self.customFileCheckBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.customFileNameInput = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.customFileNameInput.setEnabled(False)
        self.customFileNameInput.setText("")
        self.customFileNameInput.setObjectName("customFileNameInput")
        self.horizontalLayout.addWidget(self.customFileNameInput)
        self.customFileExtInput = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.customFileExtInput.setEnabled(False)
        self.customFileExtInput.setText("")
        self.customFileExtInput.setObjectName("customFileExtInput")
        self.horizontalLayout.addWidget(self.customFileExtInput)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.dialogButtonBox = QtWidgets.QDialogButtonBox(self.verticalLayoutWidget)
        self.dialogButtonBox.setStyleSheet("")
        self.dialogButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.dialogButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.dialogButtonBox.setCenterButtons(False)
        self.dialogButtonBox.setObjectName("dialogButtonBox")
        self.verticalLayout.addWidget(self.dialogButtonBox)

        self.retranslateUi(self)
        self.dialogButtonBox.accepted.connect(self.accept)
        self.dialogButtonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)


        self.pdfCheckBox.clicked.connect(self.get_link)
        self.retrunVal = None

    def retranslateUi(self, courseExtraFilesDownloadTypeDialog):
        _translate = QtCore.QCoreApplication.translate
        courseExtraFilesDownloadTypeDialog.setWindowTitle(_translate("courseExtraFilesDownloadTypeDialog", "Dialog"))
        self.pdfCheckBox.setText(_translate("courseExtraFilesDownloadTypeDialog", "PDF File"))
        self.mp4CheckBox.setText(_translate("courseExtraFilesDownloadTypeDialog", "MP4 File"))
        self.mp4FileNameInput.setPlaceholderText(_translate("courseExtraFilesDownloadTypeDialog", "MP4 file name"))
        self.customFileCheckBox.setText(_translate("courseExtraFilesDownloadTypeDialog", "Custom File"))
        self.customFileNameInput.setPlaceholderText(_translate("courseExtraFilesDownloadTypeDialog", "Custom file name"))
        self.customFileExtInput.setPlaceholderText(_translate("courseExtraFilesDownloadTypeDialog", "Extentsion, exp. pptx"))

    def get_link(self):
        self.retrunVal = self.pdfCheckBox.isChecked()

    def exec_(self):
        super(Ui_courseExtraFilesDownloadTypeDialog, self).exec_()
        return self.retrunVal


