# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fitsViewer.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1182, 756)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 1161, 731))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.vlDataView = QtGui.QVBoxLayout()
        self.vlDataView.setSpacing(5)
        self.vlDataView.setObjectName(_fromUtf8("vlDataView"))
        self.glFitsImage = GraphicsLayoutWidget(self.widget)
        self.glFitsImage.setObjectName(_fromUtf8("glFitsImage"))
        self.vlDataView.addWidget(self.glFitsImage)
        self.grdlDataButtons = QtGui.QGridLayout()
        self.grdlDataButtons.setHorizontalSpacing(5)
        self.grdlDataButtons.setVerticalSpacing(0)
        self.grdlDataButtons.setObjectName(_fromUtf8("grdlDataButtons"))
        self.btnFirstDataFrame = QtGui.QPushButton(self.widget)
        self.btnFirstDataFrame.setObjectName(_fromUtf8("btnFirstDataFrame"))
        self.grdlDataButtons.addWidget(self.btnFirstDataFrame, 1, 4, 1, 1)
        self.btnPrevDataFrame = QtGui.QPushButton(self.widget)
        self.btnPrevDataFrame.setObjectName(_fromUtf8("btnPrevDataFrame"))
        self.grdlDataButtons.addWidget(self.btnPrevDataFrame, 1, 5, 1, 1)
        self.btnSelectDataFile = QtGui.QPushButton(self.widget)
        self.btnSelectDataFile.setObjectName(_fromUtf8("btnSelectDataFile"))
        self.grdlDataButtons.addWidget(self.btnSelectDataFile, 0, 0, 1, 1)
        self.btnLastDataFrame = QtGui.QPushButton(self.widget)
        self.btnLastDataFrame.setObjectName(_fromUtf8("btnLastDataFrame"))
        self.grdlDataButtons.addWidget(self.btnLastDataFrame, 1, 7, 1, 1)
        self.spinDataFrameNum = QtGui.QSpinBox(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinDataFrameNum.sizePolicy().hasHeightForWidth())
        self.spinDataFrameNum.setSizePolicy(sizePolicy)
        self.spinDataFrameNum.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinDataFrameNum.setObjectName(_fromUtf8("spinDataFrameNum"))
        self.grdlDataButtons.addWidget(self.spinDataFrameNum, 1, 3, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.grdlDataButtons.addItem(spacerItem, 1, 2, 1, 1)
        self.btnReloadDataFile = QtGui.QPushButton(self.widget)
        self.btnReloadDataFile.setObjectName(_fromUtf8("btnReloadDataFile"))
        self.grdlDataButtons.addWidget(self.btnReloadDataFile, 1, 0, 1, 1)
        self.btnNextDataFrame = QtGui.QPushButton(self.widget)
        self.btnNextDataFrame.setObjectName(_fromUtf8("btnNextDataFrame"))
        self.grdlDataButtons.addWidget(self.btnNextDataFrame, 1, 6, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.grdlDataButtons.addItem(spacerItem1, 1, 1, 1, 1)
        self.editDataFilename = QtGui.QLineEdit(self.widget)
        self.editDataFilename.setObjectName(_fromUtf8("editDataFilename"))
        self.grdlDataButtons.addWidget(self.editDataFilename, 0, 1, 1, 7)
        self.vlDataView.addLayout(self.grdlDataButtons)
        self.horizontalLayout.addLayout(self.vlDataView)
        self.vlFitsParams = QtGui.QVBoxLayout()
        self.vlFitsParams.setObjectName(_fromUtf8("vlFitsParams"))
        self.labelFitsParams = QtGui.QLabel(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelFitsParams.sizePolicy().hasHeightForWidth())
        self.labelFitsParams.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.labelFitsParams.setFont(font)
        self.labelFitsParams.setObjectName(_fromUtf8("labelFitsParams"))
        self.vlFitsParams.addWidget(self.labelFitsParams)
        self.hlFitsParamsCols = QtGui.QHBoxLayout()
        self.hlFitsParamsCols.setObjectName(_fromUtf8("hlFitsParamsCols"))
        self.viewFitsParamsLeft = QtGui.QTableView(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.viewFitsParamsLeft.sizePolicy().hasHeightForWidth())
        self.viewFitsParamsLeft.setSizePolicy(sizePolicy)
        self.viewFitsParamsLeft.setObjectName(_fromUtf8("viewFitsParamsLeft"))
        self.hlFitsParamsCols.addWidget(self.viewFitsParamsLeft)
        self.viewFitsParamsRight = QtGui.QTableView(self.widget)
        self.viewFitsParamsRight.setObjectName(_fromUtf8("viewFitsParamsRight"))
        self.hlFitsParamsCols.addWidget(self.viewFitsParamsRight)
        self.vlFitsParams.addLayout(self.hlFitsParamsCols)
        self.cbPauseParamUpdates = QtGui.QCheckBox(self.widget)
        self.cbPauseParamUpdates.setObjectName(_fromUtf8("cbPauseParamUpdates"))
        self.vlFitsParams.addWidget(self.cbPauseParamUpdates)
        spacerItem2 = QtGui.QSpacerItem(400, 150, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        self.vlFitsParams.addItem(spacerItem2)
        self.horizontalLayout.addLayout(self.vlFitsParams)
        self.horizontalLayout.setStretch(0, 7)
        self.horizontalLayout.setStretch(1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1182, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.btnFirstDataFrame.setText(_translate("MainWindow", "<< First", None))
        self.btnPrevDataFrame.setText(_translate("MainWindow", "< Prev", None))
        self.btnSelectDataFile.setText(_translate("MainWindow", "Load data file", None))
        self.btnLastDataFrame.setText(_translate("MainWindow", "Last >>", None))
        self.btnReloadDataFile.setText(_translate("MainWindow", "Reload", None))
        self.btnNextDataFrame.setText(_translate("MainWindow", "Next >", None))
        self.labelFitsParams.setText(_translate("MainWindow", "Experiment parameters in FITS file", None))
        self.cbPauseParamUpdates.setText(_translate("MainWindow", "Pause updates of Experiment Parameters (for faster browsing)", None))

from pyqtgraph import GraphicsLayoutWidget
