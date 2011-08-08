# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CameraTemplate.ui'
#
# Created: Mon Aug 08 14:49:44 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(901, 521)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.graphicsWidget = QtGui.QWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsWidget.sizePolicy().hasHeightForWidth())
        self.graphicsWidget.setSizePolicy(sizePolicy)
        self.graphicsWidget.setObjectName(_fromUtf8("graphicsWidget"))
        self.horizontalLayout_3.addWidget(self.graphicsWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget = QtGui.QDockWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidget.sizePolicy().hasHeightForWidth())
        self.dockWidget.setSizePolicy(sizePolicy)
        self.dockWidget.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable|QtGui.QDockWidget.DockWidgetVerticalTitleBar)
        self.dockWidget.setObjectName(_fromUtf8("dockWidget"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout_2 = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.btnAcquire = QtGui.QPushButton(self.dockWidgetContents)
        self.btnAcquire.setCheckable(True)
        self.btnAcquire.setObjectName(_fromUtf8("btnAcquire"))
        self.horizontalLayout_5.addWidget(self.btnAcquire)
        self.btnSnap = FeedbackButton(self.dockWidgetContents)
        self.btnSnap.setObjectName(_fromUtf8("btnSnap"))
        self.horizontalLayout_5.addWidget(self.btnSnap)
        self.btnRecord = QtGui.QPushButton(self.dockWidgetContents)
        self.btnRecord.setEnabled(True)
        self.btnRecord.setCheckable(True)
        self.btnRecord.setFlat(False)
        self.btnRecord.setObjectName(_fromUtf8("btnRecord"))
        self.horizontalLayout_5.addWidget(self.btnRecord)
        self.recordXframesCheck = QtGui.QCheckBox(self.dockWidgetContents)
        self.recordXframesCheck.setObjectName(_fromUtf8("recordXframesCheck"))
        self.horizontalLayout_5.addWidget(self.recordXframesCheck)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.recordXframesSpin = QtGui.QSpinBox(self.dockWidgetContents)
        self.recordXframesSpin.setEnabled(True)
        self.recordXframesSpin.setMinimum(1)
        self.recordXframesSpin.setMaximum(1000000)
        self.recordXframesSpin.setProperty(_fromUtf8("value"), 100)
        self.recordXframesSpin.setObjectName(_fromUtf8("recordXframesSpin"))
        self.horizontalLayout_4.addWidget(self.recordXframesSpin)
        self.framesLabel = QtGui.QLabel(self.dockWidgetContents)
        self.framesLabel.setEnabled(True)
        self.framesLabel.setObjectName(_fromUtf8("framesLabel"))
        self.horizontalLayout_4.addWidget(self.framesLabel)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.label_2 = QtGui.QLabel(self.dockWidgetContents)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.hboxlayout.addWidget(self.label_2)
        self.binningCombo = QtGui.QComboBox(self.dockWidgetContents)
        self.binningCombo.setObjectName(_fromUtf8("binningCombo"))
        self.hboxlayout.addWidget(self.binningCombo)
        self.label_3 = QtGui.QLabel(self.dockWidgetContents)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.hboxlayout.addWidget(self.label_3)
        self.spinExposure = SpinBox(self.dockWidgetContents)
        self.spinExposure.setMinimumSize(QtCore.QSize(80, 0))
        self.spinExposure.setObjectName(_fromUtf8("spinExposure"))
        self.hboxlayout.addWidget(self.spinExposure)
        self.btnFullFrame = QtGui.QPushButton(self.dockWidgetContents)
        self.btnFullFrame.setObjectName(_fromUtf8("btnFullFrame"))
        self.hboxlayout.addWidget(self.btnFullFrame)
        self.scaleToImageBtn = QtGui.QPushButton(self.dockWidgetContents)
        self.scaleToImageBtn.setObjectName(_fromUtf8("scaleToImageBtn"))
        self.hboxlayout.addWidget(self.scaleToImageBtn)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.gridLayout_2.addLayout(self.hboxlayout, 1, 0, 1, 1)
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.dockWidget)
        self.dockWidget_2 = QtGui.QDockWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidget_2.sizePolicy().hasHeightForWidth())
        self.dockWidget_2.setSizePolicy(sizePolicy)
        self.dockWidget_2.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.dockWidget_2.setObjectName(_fromUtf8("dockWidget_2"))
        self.dockWidgetContents_2 = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidgetContents_2.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents_2.setSizePolicy(sizePolicy)
        self.dockWidgetContents_2.setObjectName(_fromUtf8("dockWidgetContents_2"))
        self.vboxlayout = QtGui.QVBoxLayout(self.dockWidgetContents_2)
        self.vboxlayout.setSpacing(0)
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName(_fromUtf8("hboxlayout1"))
        self.histogram = GraphicsView(self.dockWidgetContents_2)
        self.histogram.setFrameShape(QtGui.QFrame.NoFrame)
        self.histogram.setObjectName(_fromUtf8("histogram"))
        self.hboxlayout1.addWidget(self.histogram)
        self.gradientWidget = GradientWidget(self.dockWidgetContents_2)
        self.gradientWidget.setMinimumSize(QtCore.QSize(20, 0))
        self.gradientWidget.setObjectName(_fromUtf8("gradientWidget"))
        self.hboxlayout1.addWidget(self.gradientWidget)
        self.vboxlayout.addLayout(self.hboxlayout1)
        self.btnAutoGain = QtGui.QPushButton(self.dockWidgetContents_2)
        self.btnAutoGain.setCheckable(True)
        self.btnAutoGain.setChecked(False)
        self.btnAutoGain.setObjectName(_fromUtf8("btnAutoGain"))
        self.vboxlayout.addWidget(self.btnAutoGain)
        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setHorizontalSpacing(6)
        self.gridlayout.setVerticalSpacing(0)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.label_6 = QtGui.QLabel(self.dockWidgetContents_2)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridlayout.addWidget(self.label_6, 0, 0, 1, 1)
        self.spinAutoGainSpeed = QtGui.QDoubleSpinBox(self.dockWidgetContents_2)
        self.spinAutoGainSpeed.setProperty(_fromUtf8("value"), 2.0)
        self.spinAutoGainSpeed.setObjectName(_fromUtf8("spinAutoGainSpeed"))
        self.gridlayout.addWidget(self.spinAutoGainSpeed, 0, 1, 1, 1)
        self.label_8 = QtGui.QLabel(self.dockWidgetContents_2)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridlayout.addWidget(self.label_8, 1, 0, 1, 1)
        self.spinAutoGainCenterWeight = QtGui.QDoubleSpinBox(self.dockWidgetContents_2)
        self.spinAutoGainCenterWeight.setMaximum(1.0)
        self.spinAutoGainCenterWeight.setSingleStep(0.1)
        self.spinAutoGainCenterWeight.setObjectName(_fromUtf8("spinAutoGainCenterWeight"))
        self.gridlayout.addWidget(self.spinAutoGainCenterWeight, 1, 1, 1, 1)
        self.vboxlayout.addLayout(self.gridlayout)
        self.dockWidget_2.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget_2)
        self.dockWidget_4 = QtGui.QDockWidget(MainWindow)
        self.dockWidget_4.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable|QtGui.QDockWidget.DockWidgetVerticalTitleBar)
        self.dockWidget_4.setObjectName(_fromUtf8("dockWidget_4"))
        self.dockWidgetContents_4 = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidgetContents_4.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents_4.setSizePolicy(sizePolicy)
        self.dockWidgetContents_4.setObjectName(_fromUtf8("dockWidgetContents_4"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.dockWidgetContents_4)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.checkEnableROIs = QtGui.QCheckBox(self.dockWidgetContents_4)
        self.checkEnableROIs.setObjectName(_fromUtf8("checkEnableROIs"))
        self.gridLayout.addWidget(self.checkEnableROIs, 0, 0, 1, 2)
        self.label_7 = QtGui.QLabel(self.dockWidgetContents_4)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 5, 0, 1, 1)
        self.spinROITime = QtGui.QDoubleSpinBox(self.dockWidgetContents_4)
        self.spinROITime.setSingleStep(0.1)
        self.spinROITime.setProperty(_fromUtf8("value"), 5.0)
        self.spinROITime.setObjectName(_fromUtf8("spinROITime"))
        self.gridLayout.addWidget(self.spinROITime, 5, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(88, 17, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 6, 0, 1, 2)
        self.btnAddROI = QtGui.QPushButton(self.dockWidgetContents_4)
        self.btnAddROI.setObjectName(_fromUtf8("btnAddROI"))
        self.gridLayout.addWidget(self.btnAddROI, 1, 0, 1, 1)
        self.btnClearROIs = QtGui.QPushButton(self.dockWidgetContents_4)
        self.btnClearROIs.setObjectName(_fromUtf8("btnClearROIs"))
        self.gridLayout.addWidget(self.btnClearROIs, 1, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.plotWidget = PlotWidget(self.dockWidgetContents_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotWidget.sizePolicy().hasHeightForWidth())
        self.plotWidget.setSizePolicy(sizePolicy)
        self.plotWidget.setObjectName(_fromUtf8("plotWidget"))
        self.horizontalLayout.addWidget(self.plotWidget)
        self.dockWidget_4.setWidget(self.dockWidgetContents_4)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.dockWidget_4)
        self.dockWidget_5 = QtGui.QDockWidget(MainWindow)
        self.dockWidget_5.setFloating(False)
        self.dockWidget_5.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.dockWidget_5.setObjectName(_fromUtf8("dockWidget_5"))
        self.dockWidgetContents_5 = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidgetContents_5.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents_5.setSizePolicy(sizePolicy)
        self.dockWidgetContents_5.setObjectName(_fromUtf8("dockWidgetContents_5"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.dockWidgetContents_5)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.addFrameBtn = FeedbackButton(self.dockWidgetContents_5)
        self.addFrameBtn.setObjectName(_fromUtf8("addFrameBtn"))
        self.horizontalLayout_2.addWidget(self.addFrameBtn)
        self.clearFramesBtn = QtGui.QPushButton(self.dockWidgetContents_5)
        self.clearFramesBtn.setObjectName(_fromUtf8("clearFramesBtn"))
        self.horizontalLayout_2.addWidget(self.clearFramesBtn)
        self.dockWidget_5.setWidget(self.dockWidgetContents_5)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget_5)
        self.dockWidget_3 = QtGui.QDockWidget(MainWindow)
        self.dockWidget_3.setFloating(False)
        self.dockWidget_3.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.dockWidget_3.setObjectName(_fromUtf8("dockWidget_3"))
        self.dockWidgetContents_3 = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidgetContents_3.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents_3.setSizePolicy(sizePolicy)
        self.dockWidgetContents_3.setObjectName(_fromUtf8("dockWidgetContents_3"))
        self.vboxlayout1 = QtGui.QVBoxLayout(self.dockWidgetContents_3)
        self.vboxlayout1.setSpacing(2)
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setObjectName(_fromUtf8("vboxlayout1"))
        self.label = QtGui.QLabel(self.dockWidgetContents_3)
        self.label.setObjectName(_fromUtf8("label"))
        self.vboxlayout1.addWidget(self.label)
        self.splitter = QtGui.QSplitter(self.dockWidgetContents_3)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.staticBgBtn = FeedbackButton(self.splitter)
        self.staticBgBtn.setCheckable(True)
        self.staticBgBtn.setObjectName(_fromUtf8("staticBgBtn"))
        self.continuousBgBtn = QtGui.QPushButton(self.splitter)
        self.continuousBgBtn.setCheckable(True)
        self.continuousBgBtn.setObjectName(_fromUtf8("continuousBgBtn"))
        self.vboxlayout1.addWidget(self.splitter)
        self.frame_2 = QtGui.QFrame(self.dockWidgetContents_3)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.hboxlayout2 = QtGui.QHBoxLayout(self.frame_2)
        self.hboxlayout2.setSpacing(0)
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setObjectName(_fromUtf8("hboxlayout2"))
        self.label_4 = QtGui.QLabel(self.frame_2)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.hboxlayout2.addWidget(self.label_4)
        self.bgTimeSpin = QtGui.QDoubleSpinBox(self.frame_2)
        self.bgTimeSpin.setSingleStep(1.0)
        self.bgTimeSpin.setProperty(_fromUtf8("value"), 5.0)
        self.bgTimeSpin.setObjectName(_fromUtf8("bgTimeSpin"))
        self.hboxlayout2.addWidget(self.bgTimeSpin)
        self.vboxlayout1.addWidget(self.frame_2)
        self.frame_3 = QtGui.QFrame(self.dockWidgetContents_3)
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.hboxlayout3 = QtGui.QHBoxLayout(self.frame_3)
        self.hboxlayout3.setSpacing(2)
        self.hboxlayout3.setMargin(0)
        self.hboxlayout3.setObjectName(_fromUtf8("hboxlayout3"))
        self.label_5 = QtGui.QLabel(self.frame_3)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.hboxlayout3.addWidget(self.label_5)
        self.bgBlurSpin = QtGui.QDoubleSpinBox(self.frame_3)
        self.bgBlurSpin.setProperty(_fromUtf8("value"), 0.0)
        self.bgBlurSpin.setObjectName(_fromUtf8("bgBlurSpin"))
        self.hboxlayout3.addWidget(self.bgBlurSpin)
        self.vboxlayout1.addWidget(self.frame_3)
        self.divideBgBtn = QtGui.QPushButton(self.dockWidgetContents_3)
        self.divideBgBtn.setCheckable(True)
        self.divideBgBtn.setObjectName(_fromUtf8("divideBgBtn"))
        self.vboxlayout1.addWidget(self.divideBgBtn)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vboxlayout1.addItem(spacerItem3)
        self.dockWidget_3.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget_3)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Camera", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidget.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Camera", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAcquire.setToolTip(QtGui.QApplication.translate("MainWindow", "Start/stop camera acquisition.\n"
"In general, this can just stay on always.", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAcquire.setText(QtGui.QApplication.translate("MainWindow", "Acquire", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSnap.setToolTip(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Record a single frame. </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Image is written to the current storage directory set in </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">the data manager window.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSnap.setText(QtGui.QApplication.translate("MainWindow", "Snap", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRecord.setToolTip(QtGui.QApplication.translate("MainWindow", "Start/stop recording frames as they are acquired. \n"
"Frames are written to the current storage directory set in \n"
"the data manager window.", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRecord.setText(QtGui.QApplication.translate("MainWindow", "Record", None, QtGui.QApplication.UnicodeUTF8))
        self.recordXframesCheck.setText(QtGui.QApplication.translate("MainWindow", "Stop recording after", None, QtGui.QApplication.UnicodeUTF8))
        self.framesLabel.setText(QtGui.QApplication.translate("MainWindow", "frames.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Binning", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Exposure", None, QtGui.QApplication.UnicodeUTF8))
        self.spinExposure.setToolTip(QtGui.QApplication.translate("MainWindow", "Sets the exposure time for each frame.", None, QtGui.QApplication.UnicodeUTF8))
        self.btnFullFrame.setToolTip(QtGui.QApplication.translate("MainWindow", "Set the region of interest to the maximum possible area.", None, QtGui.QApplication.UnicodeUTF8))
        self.btnFullFrame.setText(QtGui.QApplication.translate("MainWindow", "Full Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.scaleToImageBtn.setToolTip(QtGui.QApplication.translate("MainWindow", "Scales the view such that camera pixels match screen pixels exactly. This can increase the rate frames are displayed (does not affect the acquisition rate, though).", None, QtGui.QApplication.UnicodeUTF8))
        self.scaleToImageBtn.setText(QtGui.QApplication.translate("MainWindow", "Scale 1:1", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidget_2.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Display Gain", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAutoGain.setToolTip(QtGui.QApplication.translate("MainWindow", "Determines the behavior of the white/black level sliders.\n"
"When enabled, the sliders maximum and minimum values are set\n"
"to the maximum and minimum intensity values in the image.\n"
"When disabled, the minimum is 0 and the maximum is the largest \n"
"possible intensity given the bit depth of the camera.", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAutoGain.setText(QtGui.QApplication.translate("MainWindow", "Auto Gain", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "Slow", None, QtGui.QApplication.UnicodeUTF8))
        self.spinAutoGainSpeed.setToolTip(QtGui.QApplication.translate("MainWindow", "Smooths out the auto gain control, prevents very\n"
"brief flashes from affecting the gain. Larger values\n"
"indicate more smoothing.\n"
"", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("MainWindow", "Center Weight", None, QtGui.QApplication.UnicodeUTF8))
        self.spinAutoGainCenterWeight.setToolTip(QtGui.QApplication.translate("MainWindow", "Weights the auto gain measurement to the center 1/3 of\n"
"the frame when set to 1.0. A value of 0.0 meters from \n"
"the entire frame.", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidget_4.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Plots", None, QtGui.QApplication.UnicodeUTF8))
        self.checkEnableROIs.setToolTip(QtGui.QApplication.translate("MainWindow", "Enables online calculation/plotting for ROIs.\n"
"ROIs can be still be used as position markers \n"
"if this box is unchecked.", None, QtGui.QApplication.UnicodeUTF8))
        self.checkEnableROIs.setText(QtGui.QApplication.translate("MainWindow", "Enable ROIs", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "Time:", None, QtGui.QApplication.UnicodeUTF8))
        self.spinROITime.setToolTip(QtGui.QApplication.translate("MainWindow", "Sets the amount of time that ROI data is displayed in the plot.", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAddROI.setToolTip(QtGui.QApplication.translate("MainWindow", "Adds an ROI to the canvas.", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAddROI.setText(QtGui.QApplication.translate("MainWindow", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.btnClearROIs.setToolTip(QtGui.QApplication.translate("MainWindow", "Clears all ROIs from the canvas.", None, QtGui.QApplication.UnicodeUTF8))
        self.btnClearROIs.setText(QtGui.QApplication.translate("MainWindow", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidget_5.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Persistent Frames", None, QtGui.QApplication.UnicodeUTF8))
        self.addFrameBtn.setToolTip(QtGui.QApplication.translate("MainWindow", "Adds the current camera image to the canvas.\n"
"", None, QtGui.QApplication.UnicodeUTF8))
        self.addFrameBtn.setText(QtGui.QApplication.translate("MainWindow", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.clearFramesBtn.setToolTip(QtGui.QApplication.translate("MainWindow", "Clears all images from the canvas.", None, QtGui.QApplication.UnicodeUTF8))
        self.clearFramesBtn.setText(QtGui.QApplication.translate("MainWindow", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidget_3.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Background Subtraction", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Collect Background:", None, QtGui.QApplication.UnicodeUTF8))
        self.staticBgBtn.setToolTip(QtGui.QApplication.translate("MainWindow", "Collects a set of frames to use for background division.\n"
"Using static background division is faster than continuous \n"
"background division, but does not enhance time varying signals.\n"
"Frames are collected for the amount of time set in Time const.", None, QtGui.QApplication.UnicodeUTF8))
        self.staticBgBtn.setText(QtGui.QApplication.translate("MainWindow", "Static", None, QtGui.QApplication.UnicodeUTF8))
        self.continuousBgBtn.setToolTip(QtGui.QApplication.translate("MainWindow", "Collects frames continuously for background division.\n"
"Slower than static collection, but enhances time-varying signals.\n"
"Uses the time constant set below.", None, QtGui.QApplication.UnicodeUTF8))
        self.continuousBgBtn.setText(QtGui.QApplication.translate("MainWindow", "Continuous", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Time const.", None, QtGui.QApplication.UnicodeUTF8))
        self.bgTimeSpin.setToolTip(QtGui.QApplication.translate("MainWindow", "Sets the approximate number of frames to be averaged for\n"
"background division.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Blur Bg.", None, QtGui.QApplication.UnicodeUTF8))
        self.bgBlurSpin.setToolTip(QtGui.QApplication.translate("MainWindow", "Blurs the background frame before dividing it from the current frame.", None, QtGui.QApplication.UnicodeUTF8))
        self.divideBgBtn.setToolTip(QtGui.QApplication.translate("MainWindow", "Enables background division. \n"
"Either a set of static background frames need to have already by collected\n"
"(by pressing \'Static\' above) or \'Continuous\' needs to be pressed.", None, QtGui.QApplication.UnicodeUTF8))
        self.divideBgBtn.setText(QtGui.QApplication.translate("MainWindow", "Divide Background", None, QtGui.QApplication.UnicodeUTF8))

from SpinBox import SpinBox
from FeedbackButton import FeedbackButton
from pyqtgraph.GradientWidget import GradientWidget
from pyqtgraph.GraphicsView import GraphicsView
from pyqtgraph.PlotWidget import PlotWidget
