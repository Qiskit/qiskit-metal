# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './edit_source_ui.ui',
# licensing of './edit_source_ui.ui' applies.
#
# Created: Wed Jan 20 13:44:43 2021
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_EditSource(object):

    def setupUi(self, EditSource):
        EditSource.setObjectName("EditSource")
        EditSource.resize(1211, 681)
        font = QtGui.QFont()
        font.setFamily("Arial")
        EditSource.setFont(font)
        self.centralwidget = QtWidgets.QWidget(EditSource)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.splitter.setLineWidth(2)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setHandleWidth(10)
        self.splitter.setObjectName("splitter")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_rebuild = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setWeight(75)
        font.setBold(True)
        self.btn_rebuild.setFont(font)
        self.btn_rebuild.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgb(61, 217, 245), stop:1 rgb(240, 53, 218));\n"
            "border-style: solid;\n"
            "border-radius:21px;\n"
            "font-weight: bold;\n"
            "color: rgb(255, 255, 255);")
        self.btn_rebuild.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/rebuild"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.btn_rebuild.setIcon(icon)
        self.btn_rebuild.setIconSize(QtCore.QSize(16, 16))
        self.btn_rebuild.setObjectName("btn_rebuild")
        self.horizontalLayout_2.addWidget(self.btn_rebuild)
        self.line_2 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_2.addWidget(self.line_2)
        self.zoomin = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.zoomin.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/plot/zoom_in_large"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.zoomin.setIcon(icon1)
        self.zoomin.setObjectName("zoomin")
        self.horizontalLayout_2.addWidget(self.zoomin)
        self.zoomout = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.zoomout.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/plot/zoom_out_large"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.zoomout.setIcon(icon2)
        self.zoomout.setObjectName("zoomout")
        self.horizontalLayout_2.addWidget(self.zoomout)
        self.undo = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.undo.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/plot/undo"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.undo.setIcon(icon3)
        self.undo.setObjectName("undo")
        self.horizontalLayout_2.addWidget(self.undo)
        self.btn_save = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setWeight(75)
        font.setBold(True)
        self.btn_save.setFont(font)
        self.btn_save.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/save"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.btn_save.setIcon(icon4)
        self.btn_save.setIconSize(QtCore.QSize(16, 16))
        self.btn_save.setObjectName("btn_save")
        self.horizontalLayout_2.addWidget(self.btn_save)
        self.btn_reload = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_reload.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/refresh"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.btn_reload.setIcon(icon5)
        self.btn_reload.setIconSize(QtCore.QSize(16, 16))
        self.btn_reload.setObjectName("btn_reload")
        self.horizontalLayout_2.addWidget(self.btn_reload)
        self.center = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.center.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/plot/center"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.center.setIcon(icon6)
        self.center.setObjectName("center")
        self.horizontalLayout_2.addWidget(self.center)
        self.pushButtonHideHelp = QtWidgets.QPushButton(
            self.verticalLayoutWidget)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/plot/questionmark_black"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonHideHelp.setIcon(icon7)
        self.pushButtonHideHelp.setIconSize(QtCore.QSize(16, 16))
        self.pushButtonHideHelp.setObjectName("pushButtonHideHelp")
        self.horizontalLayout_2.addWidget(self.pushButtonHideHelp)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.src_editor = MetalSourceEditor(self.verticalLayoutWidget)
        self.src_editor.setObjectName("src_editor")
        self.horizontalLayout.addWidget(self.src_editor)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.lineSrcPath = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineSrcPath.setReadOnly(True)
        self.lineSrcPath.setObjectName("lineSrcPath")
        self.verticalLayout.addWidget(self.lineSrcPath)
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setContentsMargins(0, 0, -1, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.textEditHelp = QtWidgets.QTextEdit(self.layoutWidget)
        self.textEditHelp.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
        self.textEditHelp.setReadOnly(True)
        self.textEditHelp.setObjectName("textEditHelp")
        self.verticalLayout_2.addWidget(self.textEditHelp)
        self.verticalLayout_3.addWidget(self.splitter)
        EditSource.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1211, 22))
        self.menubar.setObjectName("menubar")
        EditSource.setMenuBar(self.menubar)
        self.statusBar = QtWidgets.QStatusBar(EditSource)
        self.statusBar.setObjectName("statusBar")
        EditSource.setStatusBar(self.statusBar)

        self.retranslateUi(EditSource)
        QtCore.QObject.connect(self.btn_save, QtCore.SIGNAL("clicked()"),
                               self.src_editor.save_file)
        QtCore.QObject.connect(self.btn_reload, QtCore.SIGNAL("clicked()"),
                               self.src_editor.reload_file)
        QtCore.QObject.connect(self.zoomout, QtCore.SIGNAL("clicked()"),
                               self.src_editor.zoomOut)
        QtCore.QObject.connect(self.zoomin, QtCore.SIGNAL("clicked()"),
                               self.src_editor.zoomIn)
        QtCore.QObject.connect(self.undo, QtCore.SIGNAL("clicked()"),
                               self.src_editor.undo)
        QtCore.QObject.connect(self.center, QtCore.SIGNAL("clicked()"),
                               self.src_editor.centerCursor)
        QtCore.QObject.connect(self.btn_rebuild, QtCore.SIGNAL("clicked()"),
                               self.src_editor.rebuild_components)
        QtCore.QObject.connect(self.pushButtonHideHelp,
                               QtCore.SIGNAL("clicked()"),
                               self.src_editor.hide_help)
        QtCore.QMetaObject.connectSlotsByName(EditSource)

    def retranslateUi(self, EditSource):
        EditSource.setWindowTitle(
            QtWidgets.QApplication.translate("EditSource", "Edit source code",
                                             None, -1))
        self.btn_rebuild.setToolTip(
            QtWidgets.QApplication.translate("EditSource", "Rebuild Component",
                                             None, -1))
        self.btn_rebuild.setShortcut(
            QtWidgets.QApplication.translate("EditSource", "Ctrl+R, Meta+R",
                                             None, -1))
        self.zoomin.setToolTip(
            QtWidgets.QApplication.translate("EditSource", "Zoom In", None, -1))
        self.zoomout.setToolTip(
            QtWidgets.QApplication.translate("EditSource", "Zoom Out", None,
                                             -1))
        self.undo.setToolTip(
            QtWidgets.QApplication.translate("EditSource", "Undo", None, -1))
        self.btn_save.setToolTip(
            QtWidgets.QApplication.translate("EditSource", "Save File", None,
                                             -1))
        self.btn_save.setShortcut(
            QtWidgets.QApplication.translate("EditSource", "Ctrl+S, Meta+S",
                                             None, -1))
        self.btn_reload.setToolTip(
            QtWidgets.QApplication.translate("EditSource", "Reload File", None,
                                             -1))
        self.center.setToolTip(
            QtWidgets.QApplication.translate("EditSource", "Center", None, -1))
        self.pushButtonHideHelp.setToolTip(
            QtWidgets.QApplication.translate("EditSource", "Help", None, -1))
        self.pushButtonHideHelp.setText(
            QtWidgets.QApplication.translate("EditSource", "Help", None, -1))
        self.src_editor.setPlainText(
            QtWidgets.QApplication.translate("EditSource", "Source comes here",
                                             None, -1))
        self.lineSrcPath.setText(
            QtWidgets.QApplication.translate("EditSource",
                                             "Source code file path here", None,
                                             -1))
        self.textEditHelp.setDocumentTitle(
            QtWidgets.QApplication.translate("EditSource", "Help", None, -1))
        self.textEditHelp.setHtml(
            QtWidgets.QApplication.translate(
                "EditSource",
                "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                "<html><head><meta name=\"qrichtext\" content=\"1\" /><title>Help</title><style type=\"text/css\">\n"
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:\'Arial\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
                "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:22.4px; background-color:#ffffff;\"><span style=\" font-weight:600; color:#797a7a; background-color:#ffffff;\">Help me?</span></p>\n"
                "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:22.4px; background-color:#ffffff;\"><span style=\" font-style:italic; color:#797a7a; background-color:#ffffff;\">Double click </span><span style=\" color:#797a7a; background-color:#ffffff;\">any function or class in the source code to view its documentation. </span></p>\n"
                "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:22.4px; background-color:#ffffff;\"><span style=\" color:#797a7a; background-color:#ffffff;\">Documentation is also shown anytime one types</span><span style=\" color:#797a7a;\"> a bracket </span><span style=\" font-family:\'Monaco\'; color:#797a7a;\">(</span><span style=\" color:#797a7a;\"> after the name of a function. </span><span style=\" color:#797a7a; background-color:#ffffff;\">For example, enter</span><span style=\" color:#797a7a;\"> </span><span style=\" color:#797a7a; background-color:#ecf0f3;\">draw.rectangle(</span><span style=\" color:#797a7a;\">, and a  calltip will appear here.</span></p>\n"
                "<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:22.4px; color:#797a7a; background-color:#ffffff;\"><br /></p>\n"
                "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:22.4px; background-color:#ffffff;\"><span style=\" font-weight:600; color:#797a7a;\">Hide help panel? </span></p>\n"
                "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:22.4px; background-color:#ffffff;\"><span style=\" color:#797a7a;\">Drag the slider in the middle all the way to the right. </span></p>\n"
                "<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:22.4px; color:#797a7a; background-color:#ffffff;\"><br /></p>\n"
                "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:22.4px; background-color:#ffffff;\"><span style=\" font-weight:600; color:#797a7a;\">Search, replace, and more?</span></p>\n"
                "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:22.4px; background-color:#ffffff;\"><span style=\" color:#797a7a;\">Right click the source code to view more.</span></p></body></html>",
                None, -1))


from .widgets.edit_component.source_editor import MetalSourceEditor
from . import main_window_rc_rc
