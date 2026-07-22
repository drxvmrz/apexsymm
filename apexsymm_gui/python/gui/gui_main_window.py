# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_main.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QGroupBox, QHeaderView, QLayout, QLineEdit,
    QListWidget, QListWidgetItem, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSpinBox,
    QSplitter, QStatusBar, QTableWidget, QTableWidgetItem,
    QTextBrowser, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1061, 652)
        self.action_open_cif_file = QAction(MainWindow)
        self.action_open_cif_file.setObjectName(u"action_open_cif_file")
        self.action_open_cif_file.setMenuRole(QAction.MenuRole.NoRole)
        self.action_open_cif_folder = QAction(MainWindow)
        self.action_open_cif_folder.setObjectName(u"action_open_cif_folder")
        self.action_open_cif_folder.setMenuRole(QAction.MenuRole.NoRole)
        self.actionAdd_operator = QAction(MainWindow)
        self.actionAdd_operator.setObjectName(u"actionAdd_operator")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.action_run = QAction(MainWindow)
        self.action_run.setObjectName(u"action_run")
        self.actionAbout_2 = QAction(MainWindow)
        self.actionAbout_2.setObjectName(u"actionAbout_2")
        self.actionSave_results_as = QAction(MainWindow)
        self.actionSave_results_as.setObjectName(u"actionSave_results_as")
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        self.action_stop = QAction(MainWindow)
        self.action_stop.setObjectName(u"action_stop")
        self.action_settings = QAction(MainWindow)
        self.action_settings.setObjectName(u"action_settings")
        self.action_settings.setMenuRole(QAction.MenuRole.NoRole)
        self.action_about = QAction(MainWindow)
        self.action_about.setObjectName(u"action_about")
        self.action_about.setMenuRole(QAction.MenuRole.NoRole)
        self.action_open_opl = QAction(MainWindow)
        self.action_open_opl.setObjectName(u"action_open_opl")
        self.action_save_opl = QAction(MainWindow)
        self.action_save_opl.setObjectName(u"action_save_opl")
        self.action_open_res_json = QAction(MainWindow)
        self.action_open_res_json.setObjectName(u"action_open_res_json")
        self.action_save_csv = QAction(MainWindow)
        self.action_save_csv.setObjectName(u"action_save_csv")
        self.action_save_json = QAction(MainWindow)
        self.action_save_json.setObjectName(u"action_save_json")
        self.action_open_manual = QAction(MainWindow)
        self.action_open_manual.setObjectName(u"action_open_manual")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_8 = QGridLayout(self.centralwidget)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.widget = QWidget(self.splitter)
        self.widget.setObjectName(u"widget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.groupBox = QGroupBox(self.widget)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.btn_settings = QPushButton(self.groupBox)
        self.btn_settings.setObjectName(u"btn_settings")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_settings.sizePolicy().hasHeightForWidth())
        self.btn_settings.setSizePolicy(sizePolicy1)
        icon = QIcon()
        icon.addFile(u"setting_8532656.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_settings.setIcon(icon)

        self.gridLayout_2.addWidget(self.btn_settings, 3, 2, 2, 1)

        self.spin_supcell_radius = QSpinBox(self.groupBox)
        self.spin_supcell_radius.setObjectName(u"spin_supcell_radius")

        self.gridLayout_2.addWidget(self.spin_supcell_radius, 1, 1, 1, 2)

        self.check_no_hydro = QCheckBox(self.groupBox)
        self.check_no_hydro.setObjectName(u"check_no_hydro")

        self.gridLayout_2.addWidget(self.check_no_hydro, 4, 0, 1, 1)

        self.btn_run = QPushButton(self.groupBox)
        self.btn_run.setObjectName(u"btn_run")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.btn_run.sizePolicy().hasHeightForWidth())
        self.btn_run.setSizePolicy(sizePolicy2)
        icon1 = QIcon()
        icon1.addFile(u"play_4251022.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_run.setIcon(icon1)

        self.gridLayout_2.addWidget(self.btn_run, 3, 1, 2, 1)

        self.check_calc_only = QCheckBox(self.groupBox)
        self.check_calc_only.setObjectName(u"check_calc_only")

        self.gridLayout_2.addWidget(self.check_calc_only, 3, 0, 1, 1)

        self.check_use_supcell = QCheckBox(self.groupBox)
        self.check_use_supcell.setObjectName(u"check_use_supcell")

        self.gridLayout_2.addWidget(self.check_use_supcell, 1, 0, 1, 1)

        self.line_cif_path = QLineEdit(self.groupBox)
        self.line_cif_path.setObjectName(u"line_cif_path")

        self.gridLayout_2.addWidget(self.line_cif_path, 0, 0, 1, 2)

        self.btn_open_cif_file = QPushButton(self.groupBox)
        self.btn_open_cif_file.setObjectName(u"btn_open_cif_file")

        self.gridLayout_2.addWidget(self.btn_open_cif_file, 0, 2, 1, 1)


        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 2)

        self.groupBox_2 = QGroupBox(self.widget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy3)
        self.gridLayout_4 = QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.btn_edit_op = QPushButton(self.groupBox_2)
        self.btn_edit_op.setObjectName(u"btn_edit_op")

        self.gridLayout_4.addWidget(self.btn_edit_op, 1, 1, 1, 1)

        self.btn_remove_op = QPushButton(self.groupBox_2)
        self.btn_remove_op.setObjectName(u"btn_remove_op")

        self.gridLayout_4.addWidget(self.btn_remove_op, 1, 2, 1, 1)

        self.btn_add_op = QPushButton(self.groupBox_2)
        self.btn_add_op.setObjectName(u"btn_add_op")

        self.gridLayout_4.addWidget(self.btn_add_op, 1, 0, 1, 1)

        self.btn_remove_all_op = QPushButton(self.groupBox_2)
        self.btn_remove_all_op.setObjectName(u"btn_remove_all_op")

        self.gridLayout_4.addWidget(self.btn_remove_all_op, 1, 3, 1, 1)

        self.list_ops = QListWidget(self.groupBox_2)
        self.list_ops.setObjectName(u"list_ops")

        self.gridLayout_4.addWidget(self.list_ops, 0, 0, 1, 4)

        self.btn_open_opl = QPushButton(self.groupBox_2)
        self.btn_open_opl.setObjectName(u"btn_open_opl")

        self.gridLayout_4.addWidget(self.btn_open_opl, 2, 0, 1, 4)

        self.btn_save_opl = QPushButton(self.groupBox_2)
        self.btn_save_opl.setObjectName(u"btn_save_opl")

        self.gridLayout_4.addWidget(self.btn_save_opl, 3, 0, 1, 4)


        self.gridLayout.addWidget(self.groupBox_2, 0, 0, 1, 2)

        self.splitter.addWidget(self.widget)
        self.widget_2 = QWidget(self.splitter)
        self.widget_2.setObjectName(u"widget_2")
        self.gridLayout_3 = QGridLayout(self.widget_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.groupBox_3 = QGroupBox(self.widget_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_5 = QGridLayout(self.groupBox_3)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.combo_box_structures = QComboBox(self.groupBox_3)
        self.combo_box_structures.setObjectName(u"combo_box_structures")

        self.gridLayout_5.addWidget(self.combo_box_structures, 1, 0, 1, 2)

        self.table_results = QTableWidget(self.groupBox_3)
        self.table_results.setObjectName(u"table_results")

        self.gridLayout_5.addWidget(self.table_results, 0, 0, 1, 2)

        self.btn_open_res_json = QPushButton(self.groupBox_3)
        self.btn_open_res_json.setObjectName(u"btn_open_res_json")

        self.gridLayout_5.addWidget(self.btn_open_res_json, 4, 0, 1, 2)

        self.btn_save_csv = QPushButton(self.groupBox_3)
        self.btn_save_csv.setObjectName(u"btn_save_csv")

        self.gridLayout_5.addWidget(self.btn_save_csv, 2, 0, 1, 2)

        self.btn_save_json = QPushButton(self.groupBox_3)
        self.btn_save_json.setObjectName(u"btn_save_json")

        self.gridLayout_5.addWidget(self.btn_save_json, 3, 0, 1, 2)


        self.gridLayout_3.addWidget(self.groupBox_3, 0, 0, 1, 1)

        self.splitter.addWidget(self.widget_2)
        self.widget_3 = QWidget(self.splitter)
        self.widget_3.setObjectName(u"widget_3")
        self.gridLayout_7 = QGridLayout(self.widget_3)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.groupBox_4 = QGroupBox(self.widget_3)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout_6 = QGridLayout(self.groupBox_4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.info_text_browser = QTextBrowser(self.groupBox_4)
        self.info_text_browser.setObjectName(u"info_text_browser")

        self.gridLayout_6.addWidget(self.info_text_browser, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.groupBox_4, 0, 0, 1, 1)

        self.splitter.addWidget(self.widget_3)

        self.gridLayout_8.addWidget(self.splitter, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1061, 33))
        self.menubar.setAcceptDrops(False)
        self.menubar.setDefaultUp(False)
        self.menu_file = QMenu(self.menubar)
        self.menu_file.setObjectName(u"menu_file")
        self.menu_file.setTearOffEnabled(False)
        self.menu_run = QMenu(self.menubar)
        self.menu_run.setObjectName(u"menu_run")
        self.menu_help = QMenu(self.menubar)
        self.menu_help.setObjectName(u"menu_help")
        MainWindow.setMenuBar(self.menubar)
        self.status_bar = QStatusBar(MainWindow)
        self.status_bar.setObjectName(u"status_bar")
        MainWindow.setStatusBar(self.status_bar)

        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_run.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
        self.menu_file.addAction(self.action_open_cif_file)
        self.menu_file.addAction(self.action_open_cif_folder)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_open_opl)
        self.menu_file.addAction(self.action_save_opl)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_save_csv)
        self.menu_file.addAction(self.action_save_json)
        self.menu_file.addAction(self.action_open_res_json)
        self.menu_run.addAction(self.action_run)
        self.menu_run.addAction(self.action_stop)
        self.menu_run.addSeparator()
        self.menu_run.addAction(self.action_settings)
        self.menu_help.addAction(self.action_open_manual)
        self.menu_help.addSeparator()
        self.menu_help.addAction(self.action_about)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_open_cif_file.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c .cif-\u0444\u0430\u0439\u043b", None))
        self.action_open_cif_folder.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c .cif-\u043f\u0430\u043f\u043a\u0443", None))
        self.actionAdd_operator.setText(QCoreApplication.translate("MainWindow", u"Add operator", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"Eidt", None))
        self.action_run.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043f\u0443\u0441\u043a", None))
        self.actionAbout_2.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.actionSave_results_as.setText(QCoreApplication.translate("MainWindow", u"Save results as ...", None))
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.action_stop.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0430", None))
        self.action_settings.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.action_about.setText(QCoreApplication.translate("MainWindow", u"\u041e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0435", None))
        self.action_open_opl.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0444\u0430\u0439\u043b \u0441\u043f\u0438\u0441\u043a\u0430 \u043e\u043f\u0435\u0440\u0430\u0442\u043e\u0440\u043e\u0432 (.olf)", None))
        self.action_save_opl.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u043e\u043f\u0435\u0440\u0430\u0442\u043e\u0440\u044b \u0432 \u0444\u0430\u0439\u043b \u0441\u043f\u0438\u0441\u043a\u0430", None))
        self.action_open_res_json.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c .json \u0441 \u043f\u0440\u043e\u0448\u043b\u044b\u043c\u0438 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u0430\u043c\u0438", None))
        self.action_save_csv.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0442\u0435\u043a\u0443\u0449\u0438\u0435 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u044b \u0432 .csv-\u0444\u0430\u0439\u043b", None))
        self.action_save_json.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0442\u0435\u043a\u0443\u0449\u0438\u0439 .json \u0441 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u0430\u043c\u0438", None))
        self.action_open_manual.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0440\u0443\u043a\u043e\u0432\u043e\u0434\u0441\u0442\u0432\u043e \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u0435\u0434\u0443\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0438 \u0438 \u0437\u0430\u043f\u0443\u0441\u043a", None))
        self.btn_settings.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.check_no_hydro.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0435 \u0443\u0447\u0438\u0442\u044b\u0432\u0430\u0442\u044c \u0432\u043e\u0434\u043e\u0440\u043e\u0434", None))
        self.btn_run.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043f\u0443\u0441\u043a", None))
        self.check_calc_only.setText(QCoreApplication.translate("MainWindow", u"\u0422\u043e\u043b\u044c\u043a\u043e \u0440\u0430\u0441\u0447\u0435\u0442", None))
        self.check_use_supcell.setText(QCoreApplication.translate("MainWindow", u"\u0412\u043a\u043b\u044e\u0447\u0438\u0442\u044c \u0441\u0443\u043f\u0435\u0440\u044f\u0447\u0435\u0439\u043a\u0443", None))
        self.btn_open_cif_file.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c .cif ", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u041e\u043f\u0435\u0440\u0430\u0442\u043e\u0440\u044b \u043f\u0441\u0435\u0432\u0434\u043e\u0441\u0438\u043c\u043c\u0435\u0442\u0440\u0438\u0438 \u0434\u043b\u044f \u0440\u0430\u0441\u0447\u0435\u0442\u0430", None))
        self.btn_edit_op.setText(QCoreApplication.translate("MainWindow", u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.btn_remove_op.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c", None))
        self.btn_add_op.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
        self.btn_remove_all_op.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0447\u0438\u0441\u0442\u0438\u0442\u044c", None))
        self.btn_open_opl.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0444\u0430\u0439\u043b \u0441\u043f\u0438\u0441\u043a\u0430 \u043e\u043f\u0435\u0440\u0430\u0442\u043e\u0440\u043e\u0432 (.olf)", None))
        self.btn_save_opl.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u043e\u043f\u0435\u0440\u0430\u0442\u043e\u0440\u044b \u0432 \u0444\u0430\u0439\u043b \u0441\u043f\u0438\u0441\u043a\u0430", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u044b \u0438 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u044b \u0440\u0430\u0441\u0447\u0435\u0442\u0430", None))
        self.btn_open_res_json.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c .json \u0441 \u043f\u0440\u043e\u0448\u043b\u044b\u043c\u0438 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u0430\u043c\u0438", None))
        self.btn_save_csv.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0442\u0435\u043a\u0443\u0449\u0438\u0435 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u044b \u0432 .csv-\u0444\u0430\u0439\u043b", None))
        self.btn_save_json.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0442\u0435\u043a\u0443\u0449\u0438\u0439 .json \u0441 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u0430\u043c\u0438", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"\u0418\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f \u043e \u0441\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u0435", None))
        self.menu_file.setTitle(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u0439\u043b", None))
        self.menu_run.setTitle(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043f\u0443\u0441\u043a", None))
        self.menu_help.setTitle(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043c\u043e\u0449\u044c", None))
    # retranslateUi

