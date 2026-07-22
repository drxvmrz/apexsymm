# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_settings.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QGridLayout,
    QGroupBox, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QWidget)

class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        if not SettingsWindow.objectName():
            SettingsWindow.setObjectName(u"SettingsWindow")
        SettingsWindow.resize(542, 550)
        self.gridLayout_3 = QGridLayout(SettingsWindow)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.groupBox = QGroupBox(SettingsWindow)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 6, 0, 1, 1)

        self.btn_browse_json = QPushButton(self.groupBox)
        self.btn_browse_json.setObjectName(u"btn_browse_json")

        self.gridLayout.addWidget(self.btn_browse_json, 6, 2, 1, 1)

        self.line_json_path = QLineEdit(self.groupBox)
        self.line_json_path.setObjectName(u"line_json_path")

        self.gridLayout.addWidget(self.line_json_path, 6, 1, 1, 1)

        self.line_exec_path = QLineEdit(self.groupBox)
        self.line_exec_path.setObjectName(u"line_exec_path")

        self.gridLayout.addWidget(self.line_exec_path, 7, 1, 1, 1)

        self.spin_max_ops_out = QSpinBox(self.groupBox)
        self.spin_max_ops_out.setObjectName(u"spin_max_ops_out")
        self.spin_max_ops_out.setMinimum(1)
        self.spin_max_ops_out.setMaximum(999999999)
        self.spin_max_ops_out.setSingleStep(50)
        self.spin_max_ops_out.setValue(100)

        self.gridLayout.addWidget(self.spin_max_ops_out, 5, 1, 1, 2)

        self.spin_max_eta_out = QDoubleSpinBox(self.groupBox)
        self.spin_max_eta_out.setObjectName(u"spin_max_eta_out")
        self.spin_max_eta_out.setDecimals(2)
        self.spin_max_eta_out.setMaximum(1.000000000000000)
        self.spin_max_eta_out.setSingleStep(0.010000000000000)

        self.gridLayout.addWidget(self.spin_max_eta_out, 3, 1, 1, 2)

        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 7, 0, 1, 1)

        self.label_14 = QLabel(self.groupBox)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout.addWidget(self.label_14, 5, 0, 1, 1)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)

        self.spin_min_eta_out = QDoubleSpinBox(self.groupBox)
        self.spin_min_eta_out.setObjectName(u"spin_min_eta_out")
        self.spin_min_eta_out.setDecimals(2)
        self.spin_min_eta_out.setMaximum(1.000000000000000)
        self.spin_min_eta_out.setSingleStep(0.010000000000000)

        self.gridLayout.addWidget(self.spin_min_eta_out, 4, 1, 1, 2)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.btn_browse_exe = QPushButton(self.groupBox)
        self.btn_browse_exe.setObjectName(u"btn_browse_exe")

        self.gridLayout.addWidget(self.btn_browse_exe, 7, 2, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox, 2, 0, 1, 3)

        self.groupBox_3 = QGroupBox(SettingsWindow)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_4 = QGridLayout(self.groupBox_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_16 = QLabel(self.groupBox_3)
        self.label_16.setObjectName(u"label_16")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)

        self.gridLayout_4.addWidget(self.label_16, 1, 0, 1, 1)

        self.label_15 = QLabel(self.groupBox_3)
        self.label_15.setObjectName(u"label_15")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy1)

        self.gridLayout_4.addWidget(self.label_15, 0, 0, 1, 1)

        self.combo_language = QComboBox(self.groupBox_3)
        self.combo_language.addItem("")
        self.combo_language.setObjectName(u"combo_language")

        self.gridLayout_4.addWidget(self.combo_language, 1, 1, 1, 2)

        self.combo_gui_theme = QComboBox(self.groupBox_3)
        self.combo_gui_theme.addItem("")
        self.combo_gui_theme.setObjectName(u"combo_gui_theme")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.combo_gui_theme.sizePolicy().hasHeightForWidth())
        self.combo_gui_theme.setSizePolicy(sizePolicy2)

        self.gridLayout_4.addWidget(self.combo_gui_theme, 0, 1, 1, 2)


        self.gridLayout_3.addWidget(self.groupBox_3, 0, 0, 1, 3)

        self.groupBox_2 = QGroupBox(SettingsWindow)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.spin_cpus = QSpinBox(self.groupBox_2)
        self.spin_cpus.setObjectName(u"spin_cpus")

        self.gridLayout_2.addWidget(self.spin_cpus, 2, 1, 1, 1)

        self.spin_resolution = QDoubleSpinBox(self.groupBox_2)
        self.spin_resolution.setObjectName(u"spin_resolution")
        self.spin_resolution.setDecimals(3)
        self.spin_resolution.setMaximum(1.000000000000000)
        self.spin_resolution.setSingleStep(0.001000000000000)

        self.gridLayout_2.addWidget(self.spin_resolution, 5, 1, 1, 1)

        self.label_13 = QLabel(self.groupBox_2)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_2.addWidget(self.label_13, 6, 0, 1, 1)

        self.label_10 = QLabel(self.groupBox_2)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_2.addWidget(self.label_10, 3, 0, 1, 1)

        self.combo_device = QComboBox(self.groupBox_2)
        self.combo_device.addItem("")
        self.combo_device.setObjectName(u"combo_device")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.combo_device.sizePolicy().hasHeightForWidth())
        self.combo_device.setSizePolicy(sizePolicy3)

        self.gridLayout_2.addWidget(self.combo_device, 1, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)

        self.label_12 = QLabel(self.groupBox_2)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_2.addWidget(self.label_12, 5, 0, 1, 1)

        self.line_precision = QLineEdit(self.groupBox_2)
        self.line_precision.setObjectName(u"line_precision")

        self.gridLayout_2.addWidget(self.line_precision, 3, 1, 1, 1)

        self.label_11 = QLabel(self.groupBox_2)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_2.addWidget(self.label_11, 4, 0, 1, 1)

        self.spin_ref_cycles = QSpinBox(self.groupBox_2)
        self.spin_ref_cycles.setObjectName(u"spin_ref_cycles")
        self.spin_ref_cycles.setMaximum(1000)
        self.spin_ref_cycles.setSingleStep(1)
        self.spin_ref_cycles.setValue(10)

        self.gridLayout_2.addWidget(self.spin_ref_cycles, 6, 1, 1, 1)

        self.spin_threshold = QDoubleSpinBox(self.groupBox_2)
        self.spin_threshold.setObjectName(u"spin_threshold")
        self.spin_threshold.setDecimals(3)
        self.spin_threshold.setSingleStep(0.001000000000000)

        self.gridLayout_2.addWidget(self.spin_threshold, 4, 1, 1, 1)

        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox_2, 4, 0, 1, 3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer, 1, 0, 1, 1)

        self.btn_cancel = QPushButton(SettingsWindow)
        self.btn_cancel.setObjectName(u"btn_cancel")

        self.gridLayout_3.addWidget(self.btn_cancel, 5, 2, 1, 1)

        self.btn_apply = QPushButton(SettingsWindow)
        self.btn_apply.setObjectName(u"btn_apply")

        self.gridLayout_3.addWidget(self.btn_apply, 5, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 5, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_2, 3, 0, 1, 1)


        self.retranslateUi(SettingsWindow)

        QMetaObject.connectSlotsByName(SettingsWindow)
    # setupUi

    def retranslateUi(self, SettingsWindow):
        SettingsWindow.setWindowTitle(QCoreApplication.translate("SettingsWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.groupBox.setTitle(QCoreApplication.translate("SettingsWindow", u"\u0421\u0438\u0441\u0442\u0435\u043c\u043d\u044b\u0435 \u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.label_3.setText(QCoreApplication.translate("SettingsWindow", u"\u041f\u0443\u0442\u044c \u043a .json-\u0444\u0430\u0439\u043b\u0443 \u0441 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u0430\u043c\u0438", None))
        self.btn_browse_json.setText(QCoreApplication.translate("SettingsWindow", u"...", None))
        self.label_7.setText(QCoreApplication.translate("SettingsWindow", u"\u041f\u0443\u0442\u044c \u043a \u0438\u0441\u043f\u043e\u043b\u043d\u044f\u0435\u043c\u043e\u043c\u0443 \u0444\u0430\u0439\u043b\u0443 'pss2'", None))
        self.label_14.setText(QCoreApplication.translate("SettingsWindow", u"\u041c\u0430\u043a\u0441\u0438\u043c\u0430\u043b\u044c\u043d\u044b\u0439 \u0432\u044b\u0432\u043e\u0434 \u043e\u043f\u0435\u0440\u0430\u0442\u043e\u0440\u043e\u0432", None))
        self.label_5.setText(QCoreApplication.translate("SettingsWindow", u"\u041c\u0438\u043d\u0438\u043c\u0430\u043b\u044c\u043d\u0430\u044f \u03b7 \u0432 \u0432\u044b\u0432\u043e\u0434\u0435", None))
        self.label_4.setText(QCoreApplication.translate("SettingsWindow", u"\u041c\u0430\u043a\u0441\u0438\u043c\u0430\u043b\u044c\u043d\u0430\u044f \u03b7 \u0432 \u0432\u044b\u0432\u043e\u0434\u0435", None))
        self.btn_browse_exe.setText(QCoreApplication.translate("SettingsWindow", u"...", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("SettingsWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c\u0441\u043a\u043e\u0433\u043e \u0438\u043d\u0442\u0435\u0440\u0444\u0435\u0439\u0441\u0430", None))
        self.label_16.setText(QCoreApplication.translate("SettingsWindow", u"\u042f\u0437\u044b\u043a", None))
        self.label_15.setText(QCoreApplication.translate("SettingsWindow", u"\u0422\u0435\u043c\u0430", None))
        self.combo_language.setItemText(0, QCoreApplication.translate("SettingsWindow", u"\u0420\u0443\u0441\u0441\u043a\u0438\u0439", None))

        self.combo_gui_theme.setItemText(0, QCoreApplication.translate("SettingsWindow", u"\u0410\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u0438", None))

        self.groupBox_2.setTitle(QCoreApplication.translate("SettingsWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u0440\u0430\u0441\u0447\u0435\u0442\u0430", None))
        self.label_13.setText(QCoreApplication.translate("SettingsWindow", u"\u041c\u0430\u043a\u0441\u0438\u043c\u0430\u043b\u044c\u043d\u043e \u0446\u0438\u043a\u043b\u043e\u0432 \u0443\u0442\u043e\u0447\u043d\u0435\u043d\u0438\u044f", None))
        self.label_10.setText(QCoreApplication.translate("SettingsWindow", u"\u0422\u043e\u0447\u043d\u043e\u0441\u0442\u044c \u0432\u044b\u0447\u0438\u0441\u043b\u0435\u043d\u0438\u0439", None))
        self.combo_device.setItemText(0, QCoreApplication.translate("SettingsWindow", u"\u0426\u0435\u043d\u0442\u0440\u0430\u043b\u044c\u043d\u044b\u0439 \u043f\u0440\u043e\u0446\u0435\u0441\u0441\u043e\u0440 (CPU)", None))

        self.label_2.setText(QCoreApplication.translate("SettingsWindow", u"\u0427\u0438\u0441\u043b\u043e \u043f\u043e\u0442\u043e\u043a\u043e\u0432 \u043f\u0440\u043e\u0446\u0435\u0441\u0441\u043e\u0440\u0430", None))
        self.label_12.setText(QCoreApplication.translate("SettingsWindow", u"\u0420\u0430\u0437\u0440\u0435\u0448\u0435\u043d\u0438\u0435", None))
        self.label_11.setText(QCoreApplication.translate("SettingsWindow", u"\u041f\u043e\u0440\u043e\u0433 \u03b7 \u0443\u0447\u0435\u0442\u0430 \u043e\u043f\u0435\u0440\u0430\u0442\u043e\u0440\u0430", None))
        self.label.setText(QCoreApplication.translate("SettingsWindow", u"\u0420\u0430\u0441\u0447\u0435\u0442\u043d\u043e\u0435 \u0443\u0441\u0442\u0440\u043e\u0439\u0441\u0442\u0432\u043e", None))
        self.btn_cancel.setText(QCoreApplication.translate("SettingsWindow", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
        self.btn_apply.setText(QCoreApplication.translate("SettingsWindow", u"\u041f\u0440\u0438\u043d\u044f\u0442\u044c", None))
    # retranslateUi

