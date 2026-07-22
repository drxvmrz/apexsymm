# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_op_edit.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_OpEditWindow(object):
    def setupUi(self, OpEditWindow):
        if not OpEditWindow.objectName():
            OpEditWindow.setObjectName(u"OpEditWindow")
        OpEditWindow.resize(359, 358)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(OpEditWindow.sizePolicy().hasHeightForWidth())
        OpEditWindow.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(OpEditWindow)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 3, 0, 1, 3)

        self.btn_apply = QPushButton(OpEditWindow)
        self.btn_apply.setObjectName(u"btn_apply")

        self.gridLayout.addWidget(self.btn_apply, 4, 0, 1, 3)

        self.btn_cancel = QPushButton(OpEditWindow)
        self.btn_cancel.setObjectName(u"btn_cancel")

        self.gridLayout.addWidget(self.btn_cancel, 5, 0, 1, 3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 1, 1, 1)

        self.groupBox = QGroupBox(OpEditWindow)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.a31 = QLineEdit(self.groupBox)
        self.a31.setObjectName(u"a31")

        self.gridLayout_2.addWidget(self.a31, 2, 0, 1, 1)

        self.a11 = QLineEdit(self.groupBox)
        self.a11.setObjectName(u"a11")

        self.gridLayout_2.addWidget(self.a11, 0, 0, 1, 1)

        self.a21 = QLineEdit(self.groupBox)
        self.a21.setObjectName(u"a21")

        self.gridLayout_2.addWidget(self.a21, 1, 0, 1, 1)

        self.a23 = QLineEdit(self.groupBox)
        self.a23.setObjectName(u"a23")

        self.gridLayout_2.addWidget(self.a23, 1, 3, 1, 1)

        self.a12 = QLineEdit(self.groupBox)
        self.a12.setObjectName(u"a12")

        self.gridLayout_2.addWidget(self.a12, 0, 2, 1, 1)

        self.a13 = QLineEdit(self.groupBox)
        self.a13.setObjectName(u"a13")

        self.gridLayout_2.addWidget(self.a13, 0, 3, 1, 1)

        self.a22 = QLineEdit(self.groupBox)
        self.a22.setObjectName(u"a22")

        self.gridLayout_2.addWidget(self.a22, 1, 2, 1, 1)

        self.a32 = QLineEdit(self.groupBox)
        self.a32.setObjectName(u"a32")

        self.gridLayout_2.addWidget(self.a32, 2, 2, 1, 1)

        self.a33 = QLineEdit(self.groupBox)
        self.a33.setObjectName(u"a33")

        self.gridLayout_2.addWidget(self.a33, 2, 3, 1, 1)


        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 1)

        self.groupBox_3 = QGroupBox(OpEditWindow)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_3 = QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.combo_op_presets = QComboBox(self.groupBox_3)
        self.combo_op_presets.setObjectName(u"combo_op_presets")

        self.gridLayout_3.addWidget(self.combo_op_presets, 1, 0, 1, 1)

        self.combo_op_presets_category = QComboBox(self.groupBox_3)
        self.combo_op_presets_category.addItem("")
        self.combo_op_presets_category.addItem("")
        self.combo_op_presets_category.addItem("")
        self.combo_op_presets_category.addItem("")
        self.combo_op_presets_category.setObjectName(u"combo_op_presets_category")

        self.gridLayout_3.addWidget(self.combo_op_presets_category, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_3, 2, 0, 1, 3)

        self.groupBox_2 = QGroupBox(OpEditWindow)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.t1 = QLineEdit(self.groupBox_2)
        self.t1.setObjectName(u"t1")

        self.verticalLayout.addWidget(self.t1)

        self.t2 = QLineEdit(self.groupBox_2)
        self.t2.setObjectName(u"t2")

        self.verticalLayout.addWidget(self.t2)

        self.t3 = QLineEdit(self.groupBox_2)
        self.t3.setObjectName(u"t3")

        self.verticalLayout.addWidget(self.t3)


        self.gridLayout.addWidget(self.groupBox_2, 1, 2, 1, 1)

        self.groupBox_4 = QGroupBox(OpEditWindow)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.line_op_name = QLineEdit(self.groupBox_4)
        self.line_op_name.setObjectName(u"line_op_name")

        self.verticalLayout_2.addWidget(self.line_op_name)


        self.gridLayout.addWidget(self.groupBox_4, 0, 0, 1, 3)


        self.retranslateUi(OpEditWindow)

        QMetaObject.connectSlotsByName(OpEditWindow)
    # setupUi

    def retranslateUi(self, OpEditWindow):
        OpEditWindow.setWindowTitle(QCoreApplication.translate("OpEditWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u043e\u043f\u0435\u0440\u0430\u0442\u043e\u0440\u0430", None))
        self.btn_apply.setText(QCoreApplication.translate("OpEditWindow", u"\u041f\u0440\u0438\u043d\u044f\u0442\u044c", None))
        self.btn_cancel.setText(QCoreApplication.translate("OpEditWindow", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
        self.groupBox.setTitle(QCoreApplication.translate("OpEditWindow", u"\u041c\u0430\u0442\u0440\u0438\u0446\u0430 \u043f\u043e\u0432\u043e\u0440\u043e\u0442\u0430", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("OpEditWindow", u"\u041f\u0440\u0435\u0434\u0443\u0441\u0442\u0430\u043d\u043e\u0432\u043b\u0435\u043d\u043d\u044b\u0435 \u043e\u043f\u0435\u0440\u0430\u0442\u043e\u0440\u044b", None))
        self.combo_op_presets.setCurrentText("")
        self.combo_op_presets_category.setItemText(0, QCoreApplication.translate("OpEditWindow", u"\u0422\u0440\u0430\u043d\u0441\u043b\u044f\u0446\u0438\u0438 \u0438 \u0438\u043d\u0432\u0435\u0440\u0441\u0438\u0438", None))
        self.combo_op_presets_category.setItemText(1, QCoreApplication.translate("OpEditWindow", u"\u041e\u0431\u044b\u0447\u043d\u044b\u0435 \u043f\u043e\u0432\u043e\u0440\u043e\u0442\u044b", None))
        self.combo_op_presets_category.setItemText(2, QCoreApplication.translate("OpEditWindow", u"\u0418\u043d\u0432\u0435\u0440\u0441\u0438\u043e\u043d\u043d\u044b\u0435 \u043f\u043e\u0432\u043e\u0440\u043e\u0442\u044b", None))
        self.combo_op_presets_category.setItemText(3, QCoreApplication.translate("OpEditWindow", u"\u041f\u043b\u043e\u0441\u043a\u043e\u0441\u0442\u0438 \u043e\u0442\u0440\u0430\u0436\u0435\u043d\u0438\u044f", None))

        self.combo_op_presets_category.setCurrentText(QCoreApplication.translate("OpEditWindow", u"\u0422\u0440\u0430\u043d\u0441\u043b\u044f\u0446\u0438\u0438 \u0438 \u0438\u043d\u0432\u0435\u0440\u0441\u0438\u0438", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("OpEditWindow", u"\u0422\u0440\u0430\u043d\u0441\u043b\u044f\u0446\u0438\u044f", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("OpEditWindow", u"\u0418\u043c\u044f \u043e\u043f\u0435\u0440\u0430\u0442\u043e\u0440\u0430", None))
    # retranslateUi

