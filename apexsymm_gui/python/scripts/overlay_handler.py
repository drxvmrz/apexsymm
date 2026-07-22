"""
Этот оверлей как загрузочный экран на время расчета
На нем есть прогресс-бар и кнопка остановки

Он закрывает собой весь интерфейс
"""

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from ..gui.gui_overlay import *
from ..gui.gui_progress_bar import *

class OverlayWidget(QWidget):
    def __init__(self, parent: QWidget, progress_widget: CustomProgressBar):
        super().__init__(parent)

        self.parent_cent_widget = parent
        self.parent_cent_widget.installEventFilter(self)

        # Тут будем хранить блюр-эффект
        self.blur = None

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Там была затычка-лейбл, удаляем и вставляем наш прогресс-бар
        self.ui.progress_widget.setParent(None)
        self.ui.progress_widget = progress_widget
        self.ui.gridLayout_2.addWidget(self.ui.progress_widget, 1, 1, 1, 4)

        # Чтобы заблокировать основной интерфейс
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)        

        #self.ui.background_widget.setStyleSheet("""background-color: rgba(255, 255, 255, 255);""")

        # Изначально он не нужен - скроем
        self.hide()
    
    def _set_blur_main_window(self, enable: bool):
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(10)
        self.blur = blur_effect

        splitter = self.parent_cent_widget.findChildren(QSplitter)[0]

        if enable:
            splitter.setGraphicsEffect(self.blur)
        else:
            splitter.setGraphicsEffect(None)

    def _00set_blur_main_window(self, enable: bool):
        gr_boxes = self.parent_cent_widget.findChildren(QGroupBox)

        self.blurs = []
        for i in range(len(gr_boxes)):
            blur_effect = QGraphicsBlurEffect()
            blur_effect.setBlurRadius(30)
            self.blurs.append(blur_effect)

        if enable:
            for i in range(len(gr_boxes)):
                gr_boxes[i].setGraphicsEffect(self.blurs[i])
        else:
            for i in range(len(gr_boxes)):
                gr_boxes[i].setGraphicsEffect(None)

    def show(self):
        self._set_blur_main_window(True)
        return super().show()
    
    def hide(self):
        self._set_blur_main_window(False)
        return super().hide()

    def eventFilter(self, watched: QWidget, event: QEvent):
        if event.type() == QEvent.Type.Resize:
            self.updateGeometry()
        return super().eventFilter(watched, event)

    def updateGeometry(self):
        if self.parent():
            self.setGeometry(self.parent_cent_widget.rect())
    
    def showEvent(self, event):
        self.updateGeometry()
        # Это я показываю QWidget
        super().showEvent(event)

