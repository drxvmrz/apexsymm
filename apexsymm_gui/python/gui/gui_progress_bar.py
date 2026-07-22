"""
Имеюстя проблемы с отображением QProgressBar на MacOSX
По крайней мере на PySide6, на MacOS 26 (M2).

Причем с виджетами, типа QLabel никаких проблем нет,
Да и с самим QProgressBar на более старых версиях нет никаких проблем!

Поэтому пока сделаем кастомный прогресс-бар и используем его.
Прогресс-бар необходим, так как я очень их люблю :)
"""

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class CustomProgressBar(QLabel):
    def __init__(self, width=150, height=16):
        super().__init__()       
        self.setMinimumSize(width, height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self._value = 0
        self._maximum = 100
        self.setText("")

        # Стиль для видимости
        self.setStyleSheet("""
            background-color: #E0E0E0;
            border: 1px solid #A0A0A0;
            border-radius: 8px;
        """)

    def setValue(self, value):
        self._value = max(0, min(value, self._maximum))
        self.update()

    def setMaximum(self, value):
        self._maximum = value

    def paintEvent(self, event):
        super().paintEvent(event)

        if self._value > 0:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)

            # Рисуем прогресс
            progress_width = (self.width() - 4) * self._value / self._maximum
            progress_rect = self.rect().adjusted(2, 2, -2, -2)
            progress_rect.setWidth(progress_width)

            # Градиент для прогресса
            gradient = QLinearGradient(progress_rect.topLeft(), progress_rect.topRight())
            gradient.setColorAt(0, QColor("#007AFF"))
            gradient.setColorAt(1, QColor("#0056CC"))

            painter.setBrush(gradient)
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(progress_rect, 6, 6)

            # Текст прогресса
            painter.setPen(QColor("#FFFFFF"))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, f"{self._value}%")