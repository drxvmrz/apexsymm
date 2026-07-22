import os
import sys

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from platformdirs import user_documents_dir

from python.scripts.processing import *
from python.scripts.settings import *

def check_metadata_dir_exists():
    docs_dir = user_documents_dir() 
    msg_box = QMessageBox(QMessageBox.Icon.Critical, "Fatal error!", 
                          f"Не найдена папка {docs_dir}! Как это вообще возможно?")

    if not os.path.exists(docs_dir):
        msg_box.exec()
        exit()

    data_path = os.path.join(docs_dir, "Apexsymm Data")
    if not os.path.exists(data_path):
        os.mkdir(data_path)

    return data_path

def main_loop():
    # Абсолютный путь к файлу main и к содержащей папке
    path_main = __file__
    dir_main = os.path.dirname(path_main)

    # Папка с данными приложения (в документы обычно падает)
    app = QApplication(sys.argv)
    data_dir = check_metadata_dir_exists()

    # Пути к иконке и файлу пресетов операторов
    path_file_icon = os.path.join(dir_main, "icon.png")
    path_file_ops_presets = os.path.join(dir_main, "presets")

    # Пусть к файлу настроек (по умолчанию он не создан)
    path_file_settings = os.path.join(data_dir, "settings")

    app.setWindowIcon(QIcon(path_file_icon))

    # Загружаем настройки из файла
    settings = Settings(path_file_settings, dir_main)
    settings.init_settings()
    settings.load_settings()
    processor = Processor(settings)

    # Рисуем окна
    sets_win = SettingsWindow(settings)
    main_win = MainWindow(sets_win, processor)
    op_edit_win = EditOpWindow(main_win, path_file_ops_presets)

    # Окно редактирования операторов и главное окно у нас связаны
    # Теперь свяжем в другую сторону, теперь они взаимосвязаны
    main_win.set_edit_op_win(op_edit_win)
    main_win.setWindowTitle("Apexsymm GUI")
    main_win.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main_loop()


