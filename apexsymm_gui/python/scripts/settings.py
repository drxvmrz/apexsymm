import os
import sys

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from .io import *

from ..gui.gui_settings_window import *

def get_core_exec_name():
    if ("win32" in sys.platform) or ("win64" in sys.platform): 
        return "apexcore_win.exe"
    elif ("linux" in sys.platform):
        return "apexcore_linux"
    elif ("darwin" in sys.platform):
        return "apexcore_mac"
    else: 
        ErrorWindow.invoke_error("Unknown platform", "Неизвестная операционная система. ", 
                                 "Невозможно запустить расчетное ядро, так как это неизвестная операционная система. " \
                                 "Доступны версии для Windows, MacOS и Linux. Для Вашей операционной системы соберите ядро из исходного кода или напишите нам. " \
                                 "Мы постараемся собрать его для Вас :).")
        exit()
        return ""

class Settings():
    def __init__(self, settings_file_path, main_path):
        self.main_dir_path = main_path
        self.settings_file_path = settings_file_path

        ### Настройки самого интерфейса (GUI PREFERENCES)
        self.gui_theme = 0 # Тема интерфейса (темная/светлая)
        self.language = 0 # Язык интерфейса

        ### Настройки самого gui-приложения (SYSTEM SETTINGS)
        self.minimum_out_eta = 0.0 # Минимальная Ета для вывода в таблицу операторов, при уточнении, а не расчете
        self.maximum_out_eta = 0.0 # Максимальная Ета для вывода в таблицу операторов, при уточнении, а не расчете
        self.maxoutput = 0 # Число операторов для включения в таблицу вывода
        self.json_path = "" # Путь к файлу, который будет хранить результаты (.json, который выплевывает pss2)
        self.exec_path = "" # Путь к исполняемому файлу pss2

        ### Настройки расчета (CALCULATION SETTINGS)
        self.device = 0 # Просто сам девайс, типа CPU (0) или GPU (1)
        self.device_name = "" # Имя процессора или видеокарты, на всякий пожарный, да и это просто прикольно
        self.cpus = 0 # Максимальное число ядер ПРОЦЕССОРА для расчета (не знаю, есть ли такая настройка для ГПУ)
        self.precision = 0.0 # Точность
        self.theshold = 0.0 # Порог значения эта для рассмотрения оператора
        self.resolution = 0.0 # Разрешение в обратных ангстремах
        self.max_cycles = 0 # Максимальное число циклов уточнения

    def set_setting_file_path(self, new_path: str):
        self.settings_file_path = new_path

    def get_setting_file_path(self):
        return self.settings_file_path
    
    ######### Настройки самого интерфейса программы #########
    def set_gui_theme(self, num: int):
        """
        Установить тему интерфейса:
        Число - это индекс в checkbox'е
        0 - светлая тема
        1 - темная тема (пока в разработке)
        """
        self.gui_theme = num

    def get_gui_theme(self):
        return self.gui_theme

    def set_language(self, num: int):
        """
        Установить язык интерфейса:
        Число - это индекс в checkbox'е
        0 - Английский
        """
        self.language = num
    
    def get_language(self):
        return self.language

    ######### Системные настройки (то есть настройки самой gui-программы) #########
    def set_maximum_out_eta(self, value: float):
        """
        Установить максимальную эту, с которой выводить операторы в таблицу
        Например, операторы с 1.000 не нужны, их можно не выводить (ну условно)
        """
        self.maximum_out_eta = value

    def get_maximum_out_eta(self):
        return self.maximum_out_eta

    def set_minimum_out_eta(self, value: float):
        """
        Установить минимальную эту, с которой выводить операторы в таблицу
        """
        self.minimum_out_eta = value

    def get_minimum_out_eta(self):
        return self.minimum_out_eta
    
    def set_max_out(self, count: int):
        """
        Установить максимальное количество операторов, которое выведется в таблицу
        """
        self.maxoutput = count

    def get_max_out(self):
        return self.maxoutput

    def set_json_path(self, path: str):
        """
        Установить путь к .json-файлу с результатами,
        Который выплевывает сама программа pss2
        """
        self.json_path = path

    def get_json_path(self):
        return self.json_path
    
    def set_exec_path(self, path):
        """
        Установить путь к исполняемому файлу pss2
        """
        self.exec_path = path

    def get_exec_path(self):
        return self.exec_path

    ######### Расчетные настройки #########
    def set_device(self, name: int):
        """
        Установить устройство, выполняющее вычисления:
        0 - процессор 
        1 - видеокарта
        """
        self.device = name

    def get_device(self):
        return self.device

    def set_device_name(self, name: str):
        """
        Установить имя (название) считающего устройство
        Например: имя процессора (но пока не работает)
        """
        self.device_name = name

    def get_device_name(self):
        return self.device_name

    def set_max_cpus(self, max_CPUs_num: int):
        """
        Установить максимальное используемое число ядер процессора для расчета
        Не меньше 0 и не больше максимально допустимого числа
        """
        if max_CPUs_num < 0: raise ValueError("Max CPUs must be more than zero!")
        self.cpus = max_CPUs_num

    def get_max_cpus(self):
        return self.cpus

    def set_resolution(self, value: float):
        """
        Установить разрешение по Фурье-карте
        """
        self.resolution = value
    
    def get_resolution(self):
        return self.resolution
    
    def set_threshold(self, value: float):
        """
        Установить пороговое значение эта, ниже которой операторы будут отбрасываться
        """
        self.theshold = value
    
    def get_threshold(self):
        return self.theshold

    def set_precision(self, value: float):
        """
        Установить точность расчета при уточнении трансляций операторов
        """
        self.precision = value

    def get_precision(self):
        return self.precision
    
    def set_max_ref_cycles(self, value: int):
        """
        Установить максимальное число циклов уточнения, 
        после которых оператор будет отбрасываться как неуточненный
        """
        self.max_cycles = value

    def get_max_ref_cycles(self):
        return self.max_cycles

    # Если вдруг нет файла с настройками (например, при первом запуске), то их надо инициализировать
    def init_settings(self):
        """
        Инициализирует настройки по умолчанию, если файл с настройками отсутствует или поврежден
        """
        # Если файл есть, то все-таки ничего инициализировать не надо
        if os.path.exists(self.settings_file_path): return
        
        # Настройки интерфейса по умолчанию
        self.set_gui_theme(0)
        self.set_language(0)

        # СИСТЕМНЫЕ НАСТРОЙКИ по умолчанию
        self.set_maximum_out_eta(1.0)
        self.set_minimum_out_eta(0.0)
        self.set_max_out(200)

        json_path = os.path.normpath(os.path.join(os.path.dirname(self.settings_file_path), "last_results.json"))
        self.set_json_path(json_path) 

        exec_path = os.path.normpath(os.path.join(self.main_dir_path, "core", get_core_exec_name()))
        self.set_exec_path(exec_path)

        # РАСЧЕТНЫЕ НАСТРОЙКИ по умолчанию
        self.set_device(0)
        self.set_max_cpus(os.cpu_count())
        self.set_precision(10E-8)
        self.set_threshold(0.2)
        self.set_resolution(0.5)
        self.set_max_ref_cycles(10)

        # Создаем файл с сохраненными настройками
        self.save_settings()

    # Сохраняет настройки в файл
    def save_settings(self):
        """
        Сохраняет текущие настройки в файл настроек
        """
        with open(self.settings_file_path, "w") as file:
             file.write(f"# GUI Prefs\n"
                        f"theme={self.get_gui_theme()}\n"
                        f"lang={self.get_language()}\n"
                        f"# System settings\n"
                        f"maxoeta={self.get_maximum_out_eta()}\n"
                        f"minoeta={self.get_minimum_out_eta()}\n"
                        f"maxout={self.get_max_out()}\n"
                        f"json_path={self.get_json_path()}\n"
                        f"exec_path={self.get_exec_path()}\n"
                        f"# Calculation settings\n"
                        f"device={self.get_device()}\n"
                        f"cpus={self.get_max_cpus()}\n"
                        f"precision={self.get_precision()}\n"
                        f"threshold={self.get_threshold()}\n"
                        f"resolution={self.get_resolution()}\n"                     
                        f"refcycles={self.get_max_ref_cycles()}\n")

    # Загружает настройки из файла в объект настроек
    def load_settings(self):
        """
        Загружает текущие настройки из файла настроек
        """
        with open(self.settings_file_path, "r") as file:
            file_lines = file.readlines()
            for line in file_lines:
                # Это комментарии, они не нужны
                if line.startswith("#"): continue

                line = line.split("=")
                # НАСТРОЙКИ ИНТЕРФЕЙСА ПРОГРАММЫ
                if line[0] == "theme":
                    self.set_gui_theme(int(line[1]))
                elif line[0] == "lang":
                    self.set_language(int(line[1]))
                # СИСТЕМНЫЕ НАСТРОЙКИ
                elif line[0] == "maxoeta":
                    self.set_maximum_out_eta(float(line[1]))
                elif line[0] == "minoeta":
                    self.set_minimum_out_eta(float(line[1]))
                elif line[0] == "maxout":
                    self.set_max_out(int(line[1]))
                elif line[0] == "json_path":
                    self.set_json_path(line[1].replace("\n",""))
                elif line[0] == "exec_path":
                    self.set_exec_path(line[1].replace("\n",""))
                # РАСЧЕТНЫЕ НАСТРОЙКИ
                elif line[0] == "device":
                    self.set_device(int(line[1]))
                elif line[0] == "cpus":
                    self.set_max_cpus(int(line[1]))
                elif line[0] == "precision":
                    self.set_precision(float(line[1]))
                elif line[0] == "threshold":
                    self.set_threshold(float(line[1]))
                elif line[0] == "resolution":
                    self.set_resolution(float(line[1]))
                elif line[0] == "refcycles":
                    self.set_max_ref_cycles(int(line[1]))
                else:
                    print("UNKNOWN SETTINGS OPTION")
                    exit(1)

class SettingsWindow(QWidget):
    need_to_redraw_results = Signal()

    def __init__(self, settings: Settings):
        # Передаем объект настроек, ведь работать-то это окно будет именно с ними
        self.settings = settings

        # init GUI
        super().__init__()
        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Settings")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        
        self.ui.spin_cpus.setMaximum(os.cpu_count())
        self.ui.spin_cpus.setMinimum(0)

        # Все кнопки в окне настроек
        self.ui.btn_apply.clicked.connect(self.apply_settings)
        self.ui.btn_cancel.clicked.connect(self.cancel_settings)

        self.ui.btn_browse_json.clicked.connect(self.choose_json_path)
        self.ui.btn_browse_exe.clicked.connect(self.choose_exe_path)

    # Отрисовка текущих значений настроек в окне настроек
    def draw_settings_values(self):
        """
        Отрисовывает текущие значения настроек в окне настроек
        """
        # Отрисовка значений настроек интерфейса программы
        self.ui.combo_gui_theme.setCurrentIndex(self.settings.get_gui_theme())
        self.ui.combo_language.setCurrentIndex(self.settings.get_language())

        # Отрисовка системных настроек (самой программы-отрисовщика)
        self.ui.spin_max_eta_out.setValue(self.settings.get_maximum_out_eta())
        self.ui.spin_min_eta_out.setValue(self.settings.get_minimum_out_eta())
        self.ui.spin_max_ops_out.setValue(self.settings.get_max_out())
        self.ui.line_json_path.setText(self.settings.get_json_path())
        self.ui.line_exec_path.setText(self.settings.get_exec_path())

        # Отрисовка расчетных настроек
        self.ui.combo_device.setCurrentIndex(self.settings.get_device())
        self.ui.spin_cpus.setValue(self.settings.get_max_cpus())
        self.ui.line_precision.setText(str(self.settings.get_precision()))
        self.ui.spin_threshold.setValue(self.settings.get_threshold())
        self.ui.spin_resolution.setValue(self.settings.get_resolution())
        self.ui.spin_ref_cycles.setValue(self.settings.get_max_ref_cycles())

    def apply_settings(self):
        """
        Кнопка apply меню настроек. Применяет текущие настройки
        И потом заодно сохраняет их в файл настроек
        """
        # Критические места
        precision = 0.0
        line_json_path = ""
        line_exec_path = ""

        try:
            precision = float(self.ui.line_precision.text().replace("\n",""))
        except:
            ErrorWindow.invoke_error("Неверное значение","Точность должна числом")
            return

        if(os.path.exists(os.path.dirname(self.ui.line_json_path.text().replace("\n","")))):
            line_json_path = self.ui.line_json_path.text()
        else:
            ErrorWindow.invoke_error("Неверный путь","Данный путь не существует")
            return
        
        if(os.path.exists(self.ui.line_exec_path.text().replace("\n",""))):
            line_exec_path = self.ui.line_exec_path.text()
        else:
            ErrorWindow.invoke_error("Неверный путь к исполняемому файлу","Данный путь не существует или файл по данному пути поврежден")
            return

        # Сохраняет в объект настроек настройки интрефейса самой программы
        self.settings.set_gui_theme(self.ui.combo_gui_theme.currentIndex())
        self.settings.set_language(self.ui.combo_language.currentIndex())

        # Сохраняем системные настройки в объект
        old_maximum = self.settings.get_maximum_out_eta() # Если вдруг значения не совпадают, то надо бы перерисовать
        old_minimum = self.settings.get_minimum_out_eta() # Если вдруг значения не совпадают, то надо бы перерисовать
        self.settings.set_maximum_out_eta(self.ui.spin_max_eta_out.value())
        self.settings.set_minimum_out_eta(self.ui.spin_min_eta_out.value())
        self.settings.set_max_out(self.ui.spin_max_ops_out.value())
        self.settings.set_json_path(line_json_path)
        self.settings.set_exec_path(line_exec_path)

        if (self.settings.get_maximum_out_eta() != old_maximum) or \
        (self.settings.get_minimum_out_eta() != old_minimum):
            self.need_to_redraw_results.emit()

        # Сохраняем расчетные настройки в объект
        self.settings.set_device(self.ui.combo_device.currentIndex())
        self.settings.set_max_cpus(self.ui.spin_cpus.value())
        self.settings.set_precision(precision)
        self.settings.set_threshold(self.ui.spin_threshold.value())
        self.settings.set_resolution(self.ui.spin_resolution.value())
        self.settings.set_max_ref_cycles(self.ui.spin_ref_cycles.value())

        # Сохраняем настройки еще и в файл
        self.settings.save_settings()
        self.hide()

    def cancel_settings(self):
        """
        Кнопка отмены - просто закрывает окно настроек и ничего не меняет
        """
        self.hide()

    def choose_json_path(self):
        """
        Выбор пути к папке, в которой хранятся результаты расчетов (по умолчанию results.json)
        """
        save_dir = QFileDialog.getExistingDirectory(caption="Get results .json-file directory")

        if save_dir != "" and save_dir != None and os.path.exists(save_dir):
            save_dir += "/results.json"
            self.ui.line_json_path.setText(save_dir)
            self.settings.set_json_path(save_dir)

    def choose_exe_path(self):
        """
        Выбор исполняемого файла pss2 (или pss2.exe)
        """
        exe_path = QFileDialog.getOpenFileName(caption="Choose execution kernel file",
                                               filter="All Files (*)")
        if os.path.exists(exe_path[0]):
            self.ui.line_exec_path.setText(exe_path[0])
            self.settings.set_exec_path(exe_path[0])

