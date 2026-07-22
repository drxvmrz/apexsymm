import os
import sys
import time
import subprocess
import json

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from .settings import *
from .pss_types import *
from .io import *
from .metadata import *
from .overlay_handler import *

from ..gui.gui_progress_bar import *
from ..gui.gui_main_window import *
from ..gui.gui_operators_edit import *

# Отдельный рабочий поток для запуска pps2
class ProcessWorker(QThread):
    # Сигналы об изменении прогресса, работе и завершении расчета
    started = Signal()
    finished = Signal()
    is_done = Signal()
    failed = Signal()
    progress_updated = Signal(int)

    def __init__(self):
        super().__init__()
        self.process = QProcess()
        self.args = []
        self.should_stop = False
        self.logs = ""

        self.process.started.connect(self.process_started)
        self.process.finished.connect(self.process_finished)
        self.process.errorOccurred.connect(self.process_error_occured)
        self.process.readyReadStandardOutput.connect(self.out_stdcout)

    @staticmethod
    def _extract_progress_from_stdout(std_out: str):
        progress = -1
        cnt = std_out.count("PROGRESS: ")
        if cnt > 0:
            split_out = std_out.split("\n")
            for part in split_out:
                if part.startswith("PROGRESS: "):
                    split_part = part.split()
                    progress = int(round(float(split_part[1].replace("\n", "").replace("%", ""))))
                    break
        return progress

    def out_stdcout(self):
        data = self.process.readAllStandardOutput()
        try:
            std_out = bytes(data).decode('utf-8')
            current_progress = ProcessWorker._extract_progress_from_stdout(std_out)
            self.logs += std_out
            self.progress_updated.emit(current_progress)
            print(std_out)
        except:
            return

    def run(self):
        if self.process.state() == self.process.ProcessState.NotRunning:
            self.process.start(self.args[0], self.args[1:])
            self.progress_updated.emit(0)
            self.exec_()

    def stop(self):
        if self.process.state() == self.process.ProcessState.Running:
            self.should_stop = True
            if sys.platform == "win32" or sys.platform == "win64":
                self.process.kill()
            else:
                self.process.terminate()
            self.process.waitForFinished(100)
    
    def process_error_occured(self):
        if self.process.state() == self.process.ProcessState.NotRunning and not self.should_stop:
            self.failed.emit()

    def process_started(self):
        if self.process.state() == self.process.ProcessState.Running:
            self.started.emit()
        
    def process_finished(self):
        if self.process.state() == self.process.ProcessState.NotRunning:
            self.finished.emit()
            if self.should_stop == False:
                self.progress_updated.emit(100)
                self.is_done.emit()
                self.quit()
            self.should_stop = False


class Processor(QObject):
    results_collected = Signal()

    def __init__(self, settings: Settings):
        # Объект настроек
        super().__init__()
        self.settings = settings
        
        # Путь к .cif-файлу
        self.cif_path = ""

        # Флаги быстрых настроек расчета. Они находятся в главном окне, прям около кнопки "RUN"
        self.no_hydro = False
        self.calc_only = False
        self.use_supercell = False
        self.supercell_radius = 0

        # Массив структур в данной сессии работы программы
        # Операторы, которые будут использоваться в расчетах программы
        self.operators_to_calc = []
        
        # Аргументы командной строки для запуска pss2
        # И работа непосредственно с воркером, который запускает pss2
        self.pss2_args = []
        self.process_worker = ProcessWorker()
        self.process_worker_works = False

        # Сборщик данных 
        self.json_data = JSONReader(self.settings.get_json_path())

        # Сигналы
        self.process_worker.started.connect(self.process_worker_started)
        self.process_worker.finished.connect(self.process_worker_finished)
        self.process_worker.is_done.connect(self.process_worker_is_done)

    def _operators_to_calc(self):
        ops_args = ""

        if len(self.operators_to_calc) == 1:
            return self.operators_to_calc[0].to_string_arg()
        else:
            for i in self.operators_to_calc:
                ops_args += i.to_string_arg() + ";"
            # Удаляем последний знак ';'
            return ops_args[:-1]

    def assemble_args(self):
        args = self.pss2_args
        sets = self.settings

        # Очищаем список текущих аргументов, чтобы они не накладывались каждый запуск
        args.clear()

        # necessary args
        args.append(self.settings.get_exec_path()) # Главный аргумент - запуск программы, путь к ней
        args.append(self._operators_to_calc()) # ну и строка из операторов для расчета
        args.append(self.cif_path) # путь к cif-файлу

        # options
        args.extend(["--resolution", f"{sets.get_resolution()}"])
        args.extend(["--threshold", f"{sets.get_threshold()}"])
        args.extend(["--precision", f"{sets.get_precision()}"])
        args.extend(["--cycles", f"{sets.get_max_ref_cycles()}"])
        args.extend(["--maxthreads", f"{sets.get_max_cpus()}"])
        args.extend(["--json", f"{sets.get_json_path()}"])
        
        if self.use_supercell: args.extend(["--supercell", f"{self.supercell_radius}"])

        # flags
        if self.no_hydro: args.append("--nohydro")
        if self.calc_only: args.append("--norefine")

        # Передаем аргументы также в воркер
        self.process_worker.args = args        

    def process_worker_started(self):
        if self.process_worker.process.state() == QProcess.ProcessState.Running:
            self.process_worker_works = True

    def process_worker_finished(self):
        self.process_worker_works = False

        json_path = self.settings.get_json_path()
        if os.path.exists(json_path):
            self.collect_results()

    def process_worker_is_done(self):
        if (not self.process_worker_works) and \
        (self.process_worker.process.state() == QProcess.ProcessState.NotRunning):
            exit_code = self.process_worker.process.exitCode()
            if exit_code == 0: # Нормальное завершение работы
                return
            elif exit_code == 100: # Неверный ввод параметров командной строки
                ErrorWindow.invoke_error("Неверный ввод параметров запуска",
                                         "Параметры запуска, переданные в исполняемый файл переданы неверно, либо не существуют", 
                                         "Для исправления данной ошибки попробуйте вернуться на предыдущую версию программы")
            elif exit_code == 101: # cif-файл по данному пути не найден
                ErrorWindow.invoke_error("Неверный путь к .cif-файлу или файлам",
                                         "Выбранный .cif-файл не существует или выбранная папка их не содержит", 
                                         "Выберите другой .cif-файл или папку")
            elif exit_code == 102: # cif-файл поврежден
                ErrorWindow.invoke_error("Неверный путь к .cif-файлу",
                                         "Выбранный .cif-файл поврежден", 
                                         "Выберите другой .cif-файл или исправьте данный.")
            elif exit_code == 103: # Нет структур, пригодных для расчета
                ErrorWindow.invoke_error("Нет структур для расчета",
                                         "Выбранный .cif-файл не содержит пригодных для расчета структур", 
                                         "Вероятно, структуры содержат не полную информацию. Например, отсутствуют атомы или параметры ячейки. " \
                                         "Выберите другой .cif-файл или исправьте данный.")
            else: # Любая неизвестная ошибка (любой другой код выхода, кроме 0)
                ErrorWindow.invoke_error("Неизвестная ошибка",
                                         "Произошла неизвестная ошибка запуска", 
                                         "Попробуйте переустановить программу или вернуться на предыдущую рабочую версию")

    def collect_results(self):
        self.json_data = JSONReader(self.settings.get_json_path())
        self.json_data.load_structures()
        self.results_collected.emit()
        

class MainWindow(QMainWindow):
    def __init__(self, sets_win: SettingsWindow, processor: Processor):
        # Изначально не передается окно редактирования, его надо присвоить!
        self.edit_op_win = None

        # Если идет расчет, то ничего, кроме кнопки stop не должно быть доступно

        # Передаем окно настроек
        self.sets_win = sets_win
        # А также процессор, который управляет ходом работы ядра
        self.processor = processor

        # init GUI
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.table_results.setSortingEnabled(True)
        self.ui.status_bar.showMessage("Not running")
        

        # drag-n-drop
        self.setAcceptDrops(True)
        self.installEventFilter(self)

        # Прогресс-бар
        self.progress_bar = CustomProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(100)

        # Расчетный оверлей
        self.overlay = OverlayWidget(self.ui.centralwidget, self.progress_bar)
        # Сигнал нажатия на кнопку стоп
        self.overlay.ui.btn_stop.clicked.connect(self.run_stop)

        # Начальное состояние спинбокса супер-ячейки и меню "остановить" - выключены
        self.ui.spin_supcell_radius.setEnabled(False)
        self.ui.action_stop.setEnabled(False)

        self.ui.action_settings.triggered.connect(self.open_settings_window)
        self.ui.btn_settings.clicked.connect(self.open_settings_window)

        # Виджеты из груп-бокса "предустановки и запуск"
        self.ui.btn_open_cif_file.clicked.connect(self.choose_cif_file)
        self.ui.action_open_cif_file.triggered.connect(self.choose_cif_file)
        self.ui.action_open_cif_folder.triggered.connect(self.choose_cif_folder)
        self.ui.line_cif_path.textChanged.connect(self.change_cif_line_text)
        self.ui.check_calc_only.stateChanged.connect(self.check_calc_only)
        self.ui.check_use_supcell.stateChanged.connect(self.check_super_cell)
        self.ui.spin_supcell_radius.valueChanged.connect(self.check_super_cell_changed)

        self.ui.btn_run.clicked.connect(self.run_stop)
        self.ui.action_run.triggered.connect(self.run_stop)
        self.ui.action_stop.triggered.connect(self.run_stop)

        # Групбокс со структурами и результатами расчета для них
        self.ui.combo_box_structures.currentIndexChanged.connect(self.draw_results)
        self.ui.btn_open_res_json.clicked.connect(self.open_res_json)
        self.ui.action_open_res_json.triggered.connect(self.open_res_json)
        self.ui.btn_save_csv.clicked.connect(self.save_into_csv)
        self.ui.action_save_csv.triggered.connect(self.save_into_csv)
        self.ui.btn_save_json.clicked.connect(self.unload_json)
        self.ui.action_save_json.triggered.connect(self.unload_json)

        # Виджеты для управления операторами
        self.ui.btn_add_op.clicked.connect(self.add_operator)
        self.ui.btn_edit_op.clicked.connect(self.edit_operator)
        self.ui.btn_remove_op.clicked.connect(self.remove_operator)
        self.ui.btn_remove_all_op.clicked.connect(self.remove_all_operators)
        self.ui.list_ops.itemDoubleClicked.connect(self.edit_operator)

        self.ui.btn_open_opl.clicked.connect(self.open_olf)
        self.ui.btn_save_opl.clicked.connect(self.save_olf)
        self.ui.action_open_opl.triggered.connect(self.open_olf)
        self.ui.action_save_opl.triggered.connect(self.save_olf)

        # меню помощи
        self.ui.action_open_manual.triggered.connect(self.show_manual)
        self.ui.action_about.triggered.connect(self.show_about)

        # Пользовательские сигналы (МОИИ!)
        self.processor.process_worker.finished.connect(self.process_finished)
        self.processor.process_worker.failed.connect(self.process_failed)
        self.processor.process_worker.progress_updated.connect(self.draw_progress)
        self.processor.results_collected.connect(self.fill_structs_combo)
        self.sets_win.need_to_redraw_results.connect(self.redraw_results)

    ################# Служебные функции
    
    def _operators_exists(self):
        if self.ui.list_ops.count() < 1:
            ErrorWindow.invoke_info("Нет операторов", "Операторы для расчета псевдосимметрии отсутствуют.", 
                                    "Для того, чтобы добавить операторы, нажмите 'Add' или откройте .olf-файл.")
            return False
        return True

    def _cif_path_exists(self):
        path = self.processor.cif_path

        self.processor.process_worker.logs += f"Trying open {path}\n"
        is_cif_folder = path.endswith("*")

        if os.path.exists(path) and not is_cif_folder:
            return True
        elif os.path.exists(os.path.dirname(path)) and is_cif_folder:
            return True
        else:
            ErrorWindow.invoke_info("Не удается открыть .cif-файл или папку", "Файлы .cif не найдены или повреждены", 
                                    "Выберите другой файл, нажав 'open .cif-file' или проверьте текущий на наличие ошибок.")
            self._save_logs()
            return False

    def _execution_file_exists(self):
        path = self.processor.settings.exec_path
        if not os.path.exists(path):
            ErrorWindow.invoke_error("Не найден исполняемый файл","Исполняемый файл pss2 не найден."
                                     "Путь к исполняемому файлу, указанный в настройках, не указывает на него. Проверьте указанный путь и перезапустите расчет. " \
                                     "В противном случае, попробуйте переустановить программу.")
            return False
        else:
            return True

    def _is_executable(self):
        """
        Проверяет, отмечен ли файл pss2(.exe) как исполняемый или является ли исполняемым
        Например, в unix надо иногда ввести 'sudo chmod +x <путь к файлу>'
        """
        file_info = QFileInfo(self.processor.settings.exec_path)
        if file_info.isExecutable():
            return True
        else:
            if sys.platform != "win32" and sys.platform != "win64":
                ErrorWindow.invoke_error("Ошибка запуска","Файл, указанный как исполняемый, не является таковым.",
                                         "Выберите другой файл, переустановите программу, или в случае Вашей операционной системы " \
                                         "можно попробовать отдельно выполнить команду " \
                                         "'sudo chmod +x <путь к pss2>'. Затем перезапустите расчет.")
            else:
                ErrorWindow.invoke_error("Ошибка запуска","Файл, указанный как исполняемый, не является таковым.",
                                         "Выберите другой файл или попробуйте переустановить программу.")
            return False

    def _wrong_json(self):
        ErrorWindow.invoke_warning("Ошибка чтения .json-файла","Файл не содержит результатов расчета pss2 или был поврежден.",
                                   "Выберите другой файл, или создайте новый путем запуска расчета.")

    def _redraw_operators(self):
        """
        Перерисовывает в QListView главного окна (self) все операторы
        из self.processor.operators_to_calc
        """
        ops = self.processor.operators_to_calc
        if len(ops) > 0:
            self.ui.list_ops.clear()
            for op in ops:
                new_op_list_item = QListWidgetItem(f"{op.name} | ({op.translation[0]:.3f} {op.translation[1]:.3f} {op.translation[2]:.3f})")
                self.ui.list_ops.addItem(new_op_list_item)

    # Связать главное окно с окном изменения оператора
    def set_edit_op_win(self, edit_operators_window):
        self.edit_op_win = edit_operators_window

    def _read_olf_file(self, path: str):
        if path != "" and path is not None:
            opener = OLFIO(path)
            opener.open_file()
            self.processor.operators_to_calc = opener.get_operators_to_calc()
            self._redraw_operators()

    def _read_res_json_file(self, path: str):
        if path != "" and path is not None:
            # Вдруг откроем не тот json, или что-то с ним будет не так?!
            try:
                self.processor.json_data = JSONReader(path)
                self.processor.json_data.load_structures()
                self.fill_structs_combo()
            except:
                self._wrong_json()

    def _is_valid_drop(self, widget: QWidget, urls: list[QUrl]):
        """
        Определяет, соответствует ли drop-объект данному виджету
        Возвращает соответствующий bool 
        """
        valid = False

        if len(urls) != 1: return valid

        path = urls[0].toLocalFile()
        is_dir = os.path.isdir(path)
        
        return (path.endswith(".cif") or is_dir) or path.endswith(".olf") or path.endswith(".json")

    ################# Реализация класса

    # Для drag-n-drop
    def eventFilter(self, obj: QWidget, event: QEvent | QDragEnterEvent | QDropEvent):
        if event.type() == QEvent.Type.DragEnter:
            if event.mimeData().hasUrls():
                urls = event.mimeData().urls()
                if self._is_valid_drop(obj, urls):
                    event.acceptProposedAction()
        elif event.type() == QEvent.Type.Drop:
            if event.mimeData().hasUrls():
                urls = event.mimeData().urls()
                file_path = urls[0].toLocalFile()
                is_dir = os.path.isdir(file_path)

                if file_path.endswith("cif") or is_dir:
                    if is_dir:
                        if file_path.endswith("/") or file_path.endswith("\\"):
                            self.ui.line_cif_path.setText(f"{file_path}*")
                        else:
                            self.ui.line_cif_path.setText(f"{file_path}/*")
                    else:
                        self.ui.line_cif_path.setText(file_path)
                elif file_path.endswith(".olf"):
                    self._read_olf_file(file_path)
                elif file_path.endswith(".json"):
                    self._read_res_json_file(file_path)
                event.acceptProposedAction()

        return super().eventFilter(obj, event)

    def add_operator(self):
        self.edit_op_win.edit_index = -1
        self.edit_op_win.show()

    def remove_operator(self):
        index = self.ui.list_ops.currentRow()
        count = self.ui.list_ops.count()

        # Если ничего не выделено, то удаляем последний
        if index == -1:
            if count > 0:
                self.ui.list_ops.takeItem(count-1)
                self.processor.operators_to_calc.pop()
        # Ну или же выделенный
        else:
            self.ui.list_ops.takeItem(index)
            del self.processor.operators_to_calc[index]

    def remove_all_operators(self):
        self.ui.list_ops.clear()
        self.processor.operators_to_calc.clear()

    def edit_operator(self):
        selected_index = self.ui.list_ops.currentRow()
        if selected_index > -1:
            self.edit_op_win.edit_index = selected_index
            self.edit_op_win.load_operator_into_gui(selected_index)
            self.edit_op_win.show()

    def open_settings_window(self):
        self.sets_win.draw_settings_values()
        self.sets_win.show()
    
    def change_cif_line_text(self, new_text):
        self.processor.cif_path = new_text
        print(new_text)

    def choose_cif_folder(self):
        cif_folder = QFileDialog.getExistingDirectory(caption="Open dir contains .cifs")
        cif_folder += "/*"
        self.ui.line_cif_path.setText(cif_folder)
        self.processor.cif_path = cif_folder

    def choose_cif_file(self):
        cif_name = QFileDialog.getOpenFileName(caption="Open .cif-file", filter="Crystallography Information File (*.cif)")
        if cif_name[0] != "" and cif_name[0] is not None:
            self.ui.line_cif_path.setText(cif_name[0])
            self.processor.cif_path = cif_name[0]
        
    def check_calc_only(self, new_state):
        self.processor.calc_only = new_state
    
    def check_no_hydro(self, new_state):
        self.processor.no_hydro = new_state

    def check_super_cell_changed(self, new_value):
        self.processor.supercell_radius = new_value

    def check_super_cell(self, new_state):
        self.processor.use_supercell = new_state
        if new_state == 2:
            self.ui.spin_supcell_radius.setEnabled(True)
        else:
            self.ui.spin_supcell_radius.setEnabled(False)

    def _save_logs(self):
        cif = os.path.dirname(os.path.normpath(self.processor.cif_path))
        logs = self.processor.process_worker.logs
        apex_data_path = os.path.dirname(self.processor.settings.settings_file_path)
        path = os.path.join(apex_data_path, "stdout.log")

        with open(path, "w") as log:
            log.write(logs)

    def process_failed(self):
        self.processor.process_worker.stop()
        self.process_finished()

        ErrorWindow.invoke_error("Ошибка запуска", "Не удалось запустить расчетное ядро.", 
                            "Это может быть связано с тем, что передаваемые параметры " \
                            "запуска имеют слишком большой размер или файл или произошла неизвестная ошибка.")

    def process_finished(self):
        if self.processor.process_worker.process.state() == QProcess.ProcessState.NotRunning:
            self.set_gui_enabled(True)
            self.ui.status_bar.showMessage("Не запущено")
            self.overlay.hide()
            self._save_logs()

    def _previous_results_dialog(self) -> bool:
        """
        Выводит окно о предложении удаления предыдущих результатов, или их открытии.

        В случае открытия, запуск не будет произведен. При нажатии "Да" старый json будет удален
        При удалении или неудалении, запуск все равно будет произведен

        При нажатии да/нет возвращает True, что приведет к запуску нового расчета
        В случае нажатия кнопки "открыть" вернет False.
        """
        json_path = self.processor.settings.get_json_path()

        if os.path.exists(json_path):
            msg_win = QMessageBox()
        
            # Помещаем это окно в центр главного окна, а то на Windows оно где-то в углу
            main_win_geom = self.frameGeometry()
            center = main_win_geom.center()
            msg_win.setGeometry(center.x()-150, center.y()-150, 300, 300)

            msg_win.setIcon(QMessageBox.Icon.Question)
            msg_win.setWindowModality(Qt.WindowModality.ApplicationModal)
            msg_win.setWindowTitle("Предыдущие результаты")
            msg_win.setText("Был обнаружен файл с предыдущими результатами")
            msg_win.setInformativeText("Удалить их и заменить на результаты нового расчета или открыть для просмотра?")

            del_btn = msg_win.addButton("Удалить", QMessageBox.ButtonRole.YesRole)
            not_del_btn = msg_win.addButton("Не удалять", QMessageBox.ButtonRole.NoRole)
            open_btn = msg_win.addButton("Открыть", QMessageBox.ButtonRole.ActionRole)
            close_btn = msg_win.addButton("Отмена", QMessageBox.ButtonRole.RejectRole)

            msg_win.setDefaultButton(close_btn) # Кнопка по Enter (По умолчанию выделена)
            msg_win.setEscapeButton(close_btn) # Кнопка крестика или 'Esc'

            msg_win.exec()
            cliked_btn = msg_win.clickedButton()

            if cliked_btn == del_btn:
                os.remove(json_path)
                return True
            elif cliked_btn == not_del_btn:
                return True
            elif cliked_btn == open_btn:
                self.processor.collect_results()
                return False
            else:
                return False
        else:
            return True

    def run_stop(self):
        if not self.processor.process_worker_works:
            if not self._cif_path_exists(): return
            if not self._operators_exists(): return
            if not self._execution_file_exists(): return

            self.processor.assemble_args()
            # На unix надо дать права запуска исполняемого файла
            if sys.platform != "win64" and sys.platform != "win32":
                chmod = QProcess()
                chmod.start("chmod", ["+x", self.processor.pss2_args[0]])
                chmod.waitForFinished(1000)

            if self._is_executable():
                need_to_run = self._previous_results_dialog()
                
                if need_to_run:
                    self.ui.status_bar.showMessage("В работе...")

                    # Весь интерфейс, который производит действия, надо отключить ...
                    self.set_gui_enabled(False)
                    # ... кроме кнопки stop и соответствующего пункта меню
                    self.ui.action_stop.setEnabled(True)
                    self.ui.btn_run.setEnabled(True)
                    self.ui.action_about.setEnabled(True)
                    self.overlay.show()
                    self.processor.process_worker.run()
        else:
            self.processor.process_worker.stop()
            self.process_finished()

    @staticmethod
    def _set_color(died_val):
        """
        Возвращает цвет для окраски строки оператора на основе значения died
        died - степень инвариантности электронной плотности (эта)
        Цветовой градиент делается через линейную функцию
        """
        COLOR_GOOD = QColor(50, 205, 50, 255) # Лаймовый
        COLOR_NOT_BAD = QColor(255, 215, 0, 255) # Золотой
        COLOR_BAD = QColor(250, 128, 114, 255) # Лососевый (salmon) :))))
 
        color = QColor(0, 0, 0, 0)
        if died_val >= 0.485:
            color = COLOR_GOOD
            # Градиент цвета через альфу
            k = 255/(1.000-0.485)
            b = k*0.485
            color.setAlpha(int(k*died_val-b))
        elif died_val < 0.485 and died_val > 0.111:
            color = COLOR_NOT_BAD
            k = 255/(0.485-0.111)
            b = k*0.111
            color.setAlpha(int(k*died_val-b))
        else:
            color = COLOR_BAD
            k = 255/(0.111-0.000)
            b = 0
            # abs, птому что иногда эта может быть немного отрицательной
            color.setAlpha(abs(int(k*died_val-b)))

        return color

    # Отрисовка результатов расчета для конкретной структуры в виде таблицы
    # Индекс, если что - это индекс струкутуры из combobox'а
    def _draw_structure_info(self, index):
        cnt = len(self.processor.json_data.structures)
        if cnt > 0 and index < cnt:
            structure = self.processor.json_data.structures[index]
            structure_text = f"Name: {structure.name}\n" \
                             f"Space group: {structure.sp_gr} (No. {structure.sp_gr_num})\n" \
                             f"\n" \
                             f"a: {structure.a:.3f} Å\nb: {structure.b:.3f} Å\nc: {structure.c:.3f} Å\n" \
                             f"α: {structure.alpha:.3f}°\nβ: {structure.beta:.3f}°\nγ: {structure.gamma:.3f}°\n" \
                             f"\n" \
                             f"Cartesian basis:\n" \
                             f"a = [{structure.cartesian_a[0]:.3f}, {structure.cartesian_a[1]:.3f}, {structure.cartesian_a[2]:.3f}]\n" \
                             f"b = [{structure.cartesian_b[0]:.3f}, {structure.cartesian_b[1]:.3f}, {structure.cartesian_b[2]:.3f}]\n" \
                             f"c = [{structure.cartesian_c[0]:.3f}, {structure.cartesian_c[1]:.3f}, {structure.cartesian_c[2]:.3f}]\n" 
                             
            self.ui.info_text_browser.setText(structure_text)
        
    def draw_progress(self, new_progress):
        if new_progress != -1:
            self.progress_bar.setValue(new_progress)

    def redraw_results(self):
        if self.ui.combo_box_structures.count() != 0:
            index = self.ui.combo_box_structures.currentIndex()
            self.draw_results(index)

    def draw_results(self, index):
        obtained_structures = self.processor.json_data.get_structures()
        structure_to_draw = obtained_structures[index]

        sets = self.processor.settings
        ops_to_draw = cut_operators_array_within_settings(structure_to_draw.operators, sets.get_minimum_out_eta(),
                                                          sets.get_maximum_out_eta(), sets.get_max_out(), sets.get_precision())

        self.ui.table_results.setSortingEnabled(False)
        self.ui.table_results.clear()
        self.ui.table_results.setColumnCount(7)
        self.ui.table_results.setHorizontalHeaderItem(0, QTableWidgetItem("Name"))
        self.ui.table_results.setHorizontalHeaderItem(1, QTableWidgetItem("Cartesian Trans."))
        self.ui.table_results.setHorizontalHeaderItem(2, QTableWidgetItem("Affine Trans."))
        self.ui.table_results.setHorizontalHeaderItem(3, QTableWidgetItem("^a, deg"))
        self.ui.table_results.setHorizontalHeaderItem(4, QTableWidgetItem("^b, deg"))
        self.ui.table_results.setHorizontalHeaderItem(5, QTableWidgetItem("^c, deg"))
        self.ui.table_results.setHorizontalHeaderItem(6, QTableWidgetItem("η"))

        self.ui.table_results.setRowCount(len(ops_to_draw))
        
        for row in range(self.ui.table_results.rowCount()):
            for col in range(self.ui.table_results.columnCount()):
                op = ops_to_draw[row]

                text = ""
                if col == 0: text = op.name
                elif col == 1: text = f"{op.t1_cart:.3f}, {op.t2_cart:.3f}, {op.t3_cart:.3f}"
                elif col == 2: text = f"{op.t1_affn:.3f}, {op.t2_affn:.3f}, {op.t3_affn:.3f}"
                elif col == 3: text = f"{op.a_angle:.3f}"
                elif col == 4: text = f"{op.b_angle:.3f}"
                elif col == 5: text = f"{op.c_angle:.3f}"
                else: text = f"{op.eta:.3f}"

                new_item = QTableWidgetItem(text)
                new_item.setBackground(MainWindow._set_color(op.eta))
                self.ui.table_results.setItem(row, col, new_item)
        
        self._draw_structure_info(index)
        self.ui.table_results.resizeColumnsToContents()
        self.ui.table_results.resizeRowsToContents()
        self.ui.table_results.setSortingEnabled(True)

    def fill_structs_combo(self):
        self.ui.status_bar.showMessage("Готово")

        obtained_structures = self.processor.json_data.get_structures()
        self.ui.combo_box_structures.clear()
        
        for struct in obtained_structures:
            self.ui.combo_box_structures.addItem(f"{struct.name} ({struct.from_cif})")
        # Отрисовываем результат самой первой стурктуры (0-й индекс комбобокса)
        self.draw_results(0)

    def save_into_csv(self):
        path = QFileDialog.getSaveFileName(caption="Save file",filter="Comma-Separated Values (*.csv)")

        if path[0] != "" and path[0] is not None:
            sets = self.processor.settings
            writer = CSVwriter(path[0], sets.get_minimum_out_eta(), sets.get_maximum_out_eta(),
                               sets.get_max_out(), sets.get_precision())
            writer.dump(self.processor.json_data.get_structures())

    def unload_json(self):
        json_path = self.processor.settings.get_json_path()

        if not os.path.exists(json_path):
            ErrorWindow.invoke_info("Нет результатов", "Отсутствуют .json-файлы с результатами.", 
                                    "Запустите расчет для создания такого файла.")
            return

        path = QFileDialog.getSaveFileName(caption="Save file",filter="JavaScript Object Notation (*.json)")

        # Копируем имеющийся json и сохраняем его отдельно
        if path[0] != "" and path[0] is not None:
            file_lines = []
            with open(json_path, "r") as f:
                file_lines = f.readlines()

            with open(path[0], "w") as f:
                f.writelines(file_lines)

    def show_about(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("О программе")
        msg_box.setIcon(QMessageBox.Icon.Information)
    
        msg_box.setTextFormat(Qt.TextFormat.RichText)
        msg_box.setText(about_text)
        
        msg_box.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def show_manual(self):
        exec_dir = os.path.dirname(self.processor.settings.get_exec_path()) # Папка core
        main_dir = exec_dir.replace(os.path.basename(exec_dir), "") # Попадаем в main-папку
        manual_path = os.path.join(main_dir, "extras", "manual.pdf") # ну и пишем путь к pdf-ке с мануалом

        # Открытие файла
        if sys.platform == "win32": subprocess.run(['start', '', manual_path], shell=True)  # Windows
        elif sys.platform == "darwin": subprocess.run(['open', manual_path])      # macOS
        else: subprocess.run(['xdg-open', manual_path])  # Linux

    def set_gui_enabled(self, bool):
        if bool:           
            self.ui.menu_file.setEnabled(True)
            self.ui.action_run.setEnabled(True)
            self.ui.action_settings.setEnabled(True)
            self.ui.action_stop.setEnabled(False)
        else:
            self.ui.menu_file.setEnabled(False)
            self.ui.action_settings.setEnabled(False)
            self.ui.action_run.setEnabled(False)
            self.ui.action_stop.setEnabled(True)

    def open_olf(self):
        path = QFileDialog.getOpenFileName(caption="Open file",
                                           filter="Operator List File (*.olf)")
        self._read_olf_file(path[0])

    def save_olf(self):
        ops = self.processor.operators_to_calc
        if len(ops) > 0:
            path = QFileDialog.getSaveFileName(caption="Save file",
                                               filter="Operator List File (*.olf)")
            if path[0] != "" and path[0] is not None:
                saver = OLFIO(path[0])
                saver.set_operators_to_calc(ops)
                saver.save_file()

    def open_res_json(self):
        path = QFileDialog.getOpenFileName(caption="Open file",
                                           filter="JavaScript Object Notation (*.json)")
        self._read_res_json_file(path[0])

 
class EditOpWindow(QWidget):
    def __init__(self, main_window: MainWindow, presets_file_path: str):
        self.main_win = main_window

        # Запуск окна в режиме редактирования оператора. 
        # По умолчанию индекса нет = -1. Индекс, в смысле,каокй оператор редактируется
        self.edit_index = -1
        self.ops_presets = {}
        self.preset_file_path = presets_file_path

        # init GUI
        super().__init__()
        self.ui = Ui_OpEditWindow()
        self.ui.setupUi(self)
        #self._load_ops_presets()
        self.preset_cathegory_changed("")

        self.ui.combo_op_presets_category.textActivated.connect(self.preset_cathegory_changed)
        self.ui.combo_op_presets.textActivated.connect(self.preset_changed)
        self.ui.btn_apply.clicked.connect(self.apply_operator)
        self.ui.btn_cancel.clicked.connect(self.cancel_operator)
    
    @staticmethod
    def _is_flt(value):
        try:
            num = float(value)
            return True
        except:
            return False

    def _get_current_presets_cathegory(self):
        """
        Переводит текущую выбранную в комбо-боксе категорию
        в ключ и json-файла пресетов
        """
        combo_box = self.ui.combo_op_presets_category
        current_i = combo_box.currentIndex()

        if current_i == 0:
            return "translations_and_inv"
        elif current_i == 1:
            return "rotations"
        elif current_i == 2:
            return "inv_rotations"
        else:
            return "planes"

    def _load_ops_presets(self, cath):
        """
        Загружает пресеты операторов из данной категории, из json-файла
        """
        # На всякий, обнуляем словарь
        self.ops_presets = {}
        self.ui.combo_op_presets.clear()

        with open(self.preset_file_path, "r", encoding="utf-8") as p:
            full_data = json.load(p)
            data = full_data[0][cath]
            for op in data:
                self.ops_presets[op["name"]] = {
                    "a11": float(op["a11"]),
                    "a12": float(op["a12"]),
                    "a13": float(op["a13"]),
                    "a21": float(op["a21"]),
                    "a22": float(op["a22"]),
                    "a23": float(op["a23"]),
                    "a31": float(op["a31"]),
                    "a32": float(op["a32"]),
                    "a33": float(op["a33"])
                }
                self.ui.combo_op_presets.addItem(op["name"])

    def _new_operator_contains_only_digits(self):
        digits = True
        digits &= EditOpWindow._is_flt(self.ui.a11.text())
        digits &= EditOpWindow._is_flt(self.ui.a12.text())
        digits &= EditOpWindow._is_flt(self.ui.a13.text())
        digits &= EditOpWindow._is_flt(self.ui.a21.text())
        digits &= EditOpWindow._is_flt(self.ui.a22.text())
        digits &= EditOpWindow._is_flt(self.ui.a23.text())
        digits &= EditOpWindow._is_flt(self.ui.a31.text())
        digits &= EditOpWindow._is_flt(self.ui.a32.text())
        digits &= EditOpWindow._is_flt(self.ui.a33.text())
        digits &= EditOpWindow._is_flt(self.ui.t1.text())
        digits &= EditOpWindow._is_flt(self.ui.t2.text())
        digits &= EditOpWindow._is_flt(self.ui.t3.text())
        return digits

    def _new_operator_filled_properly(self):
        # Проверяем, заполнены ли и заполнены ли верно 
        if not self._new_operator_contains_only_digits():
            ErrorWindow.invoke_error("Ошибка ввода","Матрица поворота или вектор трансляции заданы с ошибкой.",
                                     "Вектор трансляции и матрица должны содержать только числа и не быть пустыми.")
            return False
        else:
            return True

    def preset_cathegory_changed(self, text):
        cath = self._get_current_presets_cathegory()
        self._load_ops_presets(cath)

    def preset_changed(self, text):
        self.ui.line_op_name.setText(text)

        self.ui.a11.setText(str(self.ops_presets[text]["a11"]))
        self.ui.a12.setText(str(self.ops_presets[text]["a12"]))
        self.ui.a13.setText(str(self.ops_presets[text]["a13"]))
        self.ui.a21.setText(str(self.ops_presets[text]["a21"]))
        self.ui.a22.setText(str(self.ops_presets[text]["a22"]))
        self.ui.a23.setText(str(self.ops_presets[text]["a23"]))
        self.ui.a31.setText(str(self.ops_presets[text]["a31"]))
        self.ui.a32.setText(str(self.ops_presets[text]["a32"]))
        self.ui.a33.setText(str(self.ops_presets[text]["a33"]))

        # Трансляции отсутствуют
        self.ui.t1.setText("0")
        self.ui.t2.setText("0")
        self.ui.t3.setText("0")

    def apply_operator(self):
        if not self._new_operator_filled_properly(): return

        name = self.ui.line_op_name.text()
        matrix = self._gui_to_matrix()
        translation = self._gui_to_translation()
        new_op = OpetatorToCalc(name, matrix, translation)

        if self.edit_index == -1:
            new_op_list_item = QListWidgetItem(f"{name} | ({translation[0]:.3f} {translation[1]:.3f} {translation[2]:.3f})")
            self.main_win.ui.list_ops.addItem(new_op_list_item)
            self.main_win.processor.operators_to_calc.append(new_op)
        else:
            self.main_win.processor.operators_to_calc[self.edit_index] = new_op
            item_to_change = self.main_win.ui.list_ops.item(self.edit_index)
            item_to_change.setText(f"{name} | ({translation[0]:.3f} {translation[1]:.3f} {translation[2]:.3f})")

    def load_operator_into_gui(self, index):
        op = self.main_win.processor.operators_to_calc[index]
        name = op.name
        matrix = op.matrix
        vector = op.translation

        self.ui.line_op_name.setText(name)
        self.ui.a11.setText(str(matrix[0][0]))
        self.ui.a12.setText(str(matrix[0][1]))
        self.ui.a13.setText(str(matrix[0][2]))
        self.ui.a21.setText(str(matrix[1][0]))
        self.ui.a22.setText(str(matrix[1][1]))
        self.ui.a23.setText(str(matrix[1][2]))
        self.ui.a31.setText(str(matrix[2][0]))
        self.ui.a32.setText(str(matrix[2][1]))
        self.ui.a33.setText(str(matrix[2][2]))
        self.ui.t1.setText(str(vector[0]))
        self.ui.t2.setText(str(vector[1]))
        self.ui.t3.setText(str(vector[2]))

    def cancel_operator(self):
        self.hide()
    
    def _gui_to_matrix(self):
        a00 = float(self.ui.a11.text())
        a01 = float(self.ui.a12.text())
        a02 = float(self.ui.a13.text())
        a10 = float(self.ui.a21.text())
        a11 = float(self.ui.a22.text())
        a12 = float(self.ui.a23.text())
        a20 = float(self.ui.a31.text())
        a21 = float(self.ui.a32.text())
        a22 = float(self.ui.a33.text())
        matrix = [[a00, a01, a02],[a10, a11, a12],[a20, a21, a22]]
        return matrix

    def _gui_to_translation(self):
        t0 = float(self.ui.t1.text())
        t1 = float(self.ui.t2.text())
        t2 = float(self.ui.t3.text())
        vector = [t0, t1, t2]
        return vector

