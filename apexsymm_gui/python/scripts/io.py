import json

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from .pss_types import *

LEVEL_INFO = 0
LEVEL_WARNING = 1
LEVEL_CRITICAL = 2

def cut_operators_array_within_settings(array: list[SymmOperator], min_eta: float, max_eta: float, max_out: int, precision: float) -> list[SymmOperator]:
    """
    Обрезает полученный массив трансляций операторов 
    в соответствии с настройками:

    max_eta - максимально допустимый eta для вывода оператора
    min_eta - минимально допустимый eta для вывода оператора
    max_out - сколько максимально трансляций для одного оператора можно вывести
    precision - точность расчета

    По умолчанию в json они уже должны быть отсортированы
    по названию, а внутри названий по значениям 'эта'.
    Поэтому для учета границ вывода и числа достаточно рассмотреть
    их просто все подряд. И отсчитывать, нужное ли количество получено

    Не изменяет исходный массив операторов
    """

    shown = 0
    new_array = []
    current_op_name = ""

    for op in array:
        # max_out задает максимальное число вывода для операторов с конкретным именем
        if op.name != current_op_name:
            shown = 0
            current_op_name = op.name

        if (op.eta <= max_eta + precision and op.eta >= min_eta - precision) and shown < max_out:
            new_array.append(op)
            shown += 1
        else:
            continue
    
    return new_array

class ErrorWindow(QMessageBox):
    def __init__(self, title: str, message: str, info_message: str, level: int):
        super().__init__()
        self.setWindowTitle(title)
        self.setText(message)
        self.setInformativeText(info_message)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        if level == LEVEL_INFO: # информативное окно
            self.setIcon(QMessageBox.Icon.Information)
        elif level == LEVEL_WARNING: # предупреждение
            self.setIcon(QMessageBox.Icon.Warning)
        else: # критичская ошибка
            self.setIcon(QMessageBox.Icon.Critical)

    @staticmethod
    def invoke_info(title, message, info_message = ""):
        box = ErrorWindow(title, message, info_message, LEVEL_INFO)
        box.exec_()

    @staticmethod
    def invoke_warning(title, message, info_message = ""):
        box = ErrorWindow(title, message, info_message, LEVEL_WARNING)
        box.exec_()

    @staticmethod
    def invoke_error(title, message, info_message = ""):
        box = ErrorWindow(title, message, info_message, LEVEL_CRITICAL)
        box.exec_()


class OpetatorToCalc:
    def __init__(self, name, matrix, translation):
        self.name = name
        self.matrix = matrix
        self.translation = translation 

    def to_string_arg(self):
        """
        Переводит оператор для расчета в аргумент командной строки для pss2
        ВАЖНО! Функция не добавляет ';', придется отслеживать его добавление самому
        """
        full_string = ""
        if self.name == None or self.name == "":
            full_string =   f"{self.matrix[0][0]} {self.matrix[0][1]} {self.matrix[0][2]}/" \
                            f"{self.matrix[1][0]} {self.matrix[1][1]} {self.matrix[1][2]}/" \
                            f"{self.matrix[2][0]} {self.matrix[2][1]} {self.matrix[2][2]}/" \
                            f"{self.translation[0]} {self.translation[1]} {self.translation[2]}"
        else:
            full_string =   f"{self.matrix[0][0]} {self.matrix[0][1]} {self.matrix[0][2]}/" \
                            f"{self.matrix[1][0]} {self.matrix[1][1]} {self.matrix[1][2]}/" \
                            f"{self.matrix[2][0]} {self.matrix[2][1]} {self.matrix[2][2]}/" \
                            f"{self.translation[0]} {self.translation[1]} {self.translation[2]}/{self.name}"
        return full_string
    

class OLFIO:
    """
    OLF (operator list file) - это расширение для файлов со списком операторов
    На самом деле в рамках одного исследования их может быть много, поэтому лучше их хранить
    в виде списка в отдельном файле, чтоб, если что, быстро открыть или драг-н-дропнуть 
    """
    def __init__(self, path):
        self.path = path
        self.operators_to_calc = []

    @staticmethod
    def operator_to_calc_to_json(operator_to_calc: OpetatorToCalc):
        data_dict = {
            "name": operator_to_calc.name,
            "a11": operator_to_calc.matrix[0][0],
            "a12": operator_to_calc.matrix[0][1],
            "a13": operator_to_calc.matrix[0][2],
            "a21": operator_to_calc.matrix[1][0],
            "a22": operator_to_calc.matrix[1][1],
            "a23": operator_to_calc.matrix[1][2],
            "a31": operator_to_calc.matrix[2][0],
            "a32": operator_to_calc.matrix[2][1],
            "a33": operator_to_calc.matrix[2][2],
            "t1": operator_to_calc.translation[0],
            "t2": operator_to_calc.translation[1],
            "t3": operator_to_calc.translation[2]
        }
        return data_dict

    @staticmethod
    def json_to_operator_to_calc(json_data):
        name = json_data["name"]
        matrix = [[float(json_data["a11"]), float(json_data["a12"]), float(json_data["a13"])],
                  [float(json_data["a21"]), float(json_data["a22"]), float(json_data["a23"])],
                  [float(json_data["a31"]), float(json_data["a32"]), float(json_data["a33"])]]
        trans = [float(json_data["t1"]), float(json_data["t2"]), float(json_data["t3"])]
        return OpetatorToCalc(name, matrix, trans)

    def open_file(self):
        with open(self.path, "r") as olf:
            data = json.load(olf)
            for op_to_calc in data:
                self.operators_to_calc.append(OLFIO.json_to_operator_to_calc(op_to_calc))

    def save_file(self):
        with open(self.path, "w") as olf:
            final_dict = []
            for op in self.operators_to_calc:
                final_dict.append(OLFIO.operator_to_calc_to_json(op))
            json.dump(final_dict, olf, indent=4, ensure_ascii=False)

    def set_operators_to_calc(self, ops_to_calc_array: OpetatorToCalc):
        self.operators_to_calc = ops_to_calc_array

    def get_operators_to_calc(self):
        return self.operators_to_calc


class JSONReader:
    """
    Класс для работы с json-файлами, которые содержат результаты расчетов pss2
    Он создается там с помощью ключа --json <путь к новому файлу>
    """
    def __init__(self, json_path):
        self.path = json_path
        self.structures = []

    def load_structures(self):
        with open(self.path, "r", encoding="utf-8") as f:
            obj = json.load(f)
            structures_data = obj["structures"]

            for structure in structures_data:
                self.structures.append(JSONReader._structure_from_json_to(structure))

    def get_structures(self):
        return self.structures
    
    def clear_structures(self):
        self.structures = []

    @staticmethod
    def _structure_from_json_to(json_structure_data):
        new_struct = Structure()

        # Информация о структуре
        new_struct.name = json_structure_data["name"]
        new_struct.from_cif = json_structure_data["from_cif"]
        new_struct.sp_gr = json_structure_data["space_group"]
        new_struct.sp_gr_num = json_structure_data["space_group_num"]
        new_struct.a = json_structure_data["a"]
        new_struct.cartesian_a = [json_structure_data["ax"], json_structure_data["ay"], json_structure_data["az"]]
        new_struct.b = json_structure_data["b"]
        new_struct.cartesian_b = [json_structure_data["bx"], json_structure_data["by"], json_structure_data["bz"]]
        new_struct.c = json_structure_data["c"]
        new_struct.cartesian_c = [json_structure_data["cx"], json_structure_data["cy"], json_structure_data["cz"]]
        new_struct.alpha = json_structure_data["alpha"]
        new_struct.beta = json_structure_data["beta"]
        new_struct.gamma = json_structure_data["gamma"]

        # Информация об операторах
        operators_data = json_structure_data["operators"]
        for op in operators_data:
            new_struct.operators.append(JSONReader._operator_from_json_to(op))

        return new_struct

    @staticmethod
    def _operator_from_json_to(json_operator_data):
        new_op = SymmOperator()

        new_op.name = json_operator_data["name"]
        new_op.eta = json_operator_data["eta"]

        # Матрица поворота операторы
        new_op.a11 = json_operator_data["a11"]
        new_op.a12 = json_operator_data["a12"]
        new_op.a13 = json_operator_data["a13"]
        new_op.a21 = json_operator_data["a21"]
        new_op.a22 = json_operator_data["a22"]
        new_op.a23 = json_operator_data["a23"]
        new_op.a31 = json_operator_data["a31"]
        new_op.a32 = json_operator_data["a32"]
        new_op.a33 = json_operator_data["a33"]

        # Угол между векторами трансляций и векторами базиса
        new_op.a_angle = json_operator_data["a_angle"]
        new_op.b_angle = json_operator_data["b_angle"]
        new_op.c_angle = json_operator_data["c_angle"]

        # Трансляционный вектор в декартовом базисе
        new_op.t1_cart = json_operator_data["t1_cart"]
        new_op.t2_cart = json_operator_data["t2_cart"]
        new_op.t3_cart = json_operator_data["t3_cart"]

        # Трансляционный вектор в аффинном, исходном базисе
        new_op.t1_affn = json_operator_data["t1_affn"]
        new_op.t2_affn = json_operator_data["t2_affn"]
        new_op.t3_affn = json_operator_data["t3_affn"]

        return new_op


class CSVwriter:
    def __init__(self, save_path: str, min_eta: float, max_eta: float, max_out: int, precision: float):
        # Путь к сохраняемому файлу (полностью до .csv)
        self.save_path = save_path

        # Предустановки для функции cut_operators_array_within_settings(...)
        self.min_eta = min_eta
        self.max_eta = max_eta
        self.max_out = max_out
        self.precision = precision
    
    @staticmethod
    def _assemble_header(s: Structure) -> str:
        """
        Создает заголовок для отдельной таблицы .csv
        """
        str =   f"{s.name}\n{s.from_cif}\n{s.sp_gr} ({s.sp_gr_num})\n" \
                f"a =; {s.a:.3f}; alpha =; {s.alpha:.3f}\n" \
                f"b =; {s.b:.3f}; beta =; {s.beta:.3f}\n" \
                f"c =; {s.c:.3f}; gamma =; {s.gamma:.3f}"
        
        return str

    @staticmethod
    def _operators_subtable_string(op: SymmOperator) -> str:
        """
        Превращает оператор в строку .csv
        """
        str =   f"{op.name};" \
                f" {op.a11:.3f} {op.a12:.3f} {op.a13:.3f} | {op.a21:.3f} {op.a22:.3f} {op.a23:.3f} | {op.a31:.3f} {op.a32:.3f} {op.a33:.3f};" \
                f" {op.t1_affn:.3f}, {op.t2_affn:.3f}, {op.t3_affn:.3f}; {op.t1_cart:.3f}, {op.t2_cart:.3f}, {op.t3_cart:.3f}; {op.a_angle}; {op.b_angle}; {op.c_angle}; {op.eta:.3f}"
        return str

    def dump(self, structures: list[Structure]):
        """
        Сохраняет результаты в .csv-файл с учетом предустановок вывода

        По сути, результаты - это набор структур с операторами
        Поэтому для сохранения их надо как раз передать сами структуры
        Без всяких там конвертаций json и прочей требухи
        """
        
        with open(f"{self.save_path}", "w") as f:
            for structure in structures:
                f.write(CSVwriter._assemble_header(structure) + "\n")

                ops_arr = structure.operators
                ops_arr = cut_operators_array_within_settings(ops_arr, self.min_eta, self.max_eta, self.max_out, self.precision)

                if len(ops_arr) > 0:
                    f.write("name; matrix; translation_affn; translation_cart; ^a; ^b; ^c; eta\n")
                    for op in ops_arr:
                        f.write(CSVwriter._operators_subtable_string(op) + "\n")




