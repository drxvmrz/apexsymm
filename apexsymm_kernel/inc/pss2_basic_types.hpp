#ifndef BASIC_TYPES
#define BASIC_TYPES

// std
#include <string>
#include <vector>
#include <unordered_set>
#include <array>
#include <complex>
#include <cmath>
#include <filesystem>
#include <iostream>
#include <ostream>
#include <sstream>

// Сторонние библиотеки
#include <Eigen/Dense>
#include <fftw3.h>

// usings
using std::string;
using std::vector;
using std::complex;
using std::array;

using Eigen::Vector3d;
using Eigen::Matrix3d;

// namespaces
namespace fs = std::filesystem;

// other types
typedef Vector3d vectorH; // Вектор обратной решетки
typedef Vector3d vectorT; // Векторы трансляций t
typedef Vector3d transOperator; // Трансляционная компонента оператора - вектор трансляции
typedef Matrix3d pointOperator; // Точечный оператор симметрии - матрица поворота

// classes
class MapH; // Карта не сдвинутых H-векторов с отрицательными индексами
class MapM; // Карта сдвинутых H-векторов, индексы только положительные
class MapD; // Карта межплоскостных расстояний для H-векторов (несдвинутых)
class MapF; // Карта структурных амплитуд
class MapG; // Карта фурье-коэффициентов из структурных амплитуд
class MapEta; // Карта значений степени инвариантности. Заполняется, если нужно уточнение

class SymmOperator;
class Structure;

#endif