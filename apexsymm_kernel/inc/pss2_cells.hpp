#ifndef CELLS
#define CELLS

#include "pss2_basic_types.hpp"
#include "pss2_atoms.hpp"

class Cell
{
    public:
        // Параметры ячейки
        double a, b, c;
        double alpha, beta, gamma;
        double volume;

        // Информация об элементарной ячейке
        string syngony = ""; // Сингония
        string spaceGroupSymm = ""; // Символ пространственной группы
        unsigned char spaceGroupNum = 0; // Номер пространственной группы

        Matrix3d cartesianBasis; // Декартов базис ячейки
        vector<string> affineSymmetryOps; // Операторы симметрии (нужны для размножения атомов)

        int atomsCount; // Число атомов в ячейке
        vector<Atom> atoms; // Вектор - хранилище атомов ячейки

        bool multiplied; // Является ли ячейка размноженной?

        bool isSuperCell = false; // Является ли ячейка суперячейкой
        int supCellFac = 0; // Координационный радиус последней ячейки
        Vector3d supCellShift{0, 0, 0}; // Вектор сдвига начала координат супреячейки отн. исходной

        Cell();

        // Размножает атомы
        int multiplyAtoms();

        // Подготавливает атомы к расчету
        void prepareAtoms();

        // Существует ли уже такой атом в ячейке??
        bool isAtomExists(const Atom& atomToCheck);

        /* Расширяет данную ячейку до супер-ячейки заданного размера
           radius - это как бы до какой координационной сферы из ячеек размножать */
        void extendToSuperCell(const int& radius);

        // Считает декартов базис для ячейки
        void calcCartesianBasis(bool printOut = false);
};

#endif