#ifndef ATOMS
#define ATOMS

#include "pss2_basic_types.hpp"
#include "pss2_static_consts.hpp"
#include "pss2_basic_math.hpp"

class Atom
{
    public:
        string name;
        string element;
        int elementNum = 0;

        double x, y, z;
        double sof;
        Vector3d xyz; // Радиус-вектор атома в декартовом базисе

        double Uiso = 0.0;

        Atom();
        Atom(const string name, const string element, 
            const double x, const double y, const double z, 
            const double sof);
        
        void elementToNum();
        void createCartesianVector(const Matrix3d& cartesianMatrixTransposed); // Создает атому радиус вектор в декартовых координатах
        void normalize(); // Возвращает координаты в диапазон от [0; 1), чтобы они были точно внутри ячейки
        bool isNormCoords(); // Проверяет, нормальные ли координаты у атома, находятся ли они внутри одной ячейки?!
        double calcScatFactor(const double& stl); // Расчитывает для данного атома фактор рассеяния
};

#endif