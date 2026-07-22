/*
Оператор симметрии ничем не отличается от оператора псевдодсимметрии,
Кроме того, что тут есть эта != (1 + 0i). Поэтому решено убрать класс операторов псевдосимметрии
*/

#ifndef SYMM_OPS
#define SYMM_OPS

#include "pss2_basic_types.hpp"
#include "pss2_maps_types.hpp"

class SymmOperator
{
    public:
        std::string name;
        transOperator vector;
        transOperator vector_affine; // Вектор в аффинном базисе, используется только для ввода и вывода
        pointOperator matrix;

        double vec_a_angle; // Углы между вектором трасляции оператора и векторами базиса решетки
        double vec_b_angle;
        double vec_c_angle;

        complex<double> eta; // Степень инвариантности электронной плотности относительно него

        bool refined;

        SymmOperator();
        SymmOperator(const std::string& name);
        SymmOperator(pointOperator matrix, transOperator vector, std::string name);
        SymmOperator(pointOperator matrix, transOperator vector, std::string name, complex<double> eta);

        bool isEqual(const SymmOperator& op) const;
        bool operator==(const SymmOperator& otherOp) const;

        SymmOperator multiply(const SymmOperator& op) const;
        SymmOperator operator*(const SymmOperator& op) const;
};

#endif