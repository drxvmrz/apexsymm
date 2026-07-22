#include "pss2_symm_operators.hpp"

SymmOperator::SymmOperator() 
{
    this->name = "";
    this->vector << 0, 0, 0;
    this->vector_affine << 0, 0, 0;
    this->matrix << 0, 0, 0,
                    0, 0, 0,
                    0, 0, 0;

    this->vec_a_angle = 0;
    this->vec_b_angle = 0;
    this->vec_c_angle = 0;

    this->eta = complex<double>(0.0, 0.0);
    this->refined = false;
}

SymmOperator::SymmOperator(const std::string& name) 
{
    this->name = name;
    this->vector << 0, 0, 0;
    this->vector_affine << 0, 0, 0;
    this->matrix << 0, 0, 0,
                    0, 0, 0,
                    0, 0, 0;

    this->vec_a_angle = 0;
    this->vec_b_angle = 0;
    this->vec_c_angle = 0;

    this->eta = complex<double>(0.0, 0.0);
    this->refined = false;
}

SymmOperator::SymmOperator(pointOperator matrix, transOperator vector, std::string name)
{
    this->name = name;
    this->matrix = matrix;
    this->vector = vector;
    this->vector_affine << 0, 0, 0;
    this->vec_a_angle = 0;
    this->vec_b_angle = 0;
    this->vec_c_angle = 0;
    this->eta = complex<double>(0.0, 0.0);
    this->refined = false;
}

SymmOperator::SymmOperator(pointOperator matrix, transOperator vector, std::string name, complex<double> eta)
{
    this->name = name;
    this->matrix = matrix;
    this->vector = vector;
    this->vector_affine << 0, 0, 0;
    this->eta = eta;
    this->vec_a_angle = 0;
    this->vec_b_angle = 0;
    this->vec_c_angle = 0;
    this->refined = false;
}

bool SymmOperator::isEqual(const SymmOperator& op) const
{
    const bool matricesIsEqual = (this->matrix == op.matrix);
    const bool vectorsIsEqual = (this->vector == op.vector);
    return matricesIsEqual && vectorsIsEqual;
}

bool SymmOperator::operator==(const SymmOperator& otherOp) const
{
    return this->isEqual(otherOp);
}