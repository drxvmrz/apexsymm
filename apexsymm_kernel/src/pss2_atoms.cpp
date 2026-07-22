#include "pss2_atoms.hpp"

Atom::Atom() {}

Atom::Atom(const string name, const string element, const double x, const double y, const double z, const double sof)
{
    this->name = name;
    this->element = element;
    this->x = x;
    this->y = y;
    this->z = z;
    this->sof = sof;
}

void Atom::elementToNum()
{
    this->elementNum = ScatFactors::elemToNumbers.at(this->element);
}

void Atom::createCartesianVector(const Matrix3d& cartesianMatrixTransposed)
{
    this->xyz = cartesianMatrixTransposed*Vector3d{this->x, this->y, this->z};
}

void Atom::normalize()
{
    while (x >= 1.0) x -= 1.0;
    while (y >= 1.0) y -= 1.0;
    while (z >= 1.0) z -= 1.0;
    while (x < 0.0) x += 1.0;
    while (y < 0.0) y += 1.0;
    while (z < 0.0) z += 1.0;
}

// Проверяет, нормальные ли координаты у атома, чтобы они не оказались на дальнем краю ячейки
// Ну и чтобы они находились внутри ячейки еще
bool Atom::isNormCoords()
{
    return ((0 <= x && x < 1.000) && 
            (0 <= y && y < 1.000) && 
            (0 <= z && z < 1.000));
}

double Atom::calcScatFactor(const double& stl)
{
    const auto& scatArr = ScatFactors::scatFactors[this->elementNum-1];

    double factor = scatArr[0];
    
    if (isZero(stl)) 
    {
        for (int i = 1; i < 5; i++)
        {
            factor += scatArr[i];
        }
    } 
    else
    {
        for (int i = 1; i < 5; i++)
        {
            factor += scatArr[i]*exp(-scatArr[i+4]*pow(stl, 2));
        }   
    }

    return factor;
}