#include "pss2_cells.hpp"

Cell::Cell() {}

bool Cell::isAtomExists(const Atom& atomToCheck)
{
    if (atoms.empty()) return false;

    for (const auto& aroundVector : AroundAtoms::aroundVectors)
    {
        const Vector3d checkVector = Vector3d{atomToCheck.x, atomToCheck.y, atomToCheck.z} - aroundVector;
        const Vector3d currentCartesianVector = cartesianBasis.transpose() * checkVector;

        for (const auto& atom : atoms)
        {
            const Vector3d atomCartVector = cartesianBasis.transpose() * Vector3d{atom.x, atom.y, atom.z};
            const double norma = (atomCartVector - currentCartesianVector).norm();

            if (norma < 0.1) return true;
        }
    }

    return false;
}

int Cell::multiplyAtoms()
{
    atoms.reserve(1000);
    int multiplied = 0;

    // Через foreach не получается, так как происходит реаллокация памяти от emplace_back()
    for (int i = 0; i < atoms.size(); i++)
    {
        // Просто атом-прослойка для копирования его потом в атомы структуры
        Atom newAtom(atoms[i]);
        newAtom.x = newAtom.y = newAtom.z = 0.0;
        
        // Перебираем все операторы из cif-файла для размножения атомов
        for (const string& symmOp : affineSymmetryOps)
        {
            string buf;
            unsigned char index = 0; // Индекс координаты
            double value = 0.00000;
            double sign = 1.00000;

            for (size_t j = 0; j < symmOp.size(); j++)
            {   
                // End of string (EOS)
                const bool EOS = (j == symmOp.size() - 1);

                // Запятая меняет координату, к которой применяется оператор
                // Если вдруг знак - то считаем промежуточное значение и запихиваем его в значение
                // Конец строки должен срабатывать как и запятая!!
                const char c = symmOp[j];
                if (c == ',' || isSign(c) || EOS)
                {   
                    double term = 0.0;
                    
                    if (EOS) buf += c; 
                    
                    if (buf == "x") term = atoms[i].x;
                    else if (buf == "y") term = atoms[i].y;
                    else if (buf == "z") term = atoms[i].z;
                    else if (isFrac(buf)) term = toFrac(buf);

                    // Собираем из буфера полное значение координаты и очищаем его
                    value += term*sign;
                    buf.clear();
                    
                    // И вот сейчас можно изменять знак
                    if (isSign(c)) sign = toSign(c);
                    
                    if ((c == ',') || EOS)
                    {
                        switch (index)
                        {
                            case 0: newAtom.x = value; break;
                            case 1: newAtom.y = value; break;
                            case 2: newAtom.z = value; break;
                        }
                        index++;
                        value = 0.0;
                        sign = 1.0;
                    }
                }
                // Если ничего, просто заполняем буфер
                else
                {
                    // Пробелы игнорируем
                    if(c != ' ') buf += c;
                }
            }

            newAtom.normalize();
            if (!isAtomExists(newAtom))
            {
                atoms.emplace_back(newAtom);
                multiplied++;
            }
        }
    }
    
    atomsCount = (int)atoms.size();
    return multiplied;
}

void Cell::prepareAtoms()
{
    Matrix3d basis = this->cartesianBasis.transpose();

    for(auto& atom : this->atoms)
    {
        atom.createCartesianVector(basis);
        atom.elementToNum();
    }
}

// Переводит афинный базис в декартов, возвращает матрицу в виде:
// [ax, ay, az]
// [bx, by, bz]
// [cx, cy, cz]
// Где это координаты векторов трансляций в декартовом базисе
void Cell::calcCartesianBasis(bool printOut)
{
    const double sin_gamma = sin(toRad(gamma));
    const double cos_alpha = cos(toRad(alpha));
    const double cos_beta = cos(toRad(beta));
    const double cos_gamma = cos(toRad(gamma));

    const double xi = sqrt(1.0 - cos_alpha*cos_alpha - cos_beta*cos_beta - cos_gamma*cos_gamma -
                    - 2.0 * cos_beta * cos_gamma * cos_alpha);

    const double a11 = 1.0 / (a * sin_gamma);
    const double a12 = 0.0;
    const double a13 = -(cos_beta - cos_gamma * cos_alpha) / (a * xi * sin_gamma);
    const double a21 = -cos_gamma / (b * sin_gamma);
    const double a22 = 1.0 / b;
    const double a23 = -(1.0 / (b * xi)) * (sin_gamma * cos_alpha - cos_gamma * (cos_beta - cos_gamma * cos_alpha) / sin_gamma);
    const double a31 = 0.0;
    const double a32 = 0.0;
    const double a33 = sin_gamma / (c * xi);

    // Декартов базис находится решением системы
    Matrix3d matrixA;
    matrixA << a11, a12, a13,
               a21, a22, a23,
               a31, a32, a33;

    Matrix3d matrixB;
    matrixB << 1.00, 0.00, 0.00,
               0.00, 1.00, 0.00,
               0.00, 0.00, 1.00;

    // Решаем систему уравнений
    cartesianBasis << (matrixA.colPivHouseholderQr().solve(matrixB)).transpose();
    
    if (printOut) std::cout << cartesianBasis;
}

void Cell::extendToSuperCell(const int& radius)
{
    // Увеличиваем базовые параметры
    this->supCellFac = radius + 2;
    this->supCellShift = radius*(cartesianBasis.row(0) + cartesianBasis.row(1) + cartesianBasis.row(2));

    this->a *= supCellFac;
    this->b *= supCellFac;
    this->c *= supCellFac;

    this->cartesianBasis *= supCellFac;
    this->volume *= pow(supCellFac, 3);
    this->isSuperCell = true;

    // Разбираем атомы
    vector<Atom> newAtoms{};

    // Размножаем все атомы по всем новым ячейкам
    for(const auto& atom : this->atoms)
        for(int i = 0; i < supCellFac; i++)
            for(int j = 0; j < supCellFac; j++)
                for(int k = 0; k < supCellFac; k++)
                {
                    if (i == 0 && j == 0 && k == 0) continue;
                    
                    Atom newAtom = atom;
                    newAtom.x += i;
                    newAtom.y += j;
                    newAtom.z += k;
                    newAtoms.emplace_back(newAtom);
                }

    // Встраиваем массив новых атомов в уже имеющиеся атомы ячейки
    this->atoms.insert(this->atoms.end(), newAtoms.begin(), newAtoms.end());

    for(auto& atom : this->atoms)
    {
        atom.x /= supCellFac;
        atom.y /= supCellFac;
        atom.z /= supCellFac;
    }

}

