#include <chrono>

#include "pss2_structures.hpp"

inline double calcPlanarDistance(const vectorH& H)
{
    const double norm = H.norm(); 
    return (isZero(norm) ? 0.0 : 1/norm);
}

inline double calcSTL(const vectorH& H)
{
    return H.norm()/2;
}

void Structure::_prepareAtomsToCalc()
{
    this->cell.prepareAtoms();
}

void Structure::_createLoopGrid()
{
    for(int i = 0; i < 2*hMax + 1; i++)
    {
        for(int j = 0; j < 2*kMax + 1; j++)
        {
            for(int k = 0; k < 2*lMax + 1; k++)
            {
                loopGrid.emplace_back(array<int, 3>{i, j, k});
            }
        }
    }
}

void Structure::_transformOpVecsToCart()
{
    for (auto& opVec : this->pseudoSymmOperators)
    {
        for (auto& op : opVec)
        {
            if(this->cell.isSuperCell) op.vector = (cell.cartesianBasis/cell.supCellFac).transpose() * op.vector_affine + cell.supCellShift;
            else op.vector = cell.cartesianBasis.transpose() * op.vector_affine;
        }
    }
    
}

void Structure::_allocateOperators(const vector<SymmOperator>& operators)
{
    // Смотрим все операторы, которые были введены в командную строку
    for(const auto& op : operators)
    {
        bool vectorIsAdded = false;

        for(auto& same_rot_matrix_vec : this->pseudoSymmOperators)
        {
            if(op.matrix == same_rot_matrix_vec[0].matrix)
            {
                for (const auto& one_op_from_same_matrix : same_rot_matrix_vec)
                {
                    if (op.vector_affine == one_op_from_same_matrix.vector_affine) 
                    {
                        vectorIsAdded = true;
                        break;
                    }
                }
                
                if(!vectorIsAdded) 
                {
                    same_rot_matrix_vec.emplace_back(op);
                    vectorIsAdded = true;
                    break;
                }
            }
        }

        if(this->pseudoSymmOperators.empty() || !vectorIsAdded)
        {
            vector<SymmOperator> new_same_rot_matrix_vec;
            new_same_rot_matrix_vec.emplace_back(op);
            this->pseudoSymmOperators.emplace_back(new_same_rot_matrix_vec);
        }
    }
}

void Structure::prepareStructure(vector<SymmOperator>& operators, const double& resolution, const bool& noHydrogens)
{
    // Представляем базисные векторы ячейки в "декарте"
    vecA = cell.cartesianBasis.row(0);
    vecB = cell.cartesianBasis.row(1);
    vecC = cell.cartesianBasis.row(2);

    // Вычисляем модули векторов обратной решетки
    // По сути, они нужны только для вычисления индексов h, k, l (разрешение)
    recipA = vecB.cross(vecC)/cell.volume;
    recipB = vecC.cross(vecA)/cell.volume;
    recipC = vecA.cross(vecB)/cell.volume;

    // Индексы h, k, l минимальные (по модулю) и максимальные 
    hMax = floor(1.0/(resolution*recipA.norm()));
    kMax = floor(1.0/(resolution*recipB.norm()));
    lMax = floor(1.0/(resolution*recipC.norm()));

    stepA = (1.0/(2*hMax+1))*vecA;
    stepB = (1.0/(2*kMax+1))*vecB;
    stepC = (1.0/(2*lMax+1))*vecC;

    // Для всех атомов создаем декартовые радиус-векторы
    _prepareAtomsToCalc();
    // Формируем сетку для ухода от вложенных циклов
    _createLoopGrid();
    // Распределеяем операторы
    _allocateOperators(operators);
    // Трансформируем введенные координаты векторов операторов для данной структуры в абсолютный декартов базис
    _transformOpVecsToCart();
    
}

// Вроде можно использовать абсолютно любые индексы
// Но в программе берутся только положительные!
vectorH Structure::calcHVector(const int& h, const int& k, const int& l)
{
    return (h*recipA + k*recipB + l*recipC);
}

// H-вектор должен быть несдвинутым (не M вектор)
complex<double> Structure::calcStrAmp(const vectorH& H)
{
    const double stl = calcSTL(H);

    double ampRe = 0.0;
    double ampIm = 0.0;

    for (auto& atom : cell.atoms)
    {
        const double scatFac = atom.calcScatFactor(stl);
        const double phase = -Consts::dPi*(H.dot(atom.xyz));
        const double sof = atom.sof; 

        ampRe += scatFac * sof * cos(phase);
        ampIm += scatFac * sof * sin(phase);
    }

    return complex<double>(ampRe, ampIm);
}

void Structure::prepareStructureMaps(const double& resolution, const int& maxThreads)
{
    // Выделяем память для M, H, D и F - карт
    mapM = std::make_unique<MapM>(2*hMax+1, 2*kMax+1, 2*lMax+1);
    mapH = std::make_unique<MapH>(2*hMax+1, 2*kMax+1, 2*lMax+1);
    mapD = std::make_unique<MapD>(2*hMax+1, 2*kMax+1, 2*lMax+1);
    mapF = std::make_unique<MapF>(2*hMax+1, 2*kMax+1, 2*lMax+1);

    // И для G-карты тоже (их может быть много - создаем пока пустые)
    for (const auto& op : pseudoSymmOperators)
    {
        mapsG.emplace_back(MapG{2*hMax+1, 2*kMax+1, 2*lMax+1});
    }

    const vectorH maxHVec = this->calcHVector(hMax, kMax, lMax);

    double localNormCoeff = 0;
    omp_set_num_threads(maxThreads);
    #pragma omp parallel for schedule(dynamic, 2000) reduction(+:localNormCoeff)
    for(int q = 0; q < loopGrid.size(); q++)
    {
        // Распакоука!!!!
        const int& h = loopGrid[q][0]; const int& k = loopGrid[q][1]; const int& l = loopGrid[q][2];

        const vectorH newVectorM = this->calcHVector(h, k, l);
        (*mapM)(h, k, l) = newVectorM;

        const vectorH newVectorH = newVectorM - maxHVec;
        (*mapH)(h, k, l) = newVectorH;

        const double dCurrent = calcPlanarDistance(newVectorH);
        (*mapD)(h, k, l) = dCurrent;

        if (dCurrent >= resolution)
        {
            const complex<double> F = calcStrAmp(newVectorH);
            (*mapF)(h, k, l) = F;

            // Заодно расчитываем нормирующий коэффициент
            localNormCoeff += abs(F)*abs(F);

            // А тут формируем G-карты для всех точечных операторов
            for (int i = 0; i < pseudoSymmOperators.size(); i++)
            {
                const Matrix3d rotMatr = pseudoSymmOperators[i][0].matrix;
                const vectorH conjugatedH = (-1.0)*(rotMatr.transpose()*newVectorH);

                // Считаем G-фурье коэффициент
                complex<double> G = F*calcStrAmp(conjugatedH);

                // Меняем на соотвествтующей G-карте значения по индексам h, k, l
                // Так как у нас тип complex<double>, а там fftw_complex - то так, через сеттер
                // !!!!! Может можно переобозначить оператор, но потом !!!!!!
                mapsG[i].setValG(h, k, l, G);
            }
        }
        else
        {
            // Если вне разрешения, то F = 0 + i0 и G = 0 + i0
            // Причем для всех G по данному индексу
            (*mapF)(h, k, l) = complex<double>(0.0, 0.0);

            for (int i = 0; i < pseudoSymmOperators.size(); i++)
            {
                const complex<double> G{0.0, 0.0};
                mapsG[i].setValG(h, k, l, G);
            }
        }
    }
    this->normCoeff = localNormCoeff;
}

void Structure::createMapsEta()
{
    // Создаем пустые карты и сразу записываем в них фурье-преобразование
    for (int i = 0; i < mapsG.size(); i++)
    {
        mapsEta.emplace_back(MapEta{2*hMax+1, 2*kMax+1, 2*lMax+1});
        mapsG[i].transform(mapsEta[i]);
    }
    
    const vectorH maxVecH = (*mapM).getVectorM(hMax, kMax, lMax);

    // Теперь нормируем полученные эта-карты
    for (const auto& indices : loopGrid)
    {
        const int& x = indices[0];
        const int& y = indices[1];
        const int& z = indices[2];

        const Vector3d aVec = x*stepA;
        const Vector3d bVec = y*stepB;
        const Vector3d cVec = z*stepC;

        const double dot = maxVecH.dot(aVec + bVec + cVec); // Скалярное произведение вектора H на сумму векторов трансляций
        const complex<double> phase = exp(2.0*Consts::Pi*Consts::I*dot);

        for (int i = 0; i < mapsG.size(); i++)
        {
            mapsEta[i].setEta(x, y, z, mapsEta[i].getEta(x, y, z)*phase/normCoeff);
        }
    }
}

bool Structure::isLocalEtaMinimum(const int& xGrid, const int& yGrid, const int& zGrid, const int& etaMapIndex)
{
    bool localMax = true;
    const auto& map = mapsEta[etaMapIndex];

    for(const auto& vec : Minimums::aroundVectors)
    {
        int check_x = xGrid + vec[0];
        int check_y = yGrid + vec[1];
        int check_z = zGrid + vec[2];

        if(check_x > map.xSize - 2) {check_x = 0;}
        else if(check_x < 0) {check_x = map.xSize - 2;}

        if(check_y > map.ySize - 2) {check_y = 0;}
        else if(check_y < 0) {check_y = map.ySize - 2;}

        if(check_z > map.zSize - 2) {check_z = 0;}
        else if(check_z < 0) {check_z = map.zSize - 2;}

        if (map.getEta(check_x, check_y, check_z).real() >= map.getEta(xGrid, yGrid, zGrid).real())
        {
            localMax = false;
            break;
        }
    }

    return localMax;
}

void Structure::extractOperators(const double& threshold)
{
    for(const auto& indices : loopGrid)
    {
        const int& x = indices[0];
        const int& y = indices[1];
        const int& z = indices[2];

        for (int i = 0; i < mapsEta.size(); i++)
        {   
            // Сравним реальные части, мнимые должны быть вообще равны нулю или близки к нему
            const complex<double> cVal = mapsEta[i].getEta(x, y, z);
            const double dVal = mapsEta[i].getEta(x, y, z).real();
            
            if(dVal >= threshold)
            {
                if (isLocalEtaMinimum(x, y, z, i))
                {
                    pseudoSymmOperators[i].emplace_back(SymmOperator{pseudoSymmOperators[i][0].matrix, 
                                                                    x*stepA + y*stepB + z*stepC, 
                                                                    pseudoSymmOperators[i][0].name, 
                                                                    cVal});
                }
            }
        }
    }
}

void Structure::refineAllPseudoOperators(const double& resolution, const double& precision, const int& maxCycles)
{   
    int cycle = 0; 
    bool refinedAll = false;

    // Коэффициенты A, B, C для решения квадратного уравнения для каждого оператора
    // Первый вектор - это также как и распредедление операторов по одной матрице поворота
    // Второй вектор - это разные операторы с одной матрицей. Уточнять надо все!
    // Массив - это координаты, так как каждая составляющая отвечает за добавочный вектор (его компоненту)
    vector<vector<array<complex<double>, 3>>> coeffsA;
    vector<vector<array<complex<double>, 3>>> coeffsB;
    vector<vector<array<complex<double>, 3>>> coeffsC;

    // Подготовим эти массивы данных
    for(int i = 0; i < pseudoSymmOperators.size(); i++)
    {
        coeffsA.emplace_back(vector<array<complex<double>,3>>{});
        coeffsB.emplace_back(vector<array<complex<double>,3>>{});
        coeffsC.emplace_back(vector<array<complex<double>,3>>{});

        for (const auto& op : pseudoSymmOperators[i])
        {
            coeffsA[i].emplace_back(array<complex<double>, 3>{0, 0, 0});
            coeffsB[i].emplace_back(array<complex<double>, 3>{0, 0, 0});
            coeffsC[i].emplace_back(array<complex<double>, 3>{0, 0, 0});
        }
    }

    while (cycle <= maxCycles && !refinedAll)
    {
        // Потом флаги уточненности всех операторов умножим на него, 
        // если все будут true, то цикл завершится на следующей итерации!
        refinedAll = true;

        // Создаем локальные переменные для использования в OpenMP, т.к. это члены класса
        // Они будут вместо CoeffsA/B/C, Для редукции. Потом все полученные результаты в потоках объединим
        vector<vector<vector<array<complex<double>, 3>>>> localA(omp_get_max_threads());
        vector<vector<vector<array<complex<double>, 3>>>> localB(omp_get_max_threads());
        vector<vector<vector<array<complex<double>, 3>>>> localC(omp_get_max_threads());

        // Заполняем нулями эти массивы данных
        for (int t = 0; t < omp_get_max_threads(); ++t) 
        {
            for(int i = 0; i < pseudoSymmOperators.size(); i++)
            {
                localA[t].emplace_back(vector<array<complex<double>,3>>{});
                localB[t].emplace_back(vector<array<complex<double>,3>>{});
                localC[t].emplace_back(vector<array<complex<double>,3>>{});

                for (const auto& op : pseudoSymmOperators[i])
                {
                    localA[t][i].emplace_back(array<complex<double>, 3>{0, 0, 0});
                    localB[t][i].emplace_back(array<complex<double>, 3>{0, 0, 0});
                    localC[t][i].emplace_back(array<complex<double>, 3>{0, 0, 0});
                }
            }
        }

        // Подготовка коэффициентов для решения уравнения уточнения для каждого оператора
        #pragma omp parallel
        {
            int tid = omp_get_thread_num();

            #pragma omp for schedule(guided)
            for(int o = 0; o < loopGrid.size(); o++)
            {
                const int& h = loopGrid[o][0]; const int& k = loopGrid[o][1]; const int& l = loopGrid[o][2];

                // Надо, чтобы межплоскостное расстояние было больше или равно заданному разрешением
                if ((*mapD).getPlanDist(h, k, l) < resolution) continue;

                const vectorH& M = (*mapM).getVectorM(h, k, l);
                const vectorH& H = (*mapH).getVectorH(h, k, l);

                // Перебираем все имеющиеся операторы псевдосимметрии
                for(int i = 0; i < pseudoSymmOperators.size(); i++)
                {
                    // Достаем G-карты для данных операторов
                    const complex<double> G = mapsG[i](h, k, l);

                    // Теперь перебираем все трансляции, доступные для данной матрицы поворота оператора псевдосимметрии
                    for (int j = 0; j < pseudoSymmOperators[i].size(); j++)
                    {
                        // Если трансляция не уточнена, то для нее считаем коэффициенты A, B, C для решения квадратного уравнения
                        if (pseudoSymmOperators[i][j].refined) continue;
                        
                        const double dot = H.dot(pseudoSymmOperators[i][j].vector);
                        const complex<double> expon = exp(-Consts::dPi*Consts::I*dot);
                        
                        for(int q = 0; q < 3; q++)
                        {
                            localA[tid][i][j][q] += -2.0 * Consts::I * Consts::Pi * M[q] * Consts::Pi * M[q] * H[q] * G * expon;
                            localB[tid][i][j][q] += Consts::dPi * M[q] * H[q] * G * expon;
                            localC[tid][i][j][q] += Consts::I * H[q] * G * expon;
                        }
                    }
                }
            }
        } // end OMP PARALLEL ...
        
        // Теперь объединяем все результаты, полученные в локальных копиях в одном потоке
        for (int t = 0; t < omp_get_max_threads(); t++) 
        {
            for (size_t i = 0; i < pseudoSymmOperators.size(); i++) 
            {
                for (size_t j = 0; j < pseudoSymmOperators[i].size(); j++) 
                {
                    for (int q = 0; q < 3; q++) 
                    {
                        coeffsA[i][j][q] += localA[t][i][j][q];
                        coeffsB[i][j][q] += localB[t][i][j][q];
                        coeffsC[i][j][q] += localC[t][i][j][q];
                    }
                }
            }
        }

        // Теперь уточняем все операторы сразу
        for(int i = 0; i < pseudoSymmOperators.size(); i++)
        {
            for (int j = 0; j < pseudoSymmOperators[i].size(); j++)
            {
                if (!pseudoSymmOperators[i][j].refined)
                {
                    array<complex<double>, 3> delta{0, 0, 0};

                    // k - это индекс координаты, DELTA_x[0], DELTA_y[1], DELTA_z[2]
                    for(int k = 0; k < 3; k++)
                    {
                        delta[k] = (-1.0*coeffsB[i][j][k] + sqrt(pow(coeffsB[i][j][k], 2) - 4.0*coeffsA[i][j][k]*coeffsC[i][j][k]))/(2.0*coeffsA[i][j][k]);
                    
                        // Обнуляем для каждого оператора A, B, C - коэффициенты
                        coeffsA[i][j][k] = complex<double>{0.0, 0.0};
                        coeffsB[i][j][k] = complex<double>{0.0, 0.0};
                        coeffsC[i][j][k] = complex<double>{0.0, 0.0};
                    }

                    transOperator deltaVector{delta[0].real(), delta[1].real(), delta[2].real()};
                    pseudoSymmOperators[i][j].vector += deltaVector;

                    // Больше его не уточняем, если норма меньше точности
                    if (abs(deltaVector[0]) < precision && abs(deltaVector[1]) < precision && abs(deltaVector[2]) < precision)
                    {
                        pseudoSymmOperators[i][j].refined = true;
                    }
                }
                refinedAll &= pseudoSymmOperators[i][j].refined;
            }
        }
        // Цикл уточнения завершен!
        cycle++;
    }
}

void Structure::recalcEtaForAll(const double& resolution)
{
    // Инициализируем newEtas правильного размера с нулями
    vector<vector<complex<double>>> newEtas(pseudoSymmOperators.size());
    for (int i = 0; i < pseudoSymmOperators.size(); i++) 
    {
        newEtas[i].resize(pseudoSymmOperators[i].size(), complex<double>{0, 0});
    }

    // Локальные массивы для каждого потока
    vector<vector<vector<complex<double>>>> localNewEtas(omp_get_max_threads());
    for (int t = 0; t < omp_get_max_threads(); t++) 
    {
        localNewEtas[t].resize(pseudoSymmOperators.size());
        for (int i = 0; i < pseudoSymmOperators.size(); i++) 
        {
            localNewEtas[t][i].resize(pseudoSymmOperators[i].size(), complex<double>{0, 0});
        }
    }
    
    #pragma omp parallel
    {
        int tid = omp_get_thread_num();

        // Считаем ЭТУ на основе G-коэффициентов, прямо в лоб, по формуле
        #pragma omp for schedule(guided)
        for(int q = 0; q < loopGrid.size(); q++)
        {
            const int& h = loopGrid[q][0]; 
            const int& k = loopGrid[q][1]; 
            const int& l = loopGrid[q][2];

            // Критерий на разрешение и межплоскостное расстояние
            if ((*mapD).getPlanDist(h, k, l) < resolution) continue;

            const auto& M = (*mapM)(h, k, l);
            for(int i = 0; i < pseudoSymmOperators.size(); i++)
            {
                const complex<double> G = mapsG[i](h, k, l);
                for (int j = 0; j < pseudoSymmOperators[i].size(); j++)
                {
                    const double dot = M.dot(pseudoSymmOperators[i][j].vector);
                    const complex<double> expon = exp(-Consts::dPi*Consts::I*dot);
                    localNewEtas[tid][i][j] += G*expon;
                }
            }
        }
    }

    const vectorH& maxVecH = (*mapM)(hMax, kMax, lMax);

    // Теперь просуммируем отдельные потоки жи есь!
    for (int t = 0; t < omp_get_max_threads(); t++) 
    {
        for (size_t i = 0; i < pseudoSymmOperators.size(); i++) 
        {
            for (size_t j = 0; j < pseudoSymmOperators[i].size(); j++) 
            {
                newEtas[i][j] += localNewEtas[t][i][j];
            }
        }
    }

    // Теперь их надо отнормировать и записать новое значение в оператор
    for(int i = 0; i < pseudoSymmOperators.size(); i++)
    {
        for (int j = 0; j < pseudoSymmOperators[i].size(); j++)
        {
            const complex<double> phaseCoeff = exp(Consts::dPi*Consts::I*maxVecH.dot(pseudoSymmOperators[i][j].vector));
            pseudoSymmOperators[i][j].eta = newEtas[i][j]*phaseCoeff/normCoeff;
        }
    }
}

void Structure::sortOperatorsByEta(bool descending)
{
    for (auto& opVec : pseudoSymmOperators)
    {
        if (descending)
        {
            std::sort(opVec.begin(), opVec.end(), [](const auto& a, const auto& b) { return a.eta.real() > b.eta.real(); });
        }
        else
        {
            std::sort(opVec.begin(), opVec.end(), [](const auto& a, const auto& b) { return a.eta.real() < b.eta.real(); });
        }
    }
}

void Structure::removeDuplicatePsOps(const double& precision)
{   
    // Сортируем каждый массив с одинаковыми матрицами поворота отдельно
    for (auto& ops : pseudoSymmOperators)
    {
        // Будем собирать новый вектор
        vector<SymmOperator> newVec = ops;
        newVec.reserve(ops.size());

        int i = 0;
        while (i != newVec.size())
        {
            int j = i + 1;
            while (j != newVec.size())
            {
                const Vector3d vecDiff = newVec[i].vector - newVec[j].vector;
                const double etaDiff = newVec[i].eta.real() - newVec[j].eta.real();

                // Если разница больше точности, то это не дубликат
                if ((abs(vecDiff[0]) < precision) && (abs(vecDiff[1]) < precision) && (abs(vecDiff[2]) < precision) &&  (abs(etaDiff) < precision))
                {
                    newVec.erase(newVec.begin() + j);
                }
                else
                {
                    ++j;
                }
            }
            ++i;
        }
        newVec.shrink_to_fit();
        ops = std::move(newVec);
    }
}

inline double _normalize_acos_in_deg(const double& cos_val)
{
    if(cos_val >= 1.0) return 0;
    return toDeg(acos(cos_val));
}

void Structure::calc_basis_angles()
{
    const Vector3d a_cart = cell.cartesianBasis.row(0);
    const Vector3d b_cart = cell.cartesianBasis.row(1);
    const Vector3d c_cart = cell.cartesianBasis.row(2);

    const double norm_a = a_cart.norm();
    const double norm_b = b_cart.norm();
    const double norm_c = c_cart.norm();

    for (auto& opVec : pseudoSymmOperators)
    {
        for(auto& op : opVec)
        {
            const double norm_op = op.vector.norm();

            if(!isZero(norm_op))
            {
                const double cos_a = cell.cartesianBasis.row(0).dot(op.vector)/(norm_a*norm_op);
                const double cos_b = cell.cartesianBasis.row(1).dot(op.vector)/(norm_b*norm_op);
                const double cos_c = cell.cartesianBasis.row(2).dot(op.vector)/(norm_c*norm_op);

                op.vec_a_angle = _normalize_acos_in_deg(cos_a);
                op.vec_b_angle = _normalize_acos_in_deg(cos_b);
                op.vec_c_angle = _normalize_acos_in_deg(cos_c);
            }   
        }
    }
}

void Structure::representOpsInAffine()
{
    for (auto& opVec : pseudoSymmOperators)
    {
        for(auto& op : opVec)
        {
            Vector3d tVecAff{0, 0, 0};

            if(cell.isSuperCell) tVecAff = (cell.cartesianBasis/cell.supCellFac).transpose().inverse() * (op.vector - cell.supCellShift);
            else tVecAff = cell.cartesianBasis.transpose().inverse() * op.vector;

            op.vector_affine = tVecAff;
        }
    }
}

void Structure::showPseudoOpsInfo(const int& maxOutput, const int& digits)
{
    for (auto& opVec : pseudoSymmOperators)
    {
        int shown = 0;
        std::cout << "INPUT_MATRIX:" << std::endl;
        std::cout << opVec[0].matrix << std::endl;
        
        for(auto& op : opVec)   
        {   
            std::cout << "OUTPUT_TRANSLATION_CART:" << std::endl;
            const std::string x{strRoundTo(op.vector[0], digits)};
            const std::string y{strRoundTo(op.vector[1], digits)};
            const std::string z{strRoundTo(op.vector[2], digits)};
            std::cout << "    " << x << " " << y << " " << z << std::endl;
            std::cout << "OUTPUT_TRANSLATION_AFFN:" << std::endl;
            const std::string x_affine{strRoundTo(op.vector_affine[0], digits)};
            const std::string y_affine{strRoundTo(op.vector_affine[1], digits)};
            const std::string z_affine{strRoundTo(op.vector_affine[2], digits)};
            std::cout << "    " << x_affine << " " << y_affine << " " << z_affine << std::endl;
            std::cout << "BASIS ANGLES:" << std::endl;
            const std::string angle_a{strRoundTo(op.vec_a_angle, digits)};
            const std::string angle_b{strRoundTo(op.vec_b_angle, digits)};
            const std::string angle_c{strRoundTo(op.vec_c_angle, digits)};
            std::cout << "    " << angle_a << " deg. " << angle_b << " deg. " << angle_c << " deg."<<std::endl;
            std::cout << "OUTPUT_ETA:" << std::endl;
            const std::string eta{strRoundTo(op.eta.real(), digits)};
            std::cout << "    " << eta << std::endl;
            shown++;
            
            // Если показано максимальное значение (нужное для вывода), то выходим из функции
            if(shown == maxOutput) break;
        }
    }
}

void Structure::showStructureInfo()
{
    std::cout << "ATOMS:" << std::endl;

    for (auto& atom : cell.atoms)
    {
        std::cout << atom.name << " " << atom.element << " " << strRoundTo(atom.x, 5) << " " <<  strRoundTo(atom.y, 5) << " " << strRoundTo(atom.z, 5) << std::endl;
    }
}

void Structure::extend(const int& radius)
{
    if(radius <= 0) return;

    this->cell.extendToSuperCell(radius);
}

