#ifndef STR_PROC
#define STR_PROC

#include <omp.h>

#include "pss2_basic_types.hpp"
#include "pss2_maps_types.hpp"
#include "pss2_static_consts.hpp"
#include "pss2_basic_math.hpp"

#include "pss2_atoms.hpp"
#include "pss2_cells.hpp"
#include "pss2_symm_operators.hpp"

class Structure
{
    public:
        //////////////////////////////////////////////////////////////////////////////////
        ///////////////////////// Что напрямую определяем из .cif ////////////////////////
        //////////////////////////////////////////////////////////////////////////////////

        string name = ""; // Просто название структуры
        string formula = ""; // Химическая формула
        fs::path cif_path{}; // Путь к .cif-файлу, откуда эта структура

        double xray_temperature = 0.0; // Темепература эксперимента из cif-файла
        unsigned char Z = 0; // Число формульных единиц (пока не знаю, зачем, но пусть будет)

        int hMax, kMax, lMax = 0; // Максимальные значения по h, k, l. По сути индексы обратного пространства
        Vector3d stepA, stepB, stepC; // Векторы шагов по сетке прямого пространства
        Vector3d vecA, vecB, vecC; // Базисные векторы решетки в декартовых координатах
        Vector3d recipA, recipB, recipC; // Базисные векторы обратного пространства в декартовых координатах

        Cell cell; // Элементарная ячейка структуры

        vector<array<int, 3>> loopGrid; // Для ухода от тройного вложенного цикла с перебором индексов i, j, k

        double normCoeff = 0.0; // Нормирующий коэффициент - сумма электронных плотностей в квадрате

        //vector<vector<SymmOperator>> symmOperators; Пока не особо нужен

        // Псевдооператоры должны быть распределены по точечным операторам
        // То есть вектор из векторов, где в каждом векторе разные операторы с одним точечным
        // Индекс точечного оператора должен совпадать с G-картой, соответствующей ему
        vector<vector<SymmOperator>> pseudoSymmOperators;

        /*********** Карты ************/
        std::unique_ptr<MapM> mapM; // M-карта для структуры нужна только одна
        std::unique_ptr<MapH> mapH; // H-карта для структуры тоже только одна
        std::unique_ptr<MapD> mapD; // D-карта тоже одна, она делается на основе H-карты
        std::unique_ptr<MapF> mapF; // F-карта, или карта структурных амплитуд, тоже одна для всей структуры

        vector<MapG> mapsG; // G-карт много, по одной на каждый точечный оператор симметрии
        vector<MapEta> mapsEta; // Сколько G-карт столько и этта-карт 

        Structure() = default;
        ~Structure() = default;

        Structure(Structure&&) = default;
        Structure& operator=(Structure&&) = default;

        Structure(const Structure&) = delete;
        Structure& operator=(const Structure&) = delete;

        // Подготовительные расчеты для структуры
        void prepareStructure(vector<SymmOperator>& operators, const double& resolution, const bool& noHydrogens);

        // Создает карты H, M, D, F и G
        // Их можно создать внутри одного цикла, что полезно для оптимизации
        void prepareStructureMaps(const double& resolution, const int& maxThreads);

        /* С эта-картой можно работать только после преобразования, поэтому ее в отдельный цикл -> функцию
           Плюс, может быть ее и нет нужды вызывать */
        void createMapsEta();

        // Расчитывает вектор обратной решетки по индексам Миллера
        vectorH calcHVector(const int& h, const int& k, const int& l);

        // Рассчиытвает структурную амплитуду
        complex<double> calcStrAmp(const vectorH& H);

        // Определяет, является ли точка x, y, z - локальным минимумом на этта-карте
        bool isLocalEtaMinimum(const int& xGrid, const int& yGrid, const int& zGrid, const int& etaMapIndex);

        // Достаем операторы из Eta-карты
        void extractOperators(const double& threshold);

        // Пересчитываем для всех степени инвариантности
        void recalcEtaForAll(const double& resolution);

        // Уточняет все имеющиеся операторы псевдосимметрии в структуре
        void refineAllPseudoOperators(const double& resolution, const double& precision, const int& maxCycles);

        // Сортируем в список по значению "эта", от большего к меньшему (по умолчанию, можно и наоборот)
        void sortOperatorsByEta(bool descending = true);

        // Удаляет дубликаты (такие могут быть, когда введенный оператор совпадает с найденным)
        void removeDuplicatePsOps(const double& precision);

        // Считает углы между трансляцией оператора и базисом решетки (для всех операторов структуры)
        void calc_basis_angles();

        // Представляет векторы операторов в относительных координатах афинного базиса
        void representOpsInAffine();

        // Выводит информацию об операторах в консоль. Число знаков после запятой - digits 
        void showPseudoOpsInfo(const int& maxOutput, const int& digits = 4);

        // Выводит информацию о структуре (на всякий)
        void showStructureInfo();

        // Расширяет структуру до суперструктуры
        void extend(const int& radius);

    private:
        /* Вспомогательные функции подготовки структуры -> (prepareStructure()) */
        void _prepareAtomsToCalc();
        void _createLoopGrid();
        void _transformOpVecsToCart();
        void _allocateOperators(const vector<SymmOperator>& operators);
};

#endif // STR_PROC