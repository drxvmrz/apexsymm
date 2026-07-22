#ifndef CLI_PARSER
#define CLI_PARSER

#include "scmdp.h"
#include "omp.h"

#include "pss2_static_consts.hpp"
#include "pss2_symm_operators.hpp"

// Нужно создать только один 
class CLIParser
{
    public:
        // Рабочее пространство SCMPD
        ScmdpWorkspace workspace;
        
        // Обязательные аргументы
        vector<SymmOperator> operators; // Список переданных операторов псевдосимметрии для расчета
        string cifFilePath = ""; // Путь к исследуемому .cif-файлу
        
        // Опциональные аргументы
        double threshold;
        double resolution ; // Разрешение для расчетов
        double precision;

        int maxOutput;
        int maxCycles;
        
        int superCell;

        int maxThreads;
        string saveJSONFile;

        // Опции без значений - флаги
        bool needToRefine = true;
        bool noHydrogens = false;

        CLIParser();

        // Парсит аргументы и переводит их в нормальные переменные для использования
        SCMDPStatus readSettings(int argc, const char *argv[]);

        // Проверяем, все ли введенные настройки из ключей имеют валидные значения?
        bool isSettingsValid();

    // В основном тут используются с-строки для перегона из scmdp
    private:
        const char* cCifPath = "./"; // Путь к рассматриваемому cif-файлу
        const char* cResolution = "0.5"; // Разрешение сетки по h, k, l (дефолтное значение 0.5)
        const char* cThreshold = "0.2";
        const char* cPrecision = "1E-8";
        const char* cOperators;
        const char* cMaxOutput = "10";
        const char* cMaxCycles = "10";
        const char* cSuperCell = "0";
        const char* cMaxThreads = "0";
        const char* cJSONFile = ""; // Путь к сохраняемому .json-файлу. По умолчанию отсутствует, т.к. сохранение в файл не требуется

        const char* cNoRefine = "";
        const char* cNoHydrogens = "";

        bool extractOperatorsFromCLI();

        bool isNeedToRefine();
        bool isNoHydrogens();
    
};

#endif