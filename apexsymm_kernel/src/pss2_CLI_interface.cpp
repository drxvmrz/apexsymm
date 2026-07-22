#include "pss2_CLI_interface.hpp"

CLIParser::CLIParser()
{
    const char* appDescription = "Calc the pseudosymmetry of structures (in CIF_PATH file)"
                                 "\nfor list of pseudosymmetry OPERATORS";

    const char* operatorsDescription = "Add operators. Syntax 'op1;op2;...', where:"
                                       "\n'op1' is 'a11 a12 a13/a21 a22 a23/a31 a32 a33/x y z'. \nIt means:"
                                       "(rotation matrix)/(relative coords vector of cell)\n";

    const char* resolutionDescription = "Resolution of H-vector grid in Angstrems"
                                        "\nIt's an minimal interplanar space\nDefault = 0.5\n";

    const char* thresholdDescription = "Threshold value for counting the operator in refinement"
                                       "\nDefault = 0.2\n";

    const char* precisionDescription = "Precision value for operators translation refinement"
                                       "\nDefault = 1E-8\n";

    const char* maxOutDescritpion = "How many operators with highest eta-value will be outputed."
                                    "\nIt will be outputed INT units for each different rotation matrix."
                                    "\nDefault = 10\n";

    const char* maxCyclesDescription = "Max of refinement cycles. If the operator could not be refined within this amount,"
                                       "\nit will be discarded. \nDefault = 10\n";
        
    const char* superCellDesctription = "Using a supercell for calculation! " 
                                        "\nIt will be created ((INT x INT x INT) - 1) cells around the original.\n"
                                        "They will be united and cosidered as only one while calculation process!\n"
                                        "INT value should be odd!\n";
    
    const char* maxThreadsDescription = "The max number of threads that will be used for calculation! " 
                                        "\nThe number (INT) should be a positive!\n";

    const char* saveJSONDescription = "Save results into a .json-file on <PATH>.\n";

    const char* noRefDescription = "Use this flag if you need only calculate pseudosymmetry."
                                   "\nIn this case, the operator's translation will not be refined!\n";

    const char* noHydroDescription = "Does not take hydrogen atoms into account"
                                     "\nin the calculation and refinement process\n";
                                        
    workspace = AddWorkspace("USAGE: 'apexcore <options> OPERATORS CIF_PATH' or 'apexcore OPERATORS CIF_PATH <options>'", appDescription);

    // Auto-assembly help argument
    AddHelpArg(&workspace, "--help", "-h");

    // Required arguments
    AddNonOptArg(&workspace, "OPERATORS", operatorsDescription, &cOperators);
    AddNonOptArg(&workspace, "CIF_PATH", "Path to the .cif-file or .cif-files (if '<path>/*')", &cCifPath);
    
    // Valuable Opt Args
    AddOptArg(&workspace, "--resolution", "-rs", resolutionDescription, "DBL", &cResolution);
    AddOptArg(&workspace, "--threshold", "-t", thresholdDescription, "DBL", &cThreshold);
    AddOptArg(&workspace, "--precision", "-p", precisionDescription, "DBL", &cPrecision);
    AddOptArg(&workspace, "--maxoutput", "-mo", maxOutDescritpion, "INT", &cMaxOutput);
    AddOptArg(&workspace, "--cycles", "-c", maxCyclesDescription, "INT", &cMaxCycles);
    AddOptArg(&workspace, "--supercell", "-sc", superCellDesctription, "INT", &cSuperCell);
    AddOptArg(&workspace, "--maxthreads", "-cpu", maxThreadsDescription, "INT", &cMaxThreads);
    AddOptArg(&workspace, "--json", "-json", saveJSONDescription, "<PATH>", &cJSONFile);

    // Flags
    AddOptArg(&workspace, "--nohydro", "-nh", noHydroDescription, "", &cNoHydrogens);
    AddOptArg(&workspace, "--norefine", "-nr", noRefDescription, "", &cNoRefine);
}

SCMDPStatus CLIParser::readSettings(int argc, const char *argv[])
{ 
    SCMDPStatus parsingStatus = ParseArgs(&workspace, argc, argv);
    
    if (parsingStatus == SCMDP_GOOD)
    {
        cifFilePath = cCifPath;

        resolution = strtod(cResolution, nullptr);
        threshold = strtod(cThreshold, nullptr);
        precision = strtod(cPrecision, nullptr);

        maxOutput = (int)strtol(cMaxOutput, nullptr, 10);
        maxCycles = (int)strtol(cMaxCycles, nullptr, 10);
        superCell = (int)strtol(cSuperCell, nullptr, 10);
        
        // Максимальное число потоков. Если задан 0, то все, что есть. Или сколько задано
        const int mt = (int)strtol(cMaxThreads, nullptr, 10);
        const int maxAllowed = omp_get_max_threads();
        maxThreads = (mt == 0 || mt >= maxAllowed) ? maxAllowed : mt;

        // Сохранение в файлы
        saveJSONFile = cJSONFile;

        needToRefine = isNeedToRefine();
        noHydrogens = isNoHydrogens();
    
        if(extractOperatorsFromCLI() == false) parsingStatus = SCMDP_BAD;
    }
    
    return parsingStatus;
}

bool CLIParser::isNeedToRefine()
{
    const string noRefStr(cNoRefine);
    // Если в строке есть true, значит передали флаг --norefine - тогда нам не нужно уточнение
    return noRefStr.find("true") == std::string::npos;
}

bool CLIParser::isNoHydrogens()
{
    const string noHydrStr(cNoHydrogens);
    // Если в строке есть true, значит передали флаг --nohydro, тогда не надо учитывать водороды
    return noHydrStr.find("true") != std::string::npos;
}

bool CLIParser::extractOperatorsFromCLI()
{
    bool success = true;
    
    string opsArg(cOperators);
    string opsBuf;
    std::stringstream opsStream(opsArg);
    
    vector<string> splitOps;

    while(getline(opsStream, opsBuf, ';')) splitOps.push_back(opsBuf);
    
    // Сначала считали все операторы, полученные в аргументе, через ; по отдельности
    // nameCounter - для автоназвания оператора, если вдруг ему не будет введено имя, 
    // то присвоится порядковый номер
    int nameCounter = 1;
    for (const string& opString : splitOps)
    {
        // Начинается ли вообще строка с числа или со знака (- или +)
        if(!isdigit(opString[0]) && opString[0] != '-' && opString[0] != '+') return false;

        std::stringstream ss(opString);

        string part_buf;
        vector<string> parts;

        // Разбиваем на части по /, далее будем считывать матрицу и вектор
        while(getline(ss, part_buf, '/')) parts.push_back(part_buf);
        
        // Обязательно должно быть 4 или 5 элементов. 
        // 3 матричные строки + один вектор трансляции, и название опционально (5-я часть)
        if(parts.size() != 4 && parts.size() != 5) return false;

        std::string buf;
        SymmOperator newOperator{"Op" + std::to_string(nameCounter)};

        // Отслеживают, сколько чисел было добавлено в матрицу или вектор
        int matrix_filled = 0;
        int vector_filled = 0;

        for(int i = 0; i < parts.size(); i++)
        {
            for(int j = 0; j < parts[i].size(); j++)
            {
                const bool EOS = j == parts[i].size()-1; // Конец строки
                const char& c = parts[i][j];
                if (c == ' ' && i != 4 || EOS)
                {
                    if (EOS) buf += c;

                    try
                    {
                        if(i < 3) // Заполняется матрица
                        {
                            const int row = matrix_filled / 3;
                            const int col = matrix_filled % 3;
                            newOperator.matrix(row, col) = stod(buf);
                            matrix_filled++;
                        }
                        else if(i == 3) // Заполняется вектор
                        {
                            newOperator.vector_affine[vector_filled] = stod(buf);
                            vector_filled++;
                        }
                        else // Заполняется имя
                        {
                            newOperator.name = buf;
                        }
                        
                        buf.clear();
                    }
                    catch(...)
                    {
                        return false;
                    }
                }
                else
                {
                    buf += c;
                }
            }
        }

        if(vector_filled == 3 && matrix_filled == 9)
        {
            this->operators.emplace_back(std::move(newOperator));
        }
        else
        {
            return false;
        }

        ++nameCounter; // Идем дальше
    }
    return success;
}

bool CLIParser::isSettingsValid()
{
    bool isValid = true;
    
    // optional arguments settings
    isValid &= (resolution > 0.0);
    isValid &= (threshold > 0.0);
    isValid &= (precision > 0.0);
    isValid &= (maxOutput > 0);
    isValid &= (maxCycles > 0);
    isValid &= (superCell >= 0);
    isValid &= (maxThreads >= 0);
    isValid &= saveJSONFile == "" || ((fs::exists(fs::path(saveJSONFile).parent_path()) && saveJSONFile.find(".json") != string::npos));
    
    // flags
    isValid &= (needToRefine == true || needToRefine == false);
    isValid &= (noHydrogens == true || noHydrogens == false);

    return isValid;
}