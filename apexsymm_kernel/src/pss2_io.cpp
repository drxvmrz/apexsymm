#include "pss2_io.hpp"

/*
    Class PssJSONwriter
*/

inline std::string get_platform_info()
{
    #ifdef _WIN64
    return "Windows 64-bit";
    #elif _WIN32
    return "Windows 32-bit";
    #elif __APPLE__ || __MACH__
    return "macOS";
    #elif __linux__
    return "Linux";
    #elif __FreeBSD__
    return "FreeBSD";
    #elif __unix || __unix__
    return "Unix";
    #else
    return "Unknown OS";
    #endif
}

// Переводит информацию об операторе псевдосимметрии в json
inline void operator_to_json(json& j, const SymmOperator& op)
{
    json jf{
        {"name", op.name},
        {"eta", round(op.eta.real()*1000)/1000},
        // Матрица оператора
        {"a11", op.matrix(0, 0)},
        {"a12", op.matrix(0, 1)},
        {"a13", op.matrix(0, 2)},
        {"a21", op.matrix(1, 0)},
        {"a22", op.matrix(1, 1)},
        {"a23", op.matrix(1, 2)},
        {"a31", op.matrix(2, 0)},
        {"a32", op.matrix(2, 1)},
        {"a33", op.matrix(2, 2)},
        // Трансляционная часть в декарте
        {"t1_cart", op.vector(0)},
        {"t2_cart", op.vector(1)},
        {"t3_cart", op.vector(2)},
        // Углы между трансляцией и базисом решетки структуры
        {"a_angle", op.vec_a_angle},
        {"b_angle", op.vec_b_angle},
        {"c_angle", op.vec_c_angle},
        // Трансляционная часть в декарте
        {"t1_affn", op.vector_affine(0)},
        {"t2_affn", op.vector_affine(1)},
        {"t3_affn", op.vector_affine(2)},
    };

    j["operators"].push_back(jf);
}

// Переводит структуру из циф-ридера в json для добавления туда же
inline void struct_to_json(json& j, const Structure& structure)
{
    json jf{
        {"name", structure.name},
        {"from_cif", structure.cif_path.u8string()},
        {"space_group", structure.cell.spaceGroupSymm},
        {"space_group_num", structure.cell.spaceGroupNum},
        {"a", structure.cell.a},
        {"ax", structure.cell.cartesianBasis(0,0)},
        {"ay", structure.cell.cartesianBasis(0,1)},
        {"az", structure.cell.cartesianBasis(0,2)},
        {"b", structure.cell.b},
        {"bx", structure.cell.cartesianBasis(1,0)},
        {"by", structure.cell.cartesianBasis(1,1)},
        {"bz", structure.cell.cartesianBasis(1,2)},
        {"c", structure.cell.c},
        {"cx", structure.cell.cartesianBasis(2,0)},
        {"cy", structure.cell.cartesianBasis(2,1)},
        {"cz", structure.cell.cartesianBasis(2,2)},
        {"alpha", structure.cell.alpha},
        {"beta", structure.cell.beta},
        {"gamma", structure.cell.gamma},
        {"operators", json::array()}
    };

    for(const auto& op_vec : structure.pseudoSymmOperators)
    {
        for(const auto& op : op_vec)
        {
            operator_to_json(jf, op);
        }
    }

    j["structures"].push_back(jf);
}

PssJSONwriter::PssJSONwriter() {}

void PssJSONwriter::apply_path(const std::string& path)
{
    this->path = fs::path{path};
    this->string_path = path;
}

void PssJSONwriter::apply_path(const fs::path& path)
{
    this->path = path;
    this->string_path = path.string();
}

bool PssJSONwriter::is_created()
{
    return fs::exists(this->path);
}

json PssJSONwriter::read_data()
{
    json data;
    std::ifstream file(this->string_path);
    
    if(file.is_open())
    {
        file >> data;
        file.close();
    }

    return data;
}

void PssJSONwriter::create_file(const CLIParser& cmd_settings)
{
    // Проверяет, есть ли директория
    const fs::path dir_path = this->path.parent_path();

    if(this->is_created()) { return; }
    if(!fs::exists(dir_path)) { PssBasicIO::send_error_msg(105); return; }
    else
    {
        json final_json
        {
            {"apexcore_version", "0.9.9"},
            {"platform", get_platform_info()},
            {"time", 0.0},
            {"threads", cmd_settings.maxThreads},
            {"refined", cmd_settings.needToRefine},
            {"precision", cmd_settings.precision},
            {"threshold", cmd_settings.threshold},
            {"resolution", cmd_settings.resolution},
            {"supercell", cmd_settings.superCell},
            {"structures", json::array()}
        };

        std::ofstream json_file(this->path.string());
        json_file << final_json.dump(4);
        json_file.close();
    }
}

void PssJSONwriter::add_results(const CifReader& reader, const long long& time)
{
    json data = this->read_data();

    data["time"] = time;
    for(const auto& structure : reader.current_structures) 
    {
        struct_to_json(data, structure);
    }

    std::ofstream file(this->path);
    if(file.is_open())
    {
        file << data.dump(4);
        file.close();
    }
}

int PssBasicIO::send_error_msg(const int& code)
{
    switch(code)
    {
        case 100:
            std::cout << ErrMsg::ERROR_WRONG_INPUT << std::endl;
            break;
        case 101:
            std::cout << ErrMsg::ERROR_FILE_NOT_FOUND << std::endl;
            break;
        case 102:
            std::cout << ErrMsg::ERROR_BROKEN_CIF << std::endl;
            break;
        case 103:
            std::cout << ErrMsg::ERROR_NO_SUITABLE_STRUCTURES << std::endl;
            break;
        case 104:
            std::cout << ErrMsg::ERROR_NO_SUITABLE_CIF_FILES << std::endl;
            break;
        case 105:
            std::cout << ErrMsg::ERROR_WRONG_PATH << std::endl;
            break;
        default:
            std::cout << ErrMsg::ERROR_UNKNOWN << std::endl;
            break;
    }
    return code;
}


