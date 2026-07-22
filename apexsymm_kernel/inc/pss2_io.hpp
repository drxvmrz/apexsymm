#ifndef PSS2_IO
#define PSS2_IO

#include "json.hpp"

#include "pss2_basic_types.hpp"
#include "pss2_cif_reader.hpp"
#include "pss2_static_consts.hpp"
#include "pss2_CLI_interface.hpp"

using json = nlohmann::ordered_json;

namespace PssBasicIO
{
    int send_error_msg(const int& code);
    void add_json_results(const CifReader& reader, const CLIParser& cmdSettings);
}

class PssJSONwriter
{
    public:
        fs::path path{};
        std::string string_path{};

        PssJSONwriter();

        // Задает новый путь для сохранения json-файла
        void apply_path(const fs::path& path);
        void apply_path(const std::string& path);

        // Проверяет, создал ли файл
        bool is_created();

        // Создает файл с начальными данными (настройки)
        void create_file(const CLIParser& cmd_settings);

        // Добавляет структуру в файл с результатами
        void add_results(const CifReader& reader, const long long& time);
    
    private:
        json read_data();
};

#endif