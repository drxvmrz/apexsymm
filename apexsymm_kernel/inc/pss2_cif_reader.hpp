#ifndef CIF_READER
#define CIF_READER

#include "cif.hpp"
#include "pss2_structures.hpp"

class CifReader
{
    public:
        // Главный путь к циф-файлу или к папке (который параметр командной строки)
        const fs::path cif_main_path{};

        // Все доступные .cif-файлы по пути cif_main_path,
        // Если там файл, то в векторе будет 1 элемент, равный cif_main_path
        static inline vector<fs::path> cif_file_paths{};

        // Структуры из одного .cif-файла
        vector<Structure> current_structures;

        CifReader(const string& path);

        // Получить все имеющиеся пути к .cif-файлам
        // Если передается папка, то будет много, если файл, - то один
        bool get_available_cif_paths();
        // Сколько есть доступных .cif-файлов
        int count_cif();
        // Прочитать из .cif-файла все структуры по итератору
        bool get_structures_data(const string& cif_path, bool noHydrogens);
        // Очищаем структуры (предыдущие, из других .cif для добавления новых);
        void clear_previous_data();

        // Просто проверяет существует ли данный путь и содержатся ли по нему .cif-файл(ы)
        static bool is_cif_path_exist(const string& path);
    private:   
        // Блоки данных из одного .cif-файла
        vector<cif::CifBlock> cif_blocks;

        // Собирает cif-блоки в файле по пути файла
        void collect_cif_blocks(const string& path);
};

#endif