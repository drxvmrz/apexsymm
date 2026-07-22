#include "pss2_cif_reader.hpp"

// С именем там все довольно трудно, поэтому лучше вынести в отдельную функцию
// Пока пусть будет data_<...>
inline static void _extract_structure_name(cif::CifBlock& cifBlock, Structure& structure)
{
    structure.name = cifBlock.name;
}

// базовая информация о структуре, кроме имени: формула и группа симметрии
inline static void _initBaseInfoStructure(cif::CifBlock& cifBlock, Structure& structure)
{ 
    structure.formula = get_value(cifBlock, "_chemical_formula_moiety", "My formula");
    structure.cell.syngony = get_value(cifBlock, "_symmetry_cell_setting", "My syngony");
    structure.cell.spaceGroupSymm = get_value(cifBlock, "_symmetry_space_group_name_H-M", "My space group");
    structure.cell.spaceGroupNum = get_value(cifBlock, "_symmetry_Int_Tables_number", 0);
    structure.Z = get_value(cifBlock, "_cell_formula_units_Z", 0);
    structure.xray_temperature = get_value(cifBlock, "_diffrn_ambient_temperature", 293.0);
}

// Ну а тут определяем параметры ячейки
inline static void _initCellParameters(cif::CifBlock& cifBlock, Structure& structure)
{
    structure.cell.a = get_value(cifBlock, "_cell_length_a", 0.0);
    structure.cell.b = get_value(cifBlock, "_cell_length_b", 0.0);
    structure.cell.c = get_value(cifBlock, "_cell_length_c", 0.0);
    structure.cell.alpha = get_value(cifBlock, "_cell_angle_alpha", 0.0);
    structure.cell.beta = get_value(cifBlock, "_cell_angle_beta", 0.0);
    structure.cell.gamma = get_value(cifBlock, "_cell_angle_gamma", 0.0);
    structure.cell.volume = get_value(cifBlock, "_cell_volume", 0.0);
}

// Тут внаглую воруем операторы симметрии (суем в affineSymmetryOps)
inline static void _initSymmetryParameters(cif::CifBlock& cifBlock, Structure& structure)
{
    //Тег с операторами симметрии
    const array<string, 2> tags{"_symmetry_equiv_pos_as_xyz", 
                                "_space_group_symop_operation_xyz"};

    for (const auto& tag : tags)
    {   
        cif::CifItemLoop* symmLoop(cifBlock.find_loop(tag));
        if (!symmLoop) continue;
        
        // Надо у этого тега знать индекс потому, что бывает иногда без цифр
        int index = (*symmLoop).get_header_index(tag);

        // Сколько строк - такой и размер, что очевидно
        int sizeSymmLoop = (*symmLoop).rows();

        for (int i = 0; i < sizeSymmLoop; i++)
        {
            structure.cell.affineSymmetryOps.push_back((*symmLoop)(i, index));
        }

        // Если операторы симметрии удалось достать, то можно дальше теги не смотреть
        if (symmLoop != nullptr) return;
    }
}

// Некоторые элементы могут быть со степенями окисления, 
// В данной версии нам бы такого добра не надо!
inline static std::string _extract_element(const std::string& element_from_cif)
{
    // Извлекаем первые два символа, элементов с именем длиннее не бывает
    std::string new_elem = element_from_cif.substr(0, 2);

    // Если второй символ - не буква, значит берем только первый
    if(isalpha(new_elem[1])) return new_elem;
    else return new_elem.substr(0, 1);
}

// А тут тырим жестко атомы... Потом отдельно их будем размножать
inline static bool _initAtoms(cif::CifBlock& cifBlock, Structure& structure, bool noHydrogens)
{
    // Пока берем только позиции и имя с элементом
    // Потом можно легко будет расширить и для Uiso/Uij
    const string tagName = "_atom_site_label";
    const string tagElem = "_atom_site_type_symbol";
    const string tagX = "_atom_site_fract_x";
    const string tagY = "_atom_site_fract_y";
    const string tagZ = "_atom_site_fract_z";
    const string tagSOF = " _atom_site_occupancy";

    // Ищем луп с атомами
    cif::CifItemLoop* atomLoop = cifBlock.find_loop(tagName);
    // Не удалось инициализировать атомы, такое бывает, когда .cif-файл без атомов
    if(atomLoop == nullptr) return false; 

    // Индексы для тегов в атомной таблице
    int indexName = (*atomLoop).get_header_index(tagName);
    int indexElem = (*atomLoop).get_header_index(tagElem);
    int indexX = (*atomLoop).get_header_index(tagX);
    int indexY = (*atomLoop).get_header_index(tagY);
    int indexZ = (*atomLoop).get_header_index(tagZ);
    int indexSOF = (*atomLoop).get_header_index(tagSOF);

    // Сколько строк - такой и размер, что очевидно, столько же атомов
    int sizeAtomLoop = (*atomLoop).rows();

    for (int i = 0; i < sizeAtomLoop; i++)
    {
        const std::string newName = (*atomLoop)(i, indexName);
        const std::string newElem = _extract_element((*atomLoop)(i, indexElem));

        // Если не учитываем водороды, то и нет смысла их считывать, идем дальше по _loop'у
        if (noHydrogens == true && newElem == "H") continue;

        // Пока пусть будут функции Си, надеюсь, это не слишком плохо
        const double newX = strtod(cif::strip_bk((*atomLoop)(i, indexX)).c_str(), nullptr);
        const double newY = strtod(cif::strip_bk((*atomLoop)(i, indexY)).c_str(), nullptr);
        const double newZ = strtod(cif::strip_bk((*atomLoop)(i, indexZ)).c_str(), nullptr);

        double nonConstNewSOF;
        // может быть так, что SOF в CIF-е отсутствует, тогда просто заменяем его на едининицу
        if (indexSOF == -1) nonConstNewSOF = 1.000;
        else nonConstNewSOF = strtod(cif::strip_bk((*atomLoop)(i, indexSOF)).c_str(), nullptr);

        // Создаем новый атом и добавляем его в структуру
        Atom newAtom = Atom(newName, newElem, newX, newY, newZ, nonConstNewSOF);

        newAtom.normalize();
        if(!structure.cell.isAtomExists(newAtom)) structure.cell.atoms.emplace_back(newAtom);
    }

    return true;
}

CifReader::CifReader(const string& path) : cif_main_path{fs::path(path).lexically_normal()} {}

bool CifReader::get_available_cif_paths()
{
    // Сколько удалось вытащить
    int count = 0;

    if(cif_main_path.filename().string() == "*")
    {
        const fs::path dir_path = cif_main_path.parent_path();
        for(const auto& entry : fs::directory_iterator(dir_path))
        {
            if(entry.is_regular_file())
            {
                const fs::path file_path = entry.path();
                if(file_path.extension().string() == ".cif")
                {
                    this->cif_file_paths.emplace_back(file_path);
                    ++count;
                }
            }
        }
    }
    else
    {
        if(cif_main_path.filename().extension().string() == ".cif")
        {
            this->cif_file_paths.emplace_back(cif_main_path);
            ++count;
        }
    }
    
    return (count > 0);
}

int CifReader::count_cif()
{
    return this->cif_file_paths.size();
}

void CifReader::collect_cif_blocks(const string& path)
{
    this->cif_blocks.clear();

    try
    {
        cif::CifFile new_file{path};
        new_file.read_blocks();
        this->cif_blocks.insert(cif_blocks.end(), new_file.begin(), new_file.end());
    }
    catch(...)
    {
        std::cerr << "WARNING: " << path << " is wrong and was skipped" << std::endl;
    }
}

// Если до этой функции дошло, то .cif-файлы точно присутствуют
// Если -> False, то при чтении была ошибка, если true, то все норм
bool CifReader::get_structures_data(const string& cif_path, bool noHydrogens)
{
    this->collect_cif_blocks(cif_path);

    for(int i = 0; i < this->cif_blocks.size(); i++)
    {
        // Новая структура
        Structure newStructure{};
        newStructure.cif_path = cif_path;

        // Инициализируем ее всякими всякостями
        _extract_structure_name(cif_blocks[i], newStructure);
        _initBaseInfoStructure(cif_blocks[i], newStructure);
        _initCellParameters(cif_blocks[i], newStructure);
        _initSymmetryParameters(cif_blocks[i], newStructure);

        // Собираем декартов базис ячейки и считываем атомы
        newStructure.cell.calcCartesianBasis();
        const bool result = _initAtoms(cif_blocks[i], newStructure, noHydrogens);

        // Запихиваем в циф-ридер для дальнейшего использования
        if(result)
        {
            this->current_structures.emplace_back(std::move(newStructure));
        } 
        else
        {
            std::cout << newStructure.name << " from " << cif_path << " was missed: NO ATOMS!" << std::endl;
        }
    }

    // Получилось ли хотя бы одну структуру вытащить?
    return this->current_structures.size() > 0;
}

void CifReader::clear_previous_data()
{
    std::cout << "Before clear - capacity: " << this->current_structures.capacity() 
              << ", size: " << this->current_structures.size() << std::endl;

    this->cif_blocks.clear();
    this->current_structures.clear();

    this->cif_blocks.shrink_to_fit();
    this->current_structures.shrink_to_fit();

    std::cout << "After clear - capacity: " << this->current_structures.capacity() 
              << ", size: " << this->current_structures.size() << std::endl;
}

// static method
bool CifReader::is_cif_path_exist(const string& path)
{
    const fs::path file_path{path};

    if(file_path.filename().string() == "*")
    {
        const fs::path dir_path = file_path.parent_path();

        for(const auto& entry : fs::directory_iterator(dir_path))
        {
            if(entry.is_regular_file())
            {
                if(entry.path().extension().string() == ".cif")
                {
                    return true;
                }
            }
        }
    }
    else
    {
        return fs::is_regular_file(file_path);
    }

    return false;
}