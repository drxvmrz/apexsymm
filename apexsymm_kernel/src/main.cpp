#include <chrono>

#include "pss2_static_consts.hpp"
#include "pss2_CLI_interface.hpp"
#include "pss2_cif_reader.hpp"

#include "pss2_io.hpp"

int main(int argc, char const *argv[])
{
    // Приветственное сообщение
    std::cout << HelloMsg::HELLO_MESSAGE << std::endl;

    // Запускаем таймер работы программы
    auto start = std::chrono::high_resolution_clock::now();
    auto end = std::chrono::high_resolution_clock::now();

    CLIParser cmd{};
    auto status = cmd.readSettings(argc, argv);
    if(status == SCMDP_BAD || status == SCMDP_HELP) return PssBasicIO::send_error_msg(100);
    if (!cmd.isSettingsValid()) return PssBasicIO::send_error_msg(100);
    if(!CifReader::is_cif_path_exist(cmd.cifFilePath)) return PssBasicIO::send_error_msg(101);

    // Создаем считыватель и считываем структуры из .cif-файлов
    CifReader reader{cmd.cifFilePath};
    reader.get_available_cif_paths();
    if(reader.count_cif() == 0) return PssBasicIO::send_error_msg(104);

    // Выводим введенные операторы в виде матриц и трансляций
    std::cout << "RUN!\n" << std::endl;
    for (const auto& op : cmd.operators)
    {
        std::cout << "IN_MATRIX: ";
        std::cout << op.matrix(0, 0) << " " << op.matrix(0, 1) << " " << op.matrix(0, 2) << " | ";
        std::cout << op.matrix(1, 0) << " " << op.matrix(1, 1) << " " << op.matrix(1, 2) << " | ";
        std::cout << op.matrix(2, 0) << " " << op.matrix(2, 1) << " " << op.matrix(2, 2) << std::endl;
        std::cout << "IN_TRANSL_AFFN: " << op.vector_affine(0) << " " << op.vector_affine(1) << " " << op.vector_affine(2) << "\n" << std::endl;
    }
    
    // Прогресс выполнения в процентах, он выводится в std::cout
    // Считается как 100/7, т.к. 7 основных операций и на число стурктур для расчета
    double progress_in_percents = 0.0;
    const double progress_step = 100.0/7.0/reader.count_cif();

    // Создаем записыватель в json
    PssJSONwriter writer{};
    if(cmd.saveJSONFile != "") writer.apply_path(cmd.saveJSONFile);

    // Обрабатываем все .cif файлы и структуры в них
    for(auto& cif_path : reader.cif_file_paths)
    {
        // Очистка памяти от предыдущей стурктуры
        // Некоторые структуры могут занимать много оперативки, копить ее ни к чему
        reader.clear_previous_data();
        if(!reader.get_structures_data(cif_path.string(), cmd.noHydrogens)) continue;

        // Шаг по прогрессу во столько раз меньше, сколько структур было получено из cif
        const double local_progress_step = progress_step/reader.current_structures.size();

        for(auto& str : reader.current_structures)
        {
            std::cout << "''" << str.name << "'': " << "Processing begins" << std::endl; 

            size_t atomsMultiplied = str.cell.multiplyAtoms();
            std::cout << "''" << str.name << "'': " << "Multiplied and added " << atomsMultiplied << " atoms" << std::endl;
            str.showStructureInfo();
            progress_in_percents += local_progress_step;
            std::cout << "PROGRESS: " << progress_in_percents << " %" << std::endl;

            if(cmd.superCell > 0)
            {
                str.extend(cmd.superCell);
                std::cout << "''" << str.name << "'': " << "Cell extended to supercell with " << cmd.superCell << " cell radius" << std::endl; 
            }
            progress_in_percents += local_progress_step;
            std::cout << "PROGRESS: " << progress_in_percents << " %" << std::endl;

            str.prepareStructure(cmd.operators, cmd.resolution, cmd.noHydrogens);
            std::cout << "''" << str.name << "'': " << "Structure has been prepared for calculations " << std::endl; 
            progress_in_percents += local_progress_step;
            std::cout << "PROGRESS: " << progress_in_percents << " %" << std::endl;

            std::cout << "''" << str.name << "'': " << "Preparing calculation maps now... " << std::endl; 
            str.prepareStructureMaps(cmd.resolution, cmd.maxThreads);
            progress_in_percents += local_progress_step;
            std::cout << "''" << str.name << "'': " << "Maps for calculation has been prepared" << std::endl;
            std::cout << "PROGRESS: " << progress_in_percents << " %" << std::endl;
            
            /*** Извлекаем операторы, если режим поиска трансляций и уточнения  ***/
            if (cmd.needToRefine)
            {
                std::cout << "''" << str.name << "'': " << "Operator refinement started for "<< str.name << std::endl;
                str.createMapsEta();
                str.extractOperators(cmd.threshold);
                str.refineAllPseudoOperators(cmd.resolution, cmd.precision, cmd.maxCycles);
                std::cout << "''" << str.name << "'': " << "Refinement has been done" << std::endl;
            }
            progress_in_percents += local_progress_step;
            std::cout << "PROGRESS: " << progress_in_percents << " %" << std::endl;

            /* Пересчитываем для всех 'эту', сортируем и выводим инфу в консоль*/
            std::cout << "''" << str.name << "'': " << "Recalculating Eta for refined translations..." << std::endl; 
            str.recalcEtaForAll(cmd.resolution);
            progress_in_percents += local_progress_step;
            std::cout << "PROGRESS:" << progress_in_percents << " %" << std::endl;

            str.sortOperatorsByEta(true);
            str.removeDuplicatePsOps(cmd.precision);
            str.calc_basis_angles();
            str.representOpsInAffine();
            str.showPseudoOpsInfo(cmd.maxOutput);

            if(cmd.saveJSONFile != "")
            {
                end = std::chrono::high_resolution_clock::now();
                const auto duration = std::chrono::duration_cast<std::chrono::seconds>(end - start);

                if(!writer.is_created()) writer.create_file(cmd);
                writer.add_results(reader, duration.count());

                std::cout << "JSON with results has been added in " << cmd.saveJSONFile << std::endl;
            }
        }
    }

    end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::seconds>(end - start);

    progress_in_percents = 100;
    std::cout << "PROGRESS: " << progress_in_percents << " %"  << std::endl;
    std::cout << "Ready! All is done! Please look at results :)" << std::endl;
    std::cout << "Calculation time is " << duration.count() << " seconds!" << std::endl;

    return 0;
}