#!/bin/bash
python3 -m nuitka \
--standalone \
-onedir \
--enable-plugin=pyside6 \
--macos-create-app-bundle \
--include-package=PySide6.QtCore \
--include-package=PySide6.QtWidgets \
--include-package=PySide6.QtGui \
--include-data-file="./build/apexcore_mac"="./core/apexcore_mac" \
--include-data-file="./apexsymm_gui/extras/manual_en.pdf"="./extras/manual_en.pdf" \
--include-data-file="./apexsymm_gui/extras/manual_ru.pdf"="./extras/manual_ru.pdf" \
--include-data-file="./apexsymm_gui/presets"="./presets" \
--include-data-file="./apexsymm_gui/icon.ico"="./icon.ico" \
--output-dir="./dist" \
--macos-app-icon="./apexsymm_gui/icon.png" \
--macos-app-name="Apexsymm" \
--output-file="Apexsymm.app" \
./apexsymm_gui/main.py
echo "Done! Press ENTER to continue..."
read
