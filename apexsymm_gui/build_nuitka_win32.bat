python -m nuitka ^
--mode=standalone ^
--enable-plugin=pyside6 ^
--include-package=PySide6.QtCore ^
--include-package=PySide6.QtWidgets ^
--include-package=PySide6.QtGui ^
--include-qt-plugins=platforms,styles,imageformats ^
--include-data-file=./build/apexcore_win.exe=./core/apexcore_win.exe ^
--include-data-file=./apexsymm_gui/extras/manual_en.pdf=./extras/manual_en.pdf ^
--include-data-file=./apexsymm_gui/extras/manual_ru.pdf=./extras/manual_ru.pdf ^
--include-data-file=./apexsymm_gui/icon.png=./icon.png ^
--include-data-file=./apexsymm_gui/icon.ico=./icon.ico ^
--include-data-file=./apexsymm_gui/presets=./presets ^
REM --include-data-files=./core/*.dll=./core/ ^ need to add fftw3.dll or apexcore_win will not work :c
--output-dir=dist ^
--msvc=latest ^
--windows-icon-from-ico=./apexsymm_gui/icon.png ^
--windows-disable-console ^
--output-filename=apexsymm.exe ^
main.py

pause