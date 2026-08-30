# 💎 APEXSYMM
A cross-platform user-friendly GUI-application for studying the pseudosymmetry of crystal structures using the Chuprunov method for calculating the degree of invariance of the electron density.

If you found this application useful in your research, [please cite](https://www.doi.org/):
> Article in process now

Original method [article](https://doi.org/10.1134/S1063774507010014):
> _Chuprunov E.V._ Fedorov Pseudosymmetry of Crystals: Review // Crystallography Reports. 2007. V. 52. No. 1. P. 1-11

# ⚖️ Features

- [x] A completely standalone desktop-app
- [x] User-friendly and fast graphical user interface
- [x] Rotation matrices of symmetry operators represents in cartesian basis 

# 🧑‍🔬 System Requirements

> OS: Windows 10 or later, MacOS 11 (Big Sur) or later, Linux distribution with Qt6 support
> 
> CPU: 2 GHz Multicored x64/arm64 or better
> 
> RAM: 8 Gb or more
> 
> HDD/SSD: 100 Mb or more

# ⚙️ Installation

Go to the [releases](https://github.com/drxvmrz/apexsymm/releases) and download the latest version of installer. 
Then install it as usual on your operating system.

# 🩺 Test APEXSYMM by example crystal

1. Download test operators to calculation [OLF-file](https://github.com/drxvmrz/apexsymm/blob/main/_test_examples/monoclinic_operators.olf) and test monoclinic crystal structure [CIF-file](https://github.com/drxvmrz/apexsymm/blob/main/_test_examples/test_structure.cif);
   
2. Open APEXSYMM installed on your commuter;
   
3. Drag and drop downloaded operators and crystal structure files into APEXSYMM main window;
   
4. Run the calculation!

# 📚 More information about using APEXSYMM

For more information, please refer to the complete [user manual](https://github.com/drxvmrz/apexsymm/tree/main/apexsymm_gui/extras).

# 🧑‍💻 Build APEXSYMM by yourself

❗*To build the APEXSYMM, `CMake` and `Python` must be installed and added into `PATH` system variable!*

✅To build a standalone GUI-application follow these steps:

1. Download or clone this repository;
   
2. Open downloaded repository via `Terminal` on Linux and MacOS and via `Command Prompt` or `PowerShell` on Windows:
   
```
cd <PATH TO DOWNLOADED REPOSITRORY>
```

3. Build the kernel:
   
    1. Prepare your libraries pathways in [CMakeLists.txt](https://github.com/drxvmrz/apexsymm/blob/main/apexsymm_kernel/src/CMakeLists.txt)
       
    2. Run `CMake` building:
   
         *Use `\` instead of `^` on UNIX/UNIX-like systems*
      
         ```
         cmake -S .\apexsymm_kernel\src\ -B build ^
         cmake --build build --config Release
         ```
         
5. Build the GUI shell:
   
    1. Create a `Python virtual environment` on it then activate:
       
        1. Windows (PowerShell or Command Prompt)
           
            ```
            python -m venv .venv ^
            .\.venv\bin\activate.bat
            ```
       
        2. UNIX/UNIX-like (Terminal)
           
            ```
            python -m venv venv \ 
            source venv/bin/activate
            ```
   
    2. Install needed `python packages` if missed:
       
        ```
        pip install PySide6 nuitka platformdirs imageio
        ```
   
    3. Run the `Nuitka` building:
       
        1. Windows (PowerShell or Command Prompt)
           
            ```
            .\build_nuitka_win32.bat
            ```
       
        2. UNIX/UNIX-like (Terminal):
           
            ```
            chmod +x build_nuitka_mac.sh \
            ./build_nuitka_mac
            ```
        
6. Open `dist` folder then run the app :)
