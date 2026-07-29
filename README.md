# 💎 APEXSYMM


# ⚙️ Installation

Go to the [releases](https://github.com/drxvmrz/apexsymm/releases) and download the latest version of installer. 
Then install it as usual on your operating system.

# 🩺 Test Apexsymm by example crystal

1. Download test operators to calculation [OLF-file](https://github.com/drxvmrz/apexsymm/blob/main/_test_examples/monoclinic_operators.olf) and test monoclinic crystal structure [CIF-file](https://github.com/drxvmrz/apexsymm/blob/main/_test_examples/test_structure.cif);

2. Open 'Apexsymm' is installed on your commuter;

3. Drag and drop downloaded operators and crystal structure files into 'Apexsymm' main window;

4. Run the calculation :)

# 🧑‍💻 Build by yourself

To build a standalone GUI-application follow these steps:

1. Download or clone this repository;

2. Open downloaded repository via `Terminal` on Linux and MacOS and via 
`Command Prompt` or `PowerShell` on Windows:

```
cd <PATH TO DOWNLOADED REPOSITRORY>
```

4. Build the kernel:

5. Built the GUI shell:

    5.1. Create an Python virtual environment on it then activate:

        5.1.1 Windows (PowerShell or Command Prompt)

            python -m venv .venv ^
            .\.venv\bin\activate.bat

        5.1.2 MacOS (Terminal)

            python -m venv venv \ 
            source venv/bin/activate

    5.2. Install needed packages if missed:
        
        ```
        pip install PySide6 nuitka platformdirs imageio
        ```

    5.3. Add the kernel file to [core folder](https://gitverse.ru/drxvmrz/apexsymm_gui/content/master/core)
        
        You can download the kernel file from [kernel](https://gitverse.ru/drxvmrz/apexsymm_core). 
        It can be obtained as ready execution file from releases or you can build it by yourself.

    5.4. Run the ```Nuitka``` building:
        
        5.4.1 Windows (PowerShell or Command Prompt):
            
            .\build_nuitka_win32.bat
            
        5.4.2 MacOS (Terminal):
            
            chmod +x build_nuitka_mac.sh \
            ./build_nuitka_mac

6. Run the app :)
