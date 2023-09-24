# Algorithms - Data Structures & Algorithms in Python (Goodrich, Tamassia, Goldwasser)

## For Windows Installations
`graphs.py` requires the following modules to work:
* [networkx](https://networkx.org/documentation/stable/install.html)
* [graphviz 2.46+](https://gitlab.com/graphviz/graphviz/-/package_files/6164164/download)
* [pygraphviz 1.7](https://pygraphviz.github.io/)  
Dependencies: 
    - Python >= 3.8+
    - [Graphviz >= 2.46+](https://gitlab.com/graphviz/graphviz/-/package_files/6164164/download)
    - [C/C++ Compiler](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

## Manual Installation  
1. Install Graphviz.
2. Modify `INSTALL_FOLDER` to where you installed Graphviz.
3. Run the following in cmd or PowerShell.
```cmd
set INSTALL_FOLDER="C:\Graphviz\"
python -m pip install --global-option=build_ext --global-option="-I%INSTALL_FOLDER%include" --global-option="-L%INSTALL_FOLDER%lib" pygraphviz==1.7
```

## How to run
1. Change directory to `algorithms/`
2. Run each solution separately using your debugger and IDE of choice. Solutions typically are outputted to the console.