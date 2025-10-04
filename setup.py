"""
cx_Freeze setup script for Dreamrooms.

This script builds standalone executables for the game.

Usage:
    python setup.py build

The executable will be created in the build/ directory.
"""

from cx_Freeze import setup, Executable
import sys

# Dependencies to include
build_exe_options = {
    # Packages to explicitly include
    "packages": [
        "pygame",
        "OpenGL",
        "OpenGL.GL",
        "OpenGL.GLU",
        "numpy",
        "os",
        "random"
    ],

    # Files and folders to include with the executable
    "include_files": [
        "assets/",  # Include all game assets (audio, textures)
    ],

    # Modules to exclude (reduce file size)
    "excludes": [
        "tkinter",  # Not used in the game
        "unittest",
        "email",
        "http",
        "xml",
        "pydoc",
    ],

    # Additional optimization
    "optimize": 2,
}

# Determine base for Windows (use "Win32GUI" to hide console window)
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Hides console window on Windows

# Executable configuration
executables = [
    Executable(
        "main.py",
        base=base,
        target_name="Dreamrooms",  # Name of the executable
        icon=None,  # Add "icon.ico" here if you create one
    )
]

# Setup configuration
setup(
    name="Dreamrooms",
    version="1.0",
    description="A liminal horror maze game inspired by backrooms, dreamcore, and David Lynch",
    author="Leonardo Zordan Lima, Luiz Marcelo Itapicuru Pereira Costa, Matheus Soares Martins, Thiago Crivaro Nunes",
    options={"build_exe": build_exe_options},
    executables=executables,
)
