# Building Dreamrooms Executable

This document explains how to build standalone executables for Dreamrooms.

## Prerequisites

1. **Install cx_Freeze:**
```bash
pip install cx_Freeze
```

2. **Ensure all dependencies are installed:**
```bash
pip install -r requirements.txt
```

## Building the Executable

### For Windows

1. Open a terminal/command prompt on a **Windows machine**
2. Navigate to the project directory
3. Run the build command:
```bash
python setup.py build
```

The executable will be created in `build/exe.win-amd64-3.x/` (where 3.x is your Python version)

### For Linux

1. Open a terminal on a **Linux machine**
2. Navigate to the project directory
3. Run the build command:
```bash
python setup.py build
```

The executable will be created in `build/exe.linux-x86_64-3.x/` (where 3.x is your Python version)

## Important Notes

### Platform-Specific Builds
- **You MUST build on the target platform**
- Windows executables can only be built on Windows
- Linux executables can only be built on Linux
- There is no cross-compilation support

### What Gets Included
The build process automatically includes:
- Python interpreter
- All required libraries (PyOpenGL, pygame, numpy)
- The `assets/` folder (textures, audio)
- All game modules (player, place, maze, light, etc.)

### File Size
The executable will be approximately 50-150MB because it includes:
- Python runtime
- OpenGL libraries
- Pygame libraries
- NumPy libraries
- All game assets

## Distribution

### Windows Distribution
1. Navigate to `build/exe.win-amd64-3.x/`
2. The entire folder is needed (not just the .exe)
3. Zip the entire folder for distribution
4. Users extract and run `Dreamrooms.exe`

### Linux Distribution
1. Navigate to `build/exe.linux-x86_64-3.x/`
2. The entire folder is needed (not just the executable)
3. Create a tarball: `tar -czf Dreamrooms-Linux.tar.gz build/exe.linux-x86_64-3.x/`
4. Users extract and run `./Dreamrooms`

## Troubleshooting

### Missing Assets
If the game runs but has no textures or sound:
- Check that the `assets/` folder is in the same directory as the executable
- Verify `setup.py` has `"include_files": ["assets/"]`

### Import Errors
If you get module not found errors:
- Add the missing module to the `packages` list in `setup.py`
- Rebuild with `python setup.py build`

### OpenGL Errors
If you get OpenGL-related errors:
- Ensure graphics drivers are up to date
- Some systems may need to install OpenGL separately

### "Cannot execute binary file"
On Linux, ensure the executable has execute permissions:
```bash
chmod +x Dreamrooms
```

## Creating a Distributable Package

### Windows
```bash
cd build/exe.win-amd64-3.x/
# Zip the entire directory
```

### Linux
```bash
cd build
tar -czf Dreamrooms-Linux.tar.gz exe.linux-x86_64-3.x/
```

## Alternative: Python Distribution

If building executables is problematic, you can distribute the source code:

1. Include `requirements.txt`
2. Provide installation instructions (see MANUAL.md)
3. Users run `python main.py` after installing dependencies

This is smaller and more reliable across different systems.

## Adding an Icon (Optional)

### Windows
1. Create or obtain an `.ico` file
2. Place it in the project root as `icon.ico`
3. Update `setup.py`:
   ```python
   icon="icon.ico"
   ```
4. Rebuild

### Linux
Icons are handled differently - typically through desktop entry files.

---

For questions or issues, refer to:
- [cx_Freeze Documentation](https://cx-freeze.readthedocs.io/)
- MANUAL.md for game instructions
- CODE_DOCUMENTATION.md for technical details
