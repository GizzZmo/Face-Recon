# Troubleshooting Guide

Quick solutions for common errors when setting up and running Face-Recon.

## Table of Contents
- [ModuleNotFoundError: No module named 'src'](#error-modulenotfounderror-no-module-named-src)
- [ModuleNotFoundError: No module named 'cv2'](#error-modulenotfounderror-no-module-named-cv2)
- [dlib Installation Fails](#error-dlib-installation-fails)
- [No space left on device (Windows)](#error-no-space-left-on-device-windows)
- [Other Common Issues](#other-common-issues)

---

## Error: ModuleNotFoundError: No module named 'src'

### Error Message:
```
Traceback (most recent call last):
  File "D:\Downloads\Face-Recon-1.2\Face-Recon-1.2\src\main_build_database.py", line 7, in <module>
    from src.config import KNOWN_FACES_DIR, ENCODINGS_PATH
ModuleNotFoundError: No module named 'src'
```

### ✅ Solution:
This has been **fixed in the latest version**! Update your repository:

```bash
git pull origin main
```

If you're still experiencing this issue, you can:

**Option 1: Run as a module (Recommended)**
```bash
# From the project root directory
python -m src.main_build_database
python -m src.main_realtime_recognition
```

**Option 2: Add PYTHONPATH**
```bash
# Linux/macOS
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python src/main_build_database.py

# Windows (PowerShell)
$env:PYTHONPATH = "$env:PYTHONPATH;$(pwd)"
python src/main_build_database.py

# Windows (CMD)
set PYTHONPATH=%PYTHONPATH%;%cd%
python src\main_build_database.py
```

---

## Error: ModuleNotFoundError: No module named 'cv2'

### Error Message:
```
(venv) D:\Downloads\Face-Recon-1.2\Face-Recon-1.2>python src/main_realtime_recognition.py
Traceback (most recent call last):
  File "D:\Downloads\Face-Recon-1.2\Face-Recon-1.2\src\main_realtime_recognition.py", line 5, in <module>
    import cv2
ModuleNotFoundError: No module named 'cv2'
```

### ✅ Solution:
OpenCV is not installed. Install it with:

```bash
pip install opencv-python
```

If that fails, try:

**Option 1: Use conda**
```bash
conda install -c conda-forge opencv
```

**Option 2: Install headless version (for servers)**
```bash
pip install opencv-python-headless
```

**Option 3: Install from system packages (Linux)**
```bash
# Ubuntu/Debian
sudo apt-get install python3-opencv

# Then in your virtual environment
pip install opencv-python
```

---

## Error: dlib Installation Fails

### Error Message:
```
Building wheel for dlib (pyproject.toml) ... error
ERROR: Failed building wheel for dlib
Failed to build dlib
ERROR: Could not build wheels for dlib, which is required to install pyproject.toml-based projects
```

### Root Cause:
The `face_recognition` library depends on `dlib`, which needs to be compiled from source. This often fails because:
- Missing C++ compiler
- Missing CMake
- Insufficient disk space
- Python version too new (e.g., Python 3.13)

### ✅ Solutions:

#### Solution 1: Use Python 3.10 or 3.11 (Recommended)

Python 3.13 is too new. Downgrade to Python 3.11:

```bash
# Using pyenv (Linux/macOS)
pyenv install 3.11.8
pyenv local 3.11.8

# Or download from python.org and reinstall
```

#### Solution 2: Use Pre-built dlib Wheels (Windows)

```bash
# 1. Download the appropriate wheel from:
# https://github.com/jloh02/dlib/releases

# 2. Install the downloaded wheel
# For Python 3.11 64-bit Windows:
pip install dlib-19.24.1-cp311-cp311-win_amd64.whl

# 3. Then install face_recognition
pip install face_recognition
```

#### Solution 3: Use Conda (All Platforms - Easiest!)

```bash
# Create new conda environment
conda create -n face-recon python=3.11
conda activate face-recon

# Install dlib from conda-forge
conda install -c conda-forge dlib opencv

# Install remaining dependencies
pip install face_recognition Flask imutils
```

#### Solution 4: Install Build Tools (Windows)

If you want to compile from source:

1. Install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
   - Select "Desktop development with C++"
   - Install the package (requires ~6 GB)

2. Install [CMake](https://cmake.org/download/)
   - Add to PATH during installation

3. Restart your terminal and try again:
   ```bash
   pip install dlib
   ```

#### Solution 5: Install Build Tools (Linux)

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y build-essential cmake

# Install dlib
pip install dlib
```

#### Solution 6: Use Docker

If all else fails, use Docker:

```bash
# See INSTALL.md for Docker installation instructions
docker build -t face-recon .
docker run -it face-recon
```

---

## Error: No space left on device (Windows)

### Error Message:
```
C:\Users\jonov\AppData\Local\Temp\pip-install-sr1owdu6\dlib_c433f59f3207469cb703894d4b49b662\build\temp.win-amd64-cpython-313\Release\_dlib_pybind11.dir\Release\image4.obj': No space left on device
```

### Root Cause:
dlib compilation requires 5-10 GB of temporary disk space, typically on the C: drive.

### ✅ Solutions:

#### Solution 1: Free Up Disk Space

1. Clean up C: drive:
   - Delete temporary files
   - Empty Recycle Bin
   - Run Disk Cleanup
   - Uninstall unused programs

2. Ensure at least 10 GB free on C:

#### Solution 2: Change TEMP Directory

```cmd
# In Command Prompt (run as Administrator)
# Change to a drive with more space
set TMP=D:\Temp
set TEMP=D:\Temp

# Create the directory if it doesn't exist
mkdir D:\Temp

# Now try installing
pip install dlib
```

Or make it permanent:
1. Open "Environment Variables" (Windows Settings → System → About → Advanced system settings)
2. Set `TMP` and `TEMP` to a location with more space (e.g., `D:\Temp`)
3. Restart your terminal

#### Solution 3: Use Pre-built Wheels (Recommended)

Avoid compilation entirely by using pre-built wheels:

```bash
# Download from: https://github.com/jloh02/dlib/releases
pip install dlib-19.24.1-cp311-cp311-win_amd64.whl
pip install face_recognition
```

#### Solution 4: Use Conda

Conda packages are pre-compiled:

```bash
conda install -c conda-forge dlib
pip install face_recognition
```

---

## Other Common Issues

### Python 3.13 Compatibility

**Problem:** Many packages don't have pre-built wheels for Python 3.13 yet.

**Solution:** Use Python 3.10 or 3.11:
```bash
# Check your Python version
python --version

# If it's 3.13, install Python 3.11 instead
```

### Webcam Not Accessible

**Error:** `IOError: Webcam not accessible`

**Solutions:**
1. Check if another application is using the webcam
2. Grant camera permissions (Windows Settings → Privacy → Camera)
3. Try a different camera index:
   ```python
   # Edit src/main_realtime_recognition.py
   video_capture = cv2.VideoCapture(1)  # Try 1, 2, etc.
   ```

### Permission Denied

**Error:** `PermissionError: [Errno 13] Permission denied`

**Solutions:**
```bash
# Run without sudo, use virtual environment instead
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### ImportError: DLL load failed (Windows)

**Problem:** Missing Visual C++ Redistributable

**Solution:**
1. Download and install [Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)
2. Restart your computer
3. Try again

---

## Still Need Help?

If you're still experiencing issues:

1. **Check the full installation guide**: [INSTALL.md](INSTALL.md)

2. **Search existing issues**: [GitHub Issues](https://github.com/GizzZmo/Face-Recon/issues)

3. **Create a new issue** with:
   - Your operating system and version
   - Python version: `python --version`
   - Full error message (copy-paste the entire traceback)
   - What you've already tried

4. **Quick diagnostic**:
   ```bash
   # Run this and share the output
   python --version
   pip --version
   pip list
   python -c "import sys; print(f'Platform: {sys.platform}')"
   ```

---

## Quick Commands Reference

```bash
# Check versions
python --version
pip --version

# Update pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Install individual packages
pip install opencv-python numpy Flask

# Check installed packages
pip list

# Test imports
python -c "import cv2; print('OpenCV OK')"
python -c "import face_recognition; print('face_recognition OK')"
python -c "from src.config import BASE_DIR; print('Project OK')"

# Run the application
python src/main_build_database.py
python src/main_realtime_recognition.py

# Or as modules
python -m src.main_build_database
python -m src.main_realtime_recognition
```
