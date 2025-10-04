# Installation Guide

This guide provides detailed instructions for installing Face-Recon and troubleshooting common installation issues.

## Table of Contents
- [Quick Install](#quick-install)
- [Detailed Installation Steps](#detailed-installation-steps)
- [Troubleshooting](#troubleshooting)
- [Platform-Specific Instructions](#platform-specific-instructions)
- [Alternative Installation Methods](#alternative-installation-methods)

## Quick Install

For most users on Linux/macOS with Python 3.8-3.12:

```bash
# 1. Clone the repository
git clone https://github.com/GizzZmo/Face-Recon.git
cd Face-Recon

# 2. Create a virtual environment
python -m venv venv

# Activate on Linux/macOS:
source venv/bin/activate

# Activate on Windows:
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up data directories
mkdir -p data/known_faces data/unknown_faces

# 5. Run the application
python src/main_build_database.py
```

## Detailed Installation Steps

### Step 1: Prerequisites

**Python Version:**
- Python 3.8 to 3.12 (recommended: 3.10 or 3.11)
- ⚠️ Python 3.13 is NOT recommended due to compatibility issues with dlib

**System Dependencies:**

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install -y python3-dev python3-pip cmake
sudo apt-get install -y libopencv-dev python3-opencv
```

**macOS:**
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install cmake python@3.11
```

**Windows:**
- Install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- Install [CMake](https://cmake.org/download/)
- Add CMake to PATH during installation

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate on Linux/macOS:
source venv/bin/activate

# Activate on Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

**Option A: Standard Installation (Recommended for Linux/macOS)**
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

**Option B: Install with Pre-built Wheels (Windows users)**
```bash
# Install dependencies without dlib first
pip install opencv-python numpy Flask imutils

# Then install dlib from a pre-built wheel
# For Windows Python 3.11 64-bit:
pip install https://github.com/jloh02/dlib/releases/download/v19.24.1/dlib-19.24.1-cp311-cp311-win_amd64.whl

# For other versions, visit: https://github.com/jloh02/dlib/releases

# Finally install face_recognition
pip install face_recognition
```

**Option C: Use Conda (Easiest for Windows)**
```bash
# Install Miniconda: https://docs.conda.io/en/latest/miniconda.html

# Create conda environment from environment.yml
conda env create -f environment.yml
conda activate face-recon

# Or manually:
conda create -n face-recon python=3.11
conda activate face-recon
conda install -c conda-forge dlib opencv numpy flask
pip install face_recognition imutils
```

## Troubleshooting

### Issue 1: "No module named 'src'"

**Problem:** Running `python src/main_build_database.py` fails with `ModuleNotFoundError: No module named 'src'`

**Solution:** This has been fixed in the latest version. Update your code to the latest version. The scripts now support both direct execution and module execution.

**Alternative:** Run as a module instead:
```bash
python -m src.main_build_database
python -m src.main_realtime_recognition
```

### Issue 2: dlib Installation Fails

**Problem:** `pip install face_recognition` fails because dlib won't compile.

**Common Error Messages:**
- "No space left on device" (Windows)
- "error: command 'cmake' failed"
- "Microsoft Visual C++ 14.0 or greater is required"

**Solutions:**

**Solution 1: Use Pre-built dlib Wheels (Windows)**
```bash
# Visit: https://github.com/jloh02/dlib/releases
# Download the appropriate .whl file for your Python version
# For example, Python 3.11 64-bit on Windows:
pip install dlib-19.24.1-cp311-cp311-win_amd64.whl
pip install face_recognition
```

**Solution 2: Use Conda (All Platforms)**
```bash
conda install -c conda-forge dlib
pip install face_recognition
```

**Solution 3: Increase Disk Space (Windows)**
If you see "No space left on device":
- Free up disk space on C: drive (need at least 5GB free)
- Set TEMP environment variable to a drive with more space:
  ```cmd
  set TMP=D:\Temp
  set TEMP=D:\Temp
  pip install dlib
  ```

**Solution 4: Use WSL on Windows**
```bash
# Install Windows Subsystem for Linux (WSL2)
# Then follow Linux installation instructions
```

**Solution 5: Skip dlib and Use Alternatives**
For testing or CI/CD without face recognition:
```bash
# Install minimal dependencies
pip install opencv-python numpy Flask

# Run tests without face recognition features
pytest -m "not integration"
```

### Issue 3: "No module named 'cv2'"

**Problem:** OpenCV is not installed.

**Solution:**
```bash
pip install opencv-python
```

If that fails:
```bash
# Use conda
conda install -c conda-forge opencv

# Or use the headless version (for servers)
pip install opencv-python-headless
```

### Issue 4: Python 3.13 Compatibility Issues

**Problem:** Python 3.13 is too new; many packages don't have pre-built wheels yet.

**Solution:** Use Python 3.11 or 3.10:
```bash
# Install pyenv to manage multiple Python versions
# Then install Python 3.11
pyenv install 3.11.8
pyenv local 3.11.8

# Or download Python 3.11 from python.org
```

### Issue 5: Memory Issues During Installation

**Problem:** Installation runs out of memory.

**Solution:**
```bash
# Increase pip's timeout and use no cache
pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# Or install packages one by one
pip install numpy
pip install opencv-python
pip install dlib
pip install face_recognition
pip install Flask imutils
```

## Platform-Specific Instructions

### Windows 10/11

1. **Install Visual Studio Build Tools:**
   - Download from: https://visualstudio.microsoft.com/downloads/
   - Select "Desktop development with C++"
   - This is required for compiling dlib

2. **Install CMake:**
   - Download from: https://cmake.org/download/
   - During installation, select "Add CMake to system PATH"

3. **Use PowerShell or Command Prompt as Administrator**

4. **Recommended:** Use Conda or pre-built wheels instead of building from source

### Ubuntu/Debian Linux

```bash
# Install all system dependencies
sudo apt-get update
sudo apt-get install -y \
    build-essential \
    cmake \
    python3-dev \
    python3-pip \
    libopencv-dev \
    python3-opencv \
    libboost-all-dev

# Install Python packages
pip install -r requirements.txt
```

### macOS

```bash
# Install Xcode Command Line Tools
xcode-select --install

# Install Homebrew dependencies
brew install cmake boost opencv

# Install Python packages
pip install -r requirements.txt
```

### Raspberry Pi

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y \
    python3-dev \
    python3-pip \
    cmake \
    libatlas-base-dev \
    libjasper-dev \
    libqtgui4 \
    python3-pyqt5 \
    libqt4-test

# Use lightweight requirements
pip install numpy opencv-python-headless

# dlib may take a long time to compile on Pi
# Consider using pre-built wheels or skip face recognition
```

## Alternative Installation Methods

### Docker Installation

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopencv-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "src/main_realtime_recognition.py"]
```

Build and run:
```bash
docker build -t face-recon .
docker run -it --device=/dev/video0 face-recon
```

### Using CI-Friendly Requirements

For CI/CD or minimal installations without face recognition:
```bash
pip install -r requirements-ci.txt
```

This skips the heavy `dlib` and `face_recognition` dependencies.

## Verifying Installation

After installation, verify everything works:

```bash
# Test basic imports
python -c "import cv2; import numpy; print('OpenCV and NumPy: OK')"

# Test face_recognition (if installed)
python -c "import face_recognition; print('face_recognition: OK')"

# Test project imports
python -c "from src.config import BASE_DIR; print(f'Project config: OK (BASE_DIR={BASE_DIR})')"

# Run tests (if pytest is installed)
pytest tests/
```

## Getting Help

If you continue to experience issues:

1. Check [GitHub Issues](https://github.com/GizzZmo/Face-Recon/issues) for similar problems
2. Create a new issue with:
   - Your operating system and version
   - Python version (`python --version`)
   - Full error message
   - Steps to reproduce

## Quick Reference: Common Commands

```bash
# Install from requirements.txt
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements.txt -r requirements-ci.txt

# Run scripts directly
python src/main_build_database.py
python src/main_realtime_recognition.py

# Run as modules
python -m src.main_build_database
python -m src.main_realtime_recognition

# Update dependencies
pip install --upgrade -r requirements.txt

# Check installed packages
pip list

# Verify dlib installation
python -c "import dlib; print(dlib.__version__)"
```
