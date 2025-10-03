# Quick Fix Guide

**Encountered installation errors?** This guide will get you running in minutes.

## 🚀 Fast Track to Success

### Step 1: Update to Latest Version

```bash
# Pull the latest fixes
git pull origin main
```

The import errors have been **fixed**! Scripts now work with direct execution.

### Step 2: Use the Right Python Version

```bash
# Check your Python version
python --version
```

- ✅ **Python 3.8 - 3.12**: Perfect!
- ❌ **Python 3.13**: Too new, use 3.11 instead

**If you have Python 3.13:**
```bash
# Install Python 3.11 from python.org
# or use pyenv:
pyenv install 3.11.8
pyenv local 3.11.8
```

### Step 3: Choose Your Installation Method

#### Option A: Use Conda (Easiest for Windows!)

```bash
# Install Miniconda from: https://docs.conda.io/en/latest/miniconda.html

# Create environment
conda create -n face-recon python=3.11
conda activate face-recon

# Install dependencies
conda install -c conda-forge dlib opencv numpy flask
pip install face_recognition imutils

# Done! Skip to Step 4
```

#### Option B: Use Pre-built Wheels (Windows)

```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 2. Install basic dependencies
pip install opencv-python numpy Flask imutils

# 3. Download dlib wheel from:
# https://github.com/jloh02/dlib/releases
# For Python 3.11 64-bit Windows, download:
# dlib-19.24.1-cp311-cp311-win_amd64.whl

# 4. Install downloaded wheel
pip install dlib-19.24.1-cp311-cp311-win_amd64.whl

# 5. Install face_recognition
pip install face_recognition

# Done! Skip to Step 4
```

#### Option C: Standard Installation (Linux/macOS)

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS

# 2. Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y build-essential cmake python3-dev

# 3. Install Python packages
pip install -r requirements.txt

# Done! Continue to Step 4
```

### Step 4: Set Up Data Directories

```bash
# Create directories for face data
mkdir -p data/known_faces
mkdir -p data/unknown_faces

# Add photos
mkdir -p data/known_faces/person_name
# Copy some photos of the person to: data/known_faces/person_name/
```

### Step 5: Run the Application

```bash
# Build the face database
python src/main_build_database.py

# Start real-time recognition
python src/main_realtime_recognition.py
```

## ❓ Still Getting Errors?

### "ModuleNotFoundError: No module named 'src'"

**Already fixed!** Just make sure you've pulled the latest code.

If still seeing it:
```bash
# Run as module instead
python -m src.main_build_database
python -m src.main_realtime_recognition
```

### "ModuleNotFoundError: No module named 'cv2'"

```bash
pip install opencv-python
```

### "No space left on device" (Windows)

1. Free up space on C: drive (need ~10 GB)
2. Or use pre-built wheels (Option B above) - no compilation needed!

### "dlib installation failed"

Don't compile it! Use one of these:
- **Easiest**: Use Conda (Option A)
- **Windows**: Use pre-built wheels (Option B)  
- **Still stuck**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## 📚 Need More Help?

- **Quick fixes**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Detailed guide**: [INSTALL.md](INSTALL.md)
- **Report issues**: [GitHub Issues](https://github.com/GizzZmo/Face-Recon/issues)

## ✅ Verification

Test that everything works:

```bash
# Test imports
python -c "import cv2; print('✓ OpenCV OK')"
python -c "import face_recognition; print('✓ face_recognition OK')"
python -c "from src.config import BASE_DIR; print('✓ Project config OK')"

# If all print OK, you're ready to go!
```

## 🎯 Summary

1. ✅ Update to latest code (import fixes)
2. ✅ Use Python 3.11 (not 3.13)
3. ✅ Install with Conda OR pre-built wheels (easiest)
4. ✅ Create data directories
5. ✅ Run the application

**Most common mistake**: Using Python 3.13 → Use 3.11 instead!

---

*Having trouble? Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for your specific error message.*
