# Face-Recon Security System

Face-Recon is a multi-component AI security system combining face recognition, voice authentication, IoT integration, blockchain logging, and quantum cryptography. The system includes Python backend services, web frontend, mobile apps (iOS/Android), and IoT controllers.

**ALWAYS reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

## Working Effectively

### Bootstrap, Build, and Test the Repository

**CRITICAL TIMING**: All build and installation commands require extended timeouts. NEVER CANCEL long-running operations.

1. **Environment Setup**:
   ```bash
   cd /home/runner/work/Face-Recon/Face-Recon
   python3 --version  # Verify Python 3.12+
   ```

2. **Install Dependencies** (NEVER CANCEL - takes 7+ minutes):
   ```bash
   pip install -r requirements_clean.txt
   ```
   - **Timeout Required**: 10+ minutes (actual time: ~7 minutes)
   - **Dependencies Include**: OpenCV, face_recognition, Flask, TensorFlow, scikit-learn, MQTT, cryptography
   - **Known Issue**: Original requirements.txt has markdown formatting - use requirements_clean.txt

3. **Setup PYTHONPATH** (CRITICAL for all src/ imports):
   ```bash
   export PYTHONPATH=$PWD
   ```

4. **Create Required Directories**:
   ```bash
   mkdir -p data/known_faces data/unknown_faces logs
   ```

5. **Build Face Database** (1-2 seconds per face):
   ```bash
   PYTHONPATH=/home/runner/work/Face-Recon/Face-Recon python3 src/main_build_database.py
   ```

6. **Test Core Components**:
   ```bash
   # Test library imports (should complete in 1-2 seconds)
   python3 -c "import cv2, face_recognition, flask; print('Core libraries loaded')"
   ```

7. **Lint Code** (0.15 seconds - fast):
   ```bash
   pip install flake8
   flake8 src/ --count --statistics
   ```

8. **Run Tests** (0.33 seconds):
   ```bash
   pip install pytest
   pytest
   ```

## Running the System

### Backend Services

1. **Start Main Flask API** (2-3 seconds startup):
   ```bash
   python3 server.py
   ```
   - Runs on http://127.0.0.1:5000
   - Test endpoint: `curl -X POST http://localhost:5000/access -H "Content-Type: application/json" -d '{"user": "Jon"}'`

2. **Start Enhanced Backend** (requires PYTHONPATH):
   ```bash
   PYTHONPATH=/home/runner/work/Face-Recon/Face-Recon python3 backend/server.py
   ```

3. **Real-time Face Recognition** (camera required):
   ```bash
   PYTHONPATH=/home/runner/work/Face-Recon/Face-Recon python3 src/main_realtime_recognition.py
   ```
   - **Note**: Fails in containerized environments without camera access

### Frontend

1. **Web Dashboard**: Open `frontend/index.html` or `index.html` in browser
2. **Static Files**: CSS in `styles.css`, JavaScript in `app.js`

### IoT and Additional Components

1. **MQTT Client**: `python3 mqtt_client.py`
2. **Voice Authentication**: `python3 voice_authentication.py`
3. **Face Capture**: `python3 face_capture.py` (renamed to avoid import conflicts)

## Validation Scenarios

**ALWAYS test these scenarios after making changes to ensure full functionality:**

### Scenario 1: Complete Backend Validation
1. Install dependencies (allow 10+ minutes)
2. Setup PYTHONPATH
3. Create test face data in `data/known_faces/test_user/`
4. Build face database
5. Start Flask server
6. Test API endpoint with curl
7. Verify JSON response

### Scenario 2: Face Recognition Pipeline
1. Ensure face images exist in `data/known_faces/<person_name>/`
2. Run database builder
3. Check `data/encodings.pickle` is created
4. Test face recognition import without conflicts

### Scenario 3: Development Workflow
1. Make code changes
2. Run flake8 linting (fast)
3. Run pytest (if tests exist)
4. Test affected API endpoints
5. Validate face recognition still works

## Critical Timeouts and Timing

- **Dependency Installation**: 10+ minutes timeout (actual: ~7 minutes)
- **Face Database Building**: 2+ seconds per image
- **Flask Server Startup**: 10 seconds timeout (actual: 2-3 seconds)
- **Linting (flake8)**: 5 seconds timeout (actual: 0.15 seconds)
- **Testing (pytest)**: 10 seconds timeout (actual: 0.33 seconds)

**NEVER CANCEL** operations that appear slow - builds and installations can take significant time.

## Repository Structure

```
Face-Recon/
├── backend/           # Enhanced Flask API and database
├── frontend/          # HTML/CSS/JS web interface
├── src/              # Main Python modules with configuration
├── data/             # Face images and encodings
├── utils/            # Encryption and anomaly detection
├── requirements_clean.txt  # Working Python dependencies
├── *.py              # Individual component scripts
└── .github/          # CI/CD workflows
```

## Known Issues and Workarounds

1. **Import Conflicts**: Files renamed to avoid conflicts:
   - `face_recognition.py` → `face_capture.py`
   - `voice_auth.py` → `voice_authentication.py`

2. **PYTHONPATH Required**: All imports from `src/` require:
   ```bash
   export PYTHONPATH=/home/runner/work/Face-Recon/Face-Recon
   ```

3. **Camera Access**: Real-time recognition fails without camera:
   ```
   [WARN] VIDEOIO(V4L2:/dev/video0): can't open camera by index
   ```
   - Expected in containerized environments
   - Use synthetic test data for validation

4. **Quantum Cryptography**: pqcrypto library incomplete:
   - `pqcrypto.kem.kyber` module not available
   - Use PyCryptodome for standard encryption instead

5. **Requirements File**: Original has markdown formatting:
   - Use `requirements_clean.txt` instead of `requirements.txt`

## Key Libraries and Versions

- **Python**: 3.12.3
- **OpenCV**: 4.12.0
- **Flask**: 3.1.1
- **TensorFlow**: 2.19.0
- **face_recognition**: 1.3.0

## Validation Commands

Always run these before completing work:

```bash
# Quick validation suite (each command takes 1-2 seconds)
python3 -c "import cv2, face_recognition, flask; print('✓ Core imports')"
PYTHONPATH=/home/runner/work/Face-Recon/Face-Recon python3 -c "from src.config import DATABASE_PATH; print('✓ PYTHONPATH config')"
curl -X POST http://localhost:5000/access -H "Content-Type: application/json" -d '{"user": "Jon"}' || echo "Start server first"
flake8 src/ --count || echo "Style issues exist but not critical"
```

## Manual Testing After Changes

**ALWAYS perform these manual validation scenarios after making code changes:**

### Complete Workflow Test (3-5 minutes total)
1. **Clean Environment**: `rm -rf __pycache__ src/__pycache__ data/encodings.pickle`
2. **Build Database**: `PYTHONPATH=/home/runner/work/Face-Recon/Face-Recon python3 src/main_build_database.py` (1-2 seconds)
3. **Start Server**: `python3 server.py` (2-3 seconds startup)
4. **Test API**: `curl -X POST http://localhost:5000/access -H "Content-Type: application/json" -d '{"user": "Jon"}'`
5. **Verify Response**: Should return `{"access": true}`
6. **Stop Server**: Ctrl+C

### Frontend Integration Test
1. **Start Backend**: `python3 server.py`
2. **Open Frontend**: Open `frontend/index.html` in browser
3. **Test UI**: Click "Request Access" button
4. **Verify**: Should show success/failure message

**Expected Total Test Time**: Under 5 minutes for complete validation

## Mobile and IoT Components

- **iOS App**: `ios.app.swift` - NFC functionality
- **Android App**: `android_app.java` - RFID/NFC support  
- **MQTT Client**: `mqtt_client.py` - IoT device communication
- **Raspberry Pi**: `rpi_constroller.py` - Hardware control

Access these components directly - they are standalone scripts for their respective platforms.

Fixes #6.