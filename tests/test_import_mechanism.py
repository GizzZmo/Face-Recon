"""
Test that the import mechanism works for both direct and module execution
"""

import os
import subprocess
import sys
import tempfile


def test_direct_script_execution():
    """Test that scripts can be run directly with python src/script.py"""
    # This test simulates the user's execution pattern
    base_dir = os.path.dirname(os.path.dirname(__file__))
    script_path = os.path.join(base_dir, "src", "main_build_database.py")

    # We expect this to fail with missing dependencies (cv2, face_recognition)
    # but NOT with "No module named 'src'" error
    result = subprocess.run(
        [sys.executable, script_path],
        cwd=base_dir,
        capture_output=True,
        text=True,
    )

    # Check that we don't get the 'src' module error
    assert (
        "No module named 'src'" not in result.stderr
    ), "Direct script execution should not fail with 'No module named src'"

    # The error we expect is missing cv2 or face_recognition (if not installed)
    # which is acceptable - we're just testing the import mechanism
    print("✓ Direct execution imports work (may fail on missing dependencies)")


def test_module_execution():
    """Test that scripts can be run as modules with python -m src.script"""
    base_dir = os.path.dirname(os.path.dirname(__file__))

    # Add base dir to PYTHONPATH for module execution
    env = os.environ.copy()
    env["PYTHONPATH"] = base_dir

    result = subprocess.run(
        [sys.executable, "-m", "src.main_build_database"],
        cwd=base_dir,
        capture_output=True,
        text=True,
        env=env,
    )

    # Check that we don't get the 'src' module error
    assert (
        "No module named 'src'" not in result.stderr
    ), "Module execution should not fail with 'No module named src'"

    print("✓ Module execution imports work (may fail on missing dependencies)")


def test_src_package_structure():
    """Test that src is properly set up as a package"""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    src_dir = os.path.join(base_dir, "src")

    # Check that __init__.py exists
    init_file = os.path.join(src_dir, "__init__.py")
    assert os.path.exists(init_file), "src/__init__.py must exist for package imports"

    # Check that essential modules exist
    required_files = [
        "config.py",
        "main_build_database.py",
        "main_realtime_recognition.py",
        "utils/__init__.py",
        "utils/face_utils.py",
        "utils/error_handling.py",
    ]

    for file_path in required_files:
        full_path = os.path.join(src_dir, file_path)
        assert os.path.exists(full_path), f"Required file {file_path} not found in src/"

    print("✓ src package structure is correct")


def test_config_import_without_dependencies():
    """Test that config can be imported without heavy dependencies"""
    # This tests that we can at least import config without needing cv2,
    # face_recognition, etc.
    base_dir = os.path.dirname(os.path.dirname(__file__))

    # Create a temporary Python script to test imports
    test_script = """
import sys
import os
sys.path.insert(0, {base_dir!r})

try:
    from src.config import BASE_DIR, DETECTION_MODEL, FACE_TOLERANCE
    print("SUCCESS: Config imported")
    print(f"BASE_DIR={{BASE_DIR}}")
    print(f"DETECTION_MODEL={{DETECTION_MODEL}}")
    print(f"FACE_TOLERANCE={{FACE_TOLERANCE}}")
except ImportError as e:
    print(f"FAILED: {{e}}")
    sys.exit(1)
""".format(
        base_dir=base_dir
    )

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(test_script)
        temp_script = f.name

    try:
        result = subprocess.run(
            [sys.executable, temp_script],
            capture_output=True,
            text=True,
        )

        assert (
            "SUCCESS: Config imported" in result.stdout
        ), f"Config import failed: {result.stderr}"
        assert "BASE_DIR=" in result.stdout
        assert "DETECTION_MODEL=" in result.stdout
        assert "FACE_TOLERANCE=" in result.stdout

        print("✓ Config module can be imported without heavy dependencies")
    finally:
        os.unlink(temp_script)


def test_import_fallback_mechanism():
    """Test that the import fallback mechanism works correctly"""
    base_dir = os.path.dirname(os.path.dirname(__file__))

    # Test script that simulates the import pattern in our scripts
    test_script = """
import sys
import os

# Simulate running from project root without src in path
# (this is what happens with python src/script.py)
test_passed = False

try:
    # This should fail initially
    from src.config import BASE_DIR
except ImportError:
    # This is the fallback mechanism in our scripts
    sys.path.insert(0, {base_dir!r})
    try:
        from src.config import BASE_DIR
        test_passed = True
        print("SUCCESS: Fallback import mechanism works")
    except ImportError as e:
        print(f"FAILED: Fallback also failed - {{e}}")
        sys.exit(1)

if test_passed:
    print(f"BASE_DIR={{BASE_DIR}}")
else:
    print("FAILED: No import error but test_passed not set")
    sys.exit(1)
""".format(
        base_dir=base_dir
    )

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(test_script)
        temp_script = f.name

    try:
        result = subprocess.run(
            [sys.executable, temp_script],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"Fallback test failed: {result.stderr}"
        assert "SUCCESS: Fallback import mechanism works" in result.stdout

        print("✓ Import fallback mechanism works correctly")
    finally:
        os.unlink(temp_script)


if __name__ == "__main__":
    # Run all tests
    test_src_package_structure()
    test_config_import_without_dependencies()
    test_import_fallback_mechanism()
    test_direct_script_execution()
    test_module_execution()

    print("\n" + "=" * 50)
    print("All import mechanism tests passed!")
    print("=" * 50)
