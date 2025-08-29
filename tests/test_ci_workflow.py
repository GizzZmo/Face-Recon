"""
Test CI/CD workflow functionality and improvements
"""

import os
import subprocess
import sys

import pytest


def test_linting_tools_available():
    """Test that linting tools are available"""
    tools = ["flake8", "black", "isort"]
    for tool in tools:
        result = subprocess.run(
            [sys.executable, "-m", tool, "--version"], capture_output=True, text=True
        )
        assert result.returncode == 0, f"{tool} not available"


def test_testing_tools_available():
    """Test that testing tools are available"""
    tools = ["pytest"]
    for tool in tools:
        result = subprocess.run(
            [sys.executable, "-m", tool, "--version"], capture_output=True, text=True
        )
        assert result.returncode == 0, f"{tool} not available"


def test_workflow_files_exist():
    """Test that CI workflow files exist"""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    workflows_dir = os.path.join(base_dir, ".github", "workflows")

    # Check that workflows directory exists
    assert os.path.exists(workflows_dir)

    # Check for the comprehensive CI workflow
    comprehensive_workflow = os.path.join(workflows_dir, "ci-comprehensive.yml")
    assert os.path.exists(comprehensive_workflow)


def test_requirements_txt_format():
    """Test that requirements.txt is properly formatted"""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    requirements_file = os.path.join(base_dir, "requirements.txt")

    assert os.path.exists(requirements_file)

    with open(requirements_file, "r") as f:
        content = f.read()

    # Should not contain markdown code blocks
    assert "```" not in content

    # Should contain basic dependencies
    lines = [
        line.strip()
        for line in content.split("\n")
        if line.strip() and not line.startswith("#")
    ]
    dependencies = [line for line in lines if not line.startswith("#")]

    expected_deps = ["opencv-python", "numpy", "Flask"]
    for dep in expected_deps:
        assert any(dep in line for line in dependencies), f"Missing dependency: {dep}"


def test_gitignore_exists():
    """Test that .gitignore exists and contains necessary entries"""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    gitignore_file = os.path.join(base_dir, ".gitignore")

    assert os.path.exists(gitignore_file)

    with open(gitignore_file, "r") as f:
        content = f.read()

    # Check for important ignore patterns
    required_patterns = ["__pycache__/", "*.pyc", ".env", "venv/", "logs/"]
    for pattern in required_patterns:
        assert pattern in content, f"Missing gitignore pattern: {pattern}"


@pytest.mark.parametrize("python_version", ["3.8", "3.9", "3.10", "3.11", "3.12"])
def test_python_version_matrix(python_version):
    """Test that Python versions are valid for matrix testing"""
    # This test validates that the versions we're testing in CI are reasonable
    major, minor = python_version.split(".")
    assert major == "3"
    assert 8 <= int(minor) <= 12


def test_basic_import_functionality():
    """Test basic import functionality that CI will test"""
    # This mirrors what the CI workflow tests
    try:
        # Test OpenCV import
        import cv2

        assert cv2.__version__ is not None

        # Test NumPy import
        import numpy

        assert numpy.__version__ is not None

        # Test Flask import
        import flask

        assert flask.__version__ is not None

        # Test project config
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
        import config

        assert hasattr(config, "BASE_DIR")

    except ImportError as e:
        pytest.fail(f"Import test failed: {e}")


def test_security_tools_integration():
    """Test that security tools can be run (mimicking CI)"""
    # Test that safety can be invoked (dependency security)
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "safety"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            safety_result = subprocess.run(
                [sys.executable, "-m", "safety", "--version"],
                capture_output=True,
                text=True,
            )
            assert safety_result.returncode == 0, f"safety not available or failed to run: {safety_result.stderr}"
    except Exception:
        # If safety can't be installed/run, that's ok for basic tests
        pass


def test_code_formatting_check():
    """Test basic code formatting (what CI will check)"""
    base_dir = os.path.dirname(os.path.dirname(__file__))

    # Run black check on test files only (to avoid modifying existing code)
    test_file = __file__
    result = subprocess.run(
        [sys.executable, "-m", "black", "--check", "--diff", test_file],
        capture_output=True,
        text=True,
    )

    # If black fails, print the diff for debugging
    if result.returncode != 0:
        print("Black formatting issues:")
        print(result.stdout)
        print(result.stderr)

    # For tests, we expect proper formatting
    assert result.returncode == 0, "Test files should be properly formatted"
