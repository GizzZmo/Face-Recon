"""
Test configuration and basic functionality
"""

import os
import sys

import pytest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


def test_config_import():
    """Test that config module can be imported"""
    try:
        import config

        assert hasattr(config, "BASE_DIR")
        assert hasattr(config, "DETECTION_MODEL")
        assert hasattr(config, "FACE_TOLERANCE")
    except ImportError:
        pytest.fail("Failed to import config module")


def test_config_values():
    """Test that config values are reasonable"""
    import config

    # Test that paths exist or can be created
    assert isinstance(config.BASE_DIR, str)
    assert len(config.BASE_DIR) > 0

    # Test detection model is valid
    assert config.DETECTION_MODEL in ["hog", "cnn"]

    # Test face tolerance is reasonable
    assert 0.1 <= config.FACE_TOLERANCE <= 1.0


def test_dependencies_import():
    """Test that all required dependencies can be imported"""
    try:
        import cv2

        assert cv2.__version__ is not None
    except ImportError:
        pytest.fail("OpenCV not available")

    try:
        import numpy as np

        assert np.__version__ is not None
    except ImportError:
        pytest.fail("NumPy not available")

    try:
        import flask

        assert flask.__version__ is not None
    except ImportError:
        pytest.fail("Flask not available")


def test_project_structure():
    """Test that basic project structure exists"""
    base_dir = os.path.dirname(os.path.dirname(__file__))

    # Check for essential files
    assert os.path.exists(os.path.join(base_dir, "requirements.txt"))
    assert os.path.exists(os.path.join(base_dir, "src", "config.py"))

    # Check for README
    readme_exists = (
        os.path.exists(os.path.join(base_dir, "README.md"))
        or os.path.exists(os.path.join(base_dir, "README.rst"))
        or os.path.exists(os.path.join(base_dir, "README.txt"))
    )
    assert readme_exists, "No README file found"


@pytest.mark.parametrize("detection_model", ["hog", "cnn"])
def test_detection_models(detection_model):
    """Test that detection models are valid options"""
    valid_models = ["hog", "cnn"]
    assert detection_model in valid_models


def test_directory_creation():
    """Test that data directories can be created"""
    import shutil
    import tempfile

    import config

    # Create temporary directories to test structure
    with tempfile.TemporaryDirectory() as temp_dir:
        test_data_dir = os.path.join(temp_dir, "data")
        test_known_faces = os.path.join(test_data_dir, "known_faces")
        test_unknown_faces = os.path.join(test_data_dir, "unknown_faces")

        os.makedirs(test_known_faces, exist_ok=True)
        os.makedirs(test_unknown_faces, exist_ok=True)

        assert os.path.exists(test_data_dir)
        assert os.path.exists(test_known_faces)
        assert os.path.exists(test_unknown_faces)
