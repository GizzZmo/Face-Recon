#!/usr/bin/env python3
"""
Simple test to verify that the environment setup works correctly
and essential dependencies can be imported.
"""

def test_opencv_import():
    """Test that opencv-python can be imported."""
    try:
        import cv2
        assert cv2.__version__ is not None
        print(f"✓ OpenCV version: {cv2.__version__}")
    except ImportError as e:
        assert False, f"Failed to import opencv-python: {e}"

def test_numpy_import():
    """Test that numpy can be imported."""
    try:
        import numpy as np
        assert np.__version__ is not None
        print(f"✓ NumPy version: {np.__version__}")
    except ImportError as e:
        assert False, f"Failed to import numpy: {e}"

def test_flask_import():
    """Test that Flask can be imported."""
    try:
        import flask
        assert flask.__version__ is not None
        print(f"✓ Flask version: {flask.__version__}")
    except ImportError as e:
        assert False, f"Failed to import Flask: {e}"

def test_face_recognition_import():
    """Test that face_recognition can be imported."""
    try:
        import face_recognition
        # face_recognition doesn't have a __version__ attribute, so just test import
        print("✓ face_recognition imported successfully")
    except ImportError as e:
        assert False, f"Failed to import face_recognition: {e}"

def test_imutils_import():
    """Test that imutils can be imported."""
    try:
        import imutils
        print("✓ imutils imported successfully")
    except ImportError as e:
        assert False, f"Failed to import imutils: {e}"

if __name__ == "__main__":
    print("Running basic dependency tests...")
    test_numpy_import()
    test_opencv_import()
    test_flask_import() 
    test_face_recognition_import()
    test_imutils_import()
    print("All dependency tests passed! ✓")