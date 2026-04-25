"""
Unit tests for the liveness detection utilities.

These tests do not require a camera or face-recognition library; they
exercise the pure-Python/NumPy/OpenCV helper functions directly.
"""

import numpy as np
import pytest

# Skip the whole module if OpenCV is not installed (heavy dependency).
cv2 = pytest.importorskip(
    "cv2", reason="OpenCV not installed – skipping liveness tests"
)

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.liveness import (
    detect_blink,
    eye_aspect_ratio,
    face_sharpness,
    is_likely_live,
)

# ---------------------------------------------------------------------------
# eye_aspect_ratio
# ---------------------------------------------------------------------------


class TestEyeAspectRatio:
    def _open_eye(self):
        """Approximate landmarks for an open eye (EAR ≈ 0.3)."""
        return [(0, 0), (1, 3), (3, 3), (4, 0), (3, -3), (1, -3)]

    def _closed_eye(self):
        """Approximate landmarks for a closed eye (EAR ≈ 0)."""
        return [(0, 0), (1, 0), (3, 0), (4, 0), (3, 0), (1, 0)]

    def test_open_eye_has_high_ear(self):
        ear = eye_aspect_ratio(self._open_eye())
        assert ear > 0.2

    def test_closed_eye_has_zero_ear(self):
        ear = eye_aspect_ratio(self._closed_eye())
        assert ear == pytest.approx(0.0)

    def test_zero_horizontal_distance_returns_zero(self):
        # All points at same x – degenerate case
        landmarks = [(0, 0)] * 6
        assert eye_aspect_ratio(landmarks) == pytest.approx(0.0)

    def test_returns_float(self):
        ear = eye_aspect_ratio(self._open_eye())
        assert isinstance(ear, float)


# ---------------------------------------------------------------------------
# detect_blink
# ---------------------------------------------------------------------------


class TestDetectBlink:
    def test_no_blink_when_always_open(self):
        ear_values = [0.30, 0.31, 0.29, 0.30]
        assert detect_blink(ear_values) is False

    def test_blink_detected_when_ear_dips(self):
        # Two frames closed, then open again
        ear_values = [0.30, 0.15, 0.14, 0.30]
        assert detect_blink(ear_values, ear_threshold=0.21, consec_frames=2) is True

    def test_single_frame_dip_not_a_blink(self):
        # Only one frame below threshold – not enough for a blink
        ear_values = [0.30, 0.15, 0.30]
        assert detect_blink(ear_values, ear_threshold=0.21, consec_frames=2) is False

    def test_empty_sequence_no_blink(self):
        assert detect_blink([]) is False

    def test_all_closed_frames_without_recovery_not_a_blink(self):
        ear_values = [0.10, 0.10, 0.10]
        # No recovery frame – consecutive low count never resets to trigger
        assert detect_blink(ear_values, consec_frames=2) is False

    def test_consec_frames_one(self):
        ear_values = [0.30, 0.15, 0.30]
        assert detect_blink(ear_values, consec_frames=1) is True


# ---------------------------------------------------------------------------
# face_sharpness
# ---------------------------------------------------------------------------


class TestFaceSharpness:
    def _make_sharp_image(self) -> np.ndarray:
        """Create a high-contrast chessboard-style BGR image."""
        img = np.zeros((64, 64, 3), dtype=np.uint8)
        for i in range(0, 64, 8):
            for j in range(0, 64, 8):
                if (i // 8 + j // 8) % 2 == 0:
                    img[i : i + 8, j : j + 8] = 255
        return img

    def _make_blurry_image(self) -> np.ndarray:
        """Create a heavily blurred (low-sharpness) image."""
        base = self._make_sharp_image()
        return cv2.GaussianBlur(base, (31, 31), 10)

    def test_sharp_image_has_high_variance(self):
        assert face_sharpness(self._make_sharp_image()) > 100

    def test_blurry_image_has_low_variance(self):
        assert face_sharpness(self._make_blurry_image()) < 50

    def test_grayscale_input_accepted(self):
        gray = np.zeros((64, 64), dtype=np.uint8)
        gray[::8, ::8] = 255
        score = face_sharpness(gray)
        assert isinstance(score, float)

    def test_returns_non_negative(self):
        img = self._make_sharp_image()
        assert face_sharpness(img) >= 0.0


# ---------------------------------------------------------------------------
# is_likely_live
# ---------------------------------------------------------------------------


class TestIsLikelyLive:
    def _chessboard(self) -> np.ndarray:
        img = np.zeros((64, 64, 3), dtype=np.uint8)
        for i in range(0, 64, 8):
            for j in range(0, 64, 8):
                if (i // 8 + j // 8) % 2 == 0:
                    img[i : i + 8, j : j + 8] = 255
        return img

    def test_sharp_image_is_live(self):
        assert is_likely_live(self._chessboard(), sharpness_threshold=50.0) is True

    def test_blurry_image_is_not_live(self):
        blurry = cv2.GaussianBlur(self._chessboard(), (31, 31), 10)
        assert is_likely_live(blurry, sharpness_threshold=50.0) is False

    def test_threshold_zero_always_live(self):
        blurry = cv2.GaussianBlur(self._chessboard(), (31, 31), 10)
        assert is_likely_live(blurry, sharpness_threshold=0.0) is True
