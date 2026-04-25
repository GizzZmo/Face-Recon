"""
Liveness detection utilities for Face-Recon system.

This module provides basic anti-spoofing checks to distinguish a live
person from a photograph or video replay.  The current implementation
uses two complementary heuristics that work without additional ML models:

1. **Blink detection** – tracks the Eye Aspect Ratio (EAR) over successive
   frames and flags a blink when the ratio drops below a threshold.
2. **Texture analysis** – computes the Laplacian variance of the face crop.
   A blurry, low-variance region often indicates a printed photo.

For production deployments consider replacing or supplementing these
heuristics with a dedicated depth-map or IR-based anti-spoofing model.
"""

from typing import List, Tuple

import cv2
import numpy as np

# ---------------------------------------------------------------------------
# Eye Aspect Ratio (EAR)
# ---------------------------------------------------------------------------


def eye_aspect_ratio(eye_landmarks: List[Tuple[int, int]]) -> float:
    """
    Compute the Eye Aspect Ratio (EAR) for a single eye.

    The EAR formula is defined in Soukupová & Čech (2016):

        EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)

    where p1..p6 are the six 2-D landmark points of the eye in order:
    left-corner, upper-left, upper-right, right-corner, lower-right,
    lower-left.

    Args:
        eye_landmarks: List of six (x, y) landmark tuples.

    Returns:
        Float EAR value – close to 0 when eye is shut, ~0.25-0.35 when open.

    Example:
        >>> pts = [(0,0),(1,2),(2,2),(3,0),(2,-2),(1,-2)]
        >>> round(eye_aspect_ratio(pts), 2)
        1.33
    """
    p1, p2, p3, p4, p5, p6 = [np.array(p, dtype=float) for p in eye_landmarks]
    vertical_1 = float(np.linalg.norm(p2 - p6))
    vertical_2 = float(np.linalg.norm(p3 - p5))
    horizontal = float(np.linalg.norm(p1 - p4))
    if horizontal == 0.0:
        return 0.0
    return (vertical_1 + vertical_2) / (2.0 * horizontal)


def detect_blink(
    ear_values: List[float],
    ear_threshold: float = 0.21,
    consec_frames: int = 2,
) -> bool:
    """
    Detect whether a blink occurred in a sequence of EAR values.

    A blink is detected when the EAR falls below *ear_threshold* for at
    least *consec_frames* consecutive frames followed by a recovery above
    the threshold.

    Args:
        ear_values: Ordered list of EAR values from successive frames.
        ear_threshold: EAR value below which the eye is considered closed.
        consec_frames: Minimum number of consecutive low-EAR frames that
            constitute a blink.

    Returns:
        ``True`` if a blink was detected, ``False`` otherwise.
    """
    below = [v < ear_threshold for v in ear_values]
    count = 0
    for closed in below:
        if closed:
            count += 1
        else:
            if count >= consec_frames:
                return True
            count = 0
    return False


# ---------------------------------------------------------------------------
# Texture / sharpness analysis
# ---------------------------------------------------------------------------


def face_sharpness(face_image: np.ndarray) -> float:
    """
    Return the Laplacian variance of a face image crop as a sharpness score.

    A high variance indicates a sharp (likely live) face; a low variance
    suggests a blurry image such as a printed photograph held in front of
    the camera.

    Args:
        face_image: Grayscale or BGR face crop as a NumPy array.

    Returns:
        Non-negative float – higher means sharper.
    """
    if len(face_image.shape) == 3:
        gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
    else:
        gray = face_image
    return float(cv2.Laplacian(gray, cv2.CV_64F).var())


def is_likely_live(
    face_image: np.ndarray,
    sharpness_threshold: float = 80.0,
) -> bool:
    """
    Heuristic liveness check based on image sharpness.

    A face region that is too blurry is flagged as a potential spoof
    (e.g., a low-resolution print or phone screen).

    Args:
        face_image: BGR or grayscale face crop.
        sharpness_threshold: Minimum Laplacian variance to be considered
            live.  Tune this for your camera and lighting conditions.

    Returns:
        ``True`` if the face appears live, ``False`` if it may be a spoof.
    """
    return face_sharpness(face_image) >= sharpness_threshold
