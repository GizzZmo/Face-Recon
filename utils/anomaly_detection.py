"""
AI-based anomaly detection for access logs or sensor data.

Provides a wrapper class around Isolation Forest for detecting
unusual patterns in security system data.
"""

import numpy as np
from sklearn.ensemble import IsolationForest


class AnomalyDetector:
    """
    Anomaly detection using Isolation Forest algorithm.

    Useful for detecting unusual access patterns, times, or behaviors
    in security system logs.
    """

    def __init__(self, contamination: float = 0.1, random_state: int = 42):
        """
        Initialize anomaly detector.

        Args:
            contamination: Expected proportion of outliers (0.0-0.5)
            random_state: Random seed for reproducibility
        """
        self.model = IsolationForest(
            contamination=contamination, random_state=random_state
        )

    def fit(self, data: np.ndarray) -> None:
        """
        Train the anomaly detection model.

        Args:
            data: Training data array, shape (n_samples, n_features)
        """
        self.model.fit(data)

    def detect(self, value: float) -> int:
        """
        Detect if a value is anomalous.

        Args:
            value: Single value to check

        Returns:
            -1 if anomalous, 1 if normal
        """
        return int(self.model.predict([[value]])[0])

    def is_anomaly(self, value: float) -> bool:
        """
        Check if value is an anomaly.

        Args:
            value: Value to check

        Returns:
            True if anomalous, False if normal
        """
        return self.detect(value) == -1


if __name__ == "__main__":
    # Example usage
    data = np.array([[8], [12], [15], [50]])  # 50 is an anomaly
    detector = AnomalyDetector()
    detector.fit(data)

    test_value = 50
    result = detector.detect(test_value)
    status = "Anomaly" if result == -1 else "Normal"
    print(f"Value {test_value}: {status} detected")
