"""
AI-based anomaly detection for access logs or sensor data.
"""

import numpy as np
from sklearn.ensemble import IsolationForest


class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest()

    def fit(self, data):
        self.model.fit(data)

    def detect(self, value):
        return self.model.predict([[value]])[0]


if __name__ == "__main__":
    # Example usage
    data = np.array([[8], [12], [15], [50]])  # 50 is an anomaly
    detector = AnomalyDetector()
    detector.fit(data)
    print(detector.detect(50))  # Output: -1 (anomaly), 1 (normal)
