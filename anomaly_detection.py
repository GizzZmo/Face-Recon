"""
Anomaly detection module for identifying unusual access patterns.

Uses Isolation Forest algorithm to detect anomalous behavior
in access times or patterns.
"""

import numpy as np
from sklearn.ensemble import IsolationForest

# Training data: access times (hours). 50 is an anomalous value.
data = np.array([[8], [12], [15], [50]])

# Train isolation forest model for anomaly detection
model = IsolationForest(contamination=0.25, random_state=42)
model.fit(data)


def detect_anomaly(value: float) -> int:
    """
    Detect if a value is anomalous.

    Args:
        value: The value to check (e.g., access time)

    Returns:
        1 if normal, -1 if anomalous
    """
    prediction = model.predict([[value]])[0]
    return int(prediction)


def is_anomalous_access(value: float) -> bool:
    """
    Check if access time is anomalous.

    Args:
        value: Access time or other metric

    Returns:
        True if anomalous, False if normal
    """
    return detect_anomaly(value) == -1


# Example usage
if __name__ == "__main__":
    test_value = 50
    result = detect_anomaly(test_value)
    status = "Anomalous" if result == -1 else "Normal"
    print(f"Value {test_value}: {status} activity detected")
