"""
AI model for smart access control decisions.

This module demonstrates using machine learning to make dynamic access
control decisions based on time of day and user history.
"""

import numpy as np
from sklearn.neural_network import MLPClassifier

# Training data: [time_of_day, access_history] -> access_granted
# Example: [8am, has_history], [12pm, no_history], [3pm, has_history]
data = np.array([[8, 1], [12, 0], [15, 1]])
labels = np.array([1, 0, 1])  # 1 = grant access, 0 = deny access

# Train a simple neural network classifier
model = MLPClassifier(hidden_layer_sizes=(10, 10), max_iter=1000, random_state=42)
model.fit(data, labels)


def predict_smart_access(time_of_day: int, access_history: int) -> int:
    """
    Predict whether to grant access based on time and history.

    Args:
        time_of_day: Hour of day (0-23)
        access_history: 1 if user has previous access, 0 otherwise

    Returns:
        1 if access should be granted, 0 if denied
    """
    return int(model.predict([[time_of_day, access_history]])[0])


# Example usage
if __name__ == "__main__":
    result = predict_smart_access(10, 1)
    print(f"Access decision for 10am with history: {'Granted' if result else 'Denied'}")
