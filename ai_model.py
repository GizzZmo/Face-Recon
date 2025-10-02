import numpy as np
from sklearn.neural_network import MLPClassifier

data = np.array([[8, 1], [12, 0], [15, 1]])
labels = np.array([1, 0, 1])

model = MLPClassifier(hidden_layer_sizes=(10, 10), max_iter=1000)
model.fit(data, labels)


def predict_smart_access(time, history):
    return model.predict([[time, history]])[0]


print(predict_smart_access(10, 1))  # Dynamisk adgangsvurdering!
