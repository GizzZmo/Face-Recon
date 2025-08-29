import numpy as np
from sklearn.ensemble import IsolationForest

data = np.array([[8], [12], [15], [50]])  # 50 er en anomal verdi
model = IsolationForest()
model.fit(data)


def detect_anomaly(value):
    return model.predict([[value]])


print(detect_anomaly(50))  # Detekterer uvanlig aktivitet
