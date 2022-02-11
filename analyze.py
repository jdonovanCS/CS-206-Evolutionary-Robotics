import matplotlib.pyplot as plt
import numpy as np

backLegTouchSenorValues = np.load("data/backLegTouchSensor.npy")
frontLegTouchSensorValues = np.load("data/frontLegTouchSensor.npy")
plt.plot(backLegTouchSenorValues, label="backLegTouch", linewidth=3.5)
plt.plot(frontLegTouchSensorValues, label="frontLegTouch")
plt.legend()
plt.show()