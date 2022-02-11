import matplotlib.pyplot as plt
import numpy as np

backLegTouchSenorValues = np.load("data/backLegTouchSensor.npy")
frontLegTouchSensorValues = np.load("data/frontLegTouchSensor.npy")
plt.plot(backLegTouchSenorValues, label="backLegTouch", linewidth=3.5)
plt.plot(frontLegTouchSensorValues, label="frontLegTouch")
plt.legend()
plt.show()

targetAngles = np.load("data/targetAngles.npy")
plt.plot(targetAngles, label="target angles")
targetAngles = np.load("data/b_targetAngles.npy")
plt.plot(targetAngles, label="front target angles")
targetAngles = np.load("data/f_targetAngles.npy")
plt.plot(targetAngles, label="back target angles")
plt.show()