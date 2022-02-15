import numpy as np
steps = 1000
b_amplitude = np.pi/4
b_frequency = 10
b_phaseOffset = 0
f_amplitude = np.pi/4
f_frequency = 10
f_phaseOffset = np.pi/2
targetBeforeSin = np.linspace(0, (2*np.pi), 1000)
targetAngles = (np.sin(targetBeforeSin))*(np.pi/4)
b_targetAngles = b_amplitude * np.sin(b_frequency * targetBeforeSin + b_phaseOffset)
f_targetAngles = f_amplitude * np.sin(f_frequency * targetBeforeSin + f_phaseOffset)

STEPS = 1000
AMPLITUDE = np.pi/4
FREQUENCY = 10
PHASE_OFFSET = 0
TARGET_ANGLES = targetBeforeSin