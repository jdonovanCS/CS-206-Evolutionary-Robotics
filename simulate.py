import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as np
import random

steps = 1000
b_amplitude = np.pi/4
b_frequency = 10
b_phaseOffset = 0
f_amplitude = np.pi/4
f_frequency = 10
f_phaseOffset = np.pi/2


physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotId)
backLegSensorValues = np.zeros(steps)
frontLegSensorValues = np.zeros(steps)
targetBeforeSin = np.linspace(0, (2*np.pi), 1000)
# targetAngles = (np.sin(targetBeforeSin))*(np.pi/4)
b_targetAngles = b_amplitude * np.sin(b_frequency * targetBeforeSin + b_phaseOffset)
f_targetAngles = f_amplitude * np.sin(f_frequency * targetBeforeSin + f_phaseOffset)
np.save("data/b_targetAngles.npy", b_targetAngles)
np.save("data/f_targetAngles.npy", f_targetAngles)
for i in range(steps):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, jointName="Torso_BackLeg", controlMode=p.POSITION_CONTROL, targetPosition=b_targetAngles[i], maxForce=35)
    pyrosim.Set_Motor_For_Joint(bodyIndex=robotId, jointName="Torso_FrontLeg", controlMode=p.POSITION_CONTROL, targetPosition=f_targetAngles[i], maxForce=35)
    time.sleep(1/60)
np.save("data/backLegTouchSensor.npy", backLegSensorValues)
np.save("data/frontLegTouchSensor.npy", frontLegSensorValues)

p.disconnect()
