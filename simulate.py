import pybullet as p
import time
import pybullet_data

steps = 1000

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")
for i in range(steps):
    p.stepSimulation()
    time.sleep(1/60)
    print(i)

p.disconnect()