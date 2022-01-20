import pybullet as p
import time


steps = 1000

physicsClient = p.connect(p.GUI)
p.loadSDF("box.sdf")
for i in range(steps):
    p.stepSimulation()
    time.sleep(1/60)
    print(i)

p.disconnect()