from robot import ROBOT
from world import WORLD
import pybullet as p
import pybullet_data
import time
import constants as c

class SIMULATION:
    def __init__(self, directOrGUI, solutionID):
        self.directOrGUI = directOrGUI
        self.solutionID = solutionID
        if self.directOrGUI == 'DIRECT':
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
            p.startStateLogging(loggingType=3, fileName='video_of_best.mp4')
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.8)
        self.world = WORLD(solutionID)
        self.robot = ROBOT(solutionID)

    def Run(self):
        for i in range(c.STEPS):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)
            if self.directOrGUI == 'GUI':
                time.sleep(c.SLEEP_RATE)

    def Get_Fitness(self):
        self.robot.Get_Fitness()
    
    def __del__(self):
        self.robot.Save_Values()
        p.disconnect()
        