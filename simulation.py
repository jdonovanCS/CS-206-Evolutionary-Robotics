from robot import ROBOT
from world import WORLD
import pybullet as p
import pybullet_data
import time
import constants as c
import sys
import matplotlib.pyplot as plt
import wandb

class SIMULATION:
    def __init__(self, directOrGUI, solutionID):
        self.directOrGUI = directOrGUI
        self.solutionID = solutionID
        if self.directOrGUI == 'DIRECT':
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
            fileName = 'video_of_best.mp4'
            p.startStateLogging(loggingType=p.STATE_LOGGING_VIDEO_MP4, fileName=fileName)
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
                if i == c.STEPS-1:
                    api = wandb.Api()
                    runs = api.runs(path="jdonovan/CS-206-Evolutionary-Robotics", filters={"config.version": "fp-base", "config.population": c.populationSize}, order="-created_at", per_page=10)
                    run=runs[0]
                    image = wandb.Image(self.robot.footprint_graph, caption="footprint_graph")
                    print('logging footprint')
                    run2 = api.run(path="jdonovan/CS-206-Evolutionary-Robotics/" + run.path[2])
                    run2.config = run.config
                    wandb.init(id=run.path[2])
                    wandb.log({'footprint_graph': image})
                    wandb.finish()
                    run2.update()
                    print('done logging')

    def Get_Fitness(self):
        self.robot.Get_Fitness()
    
    def __del__(self):
        self.robot.Save_Values()
        p.disconnect()
        