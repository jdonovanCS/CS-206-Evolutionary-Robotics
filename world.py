import pybullet as p
import os

class WORLD:
    def __init__(self, solutionID):
        self.planeId = p.loadURDF("plane.urdf")
        p.loadSDF("world{}.sdf".format(solutionID))
        os.system('del \"world{}.sdf\"'.format(solutionID))