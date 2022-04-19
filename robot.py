from sensor import SENSOR
from motor import MOTOR
import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import constants as c
import numpy as np

class ROBOT:
    def __init__(self, solutionID):
        self.motors = {}
        self.robot = p.loadURDF("body{}.urdf".format(solutionID))
        self.solutionID = solutionID
        pyrosim.Prepare_To_Simulate(self.robot)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        self.nn = NEURAL_NETWORK("brain{}.nndf".format(solutionID))
        os.system('del \"brain{}.nndf\"'.format(solutionID))
        os.system('del \"body{}.urdf\"'.format(solutionID))


    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)
        self.footprint_graph = np.zeros((len(self.sensors)*10, c.STEPS))

    def Sense(self, timestep):
        for i, s in enumerate(self.sensors.values()):
            s.Get_Value(timestep)
            self.footprint_graph[i*10:(i*10)+10, timestep] = s.values[timestep]
            self.footprint_graph[i*10:(i*10+2), timestep] = 0
            self.footprint_graph[(i*10)+8:(i*10)+10, timestep] = 0

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Act(self, timestep):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                # desiredAngle = self.nn.Get_Value_Of(neuronName)
                self.motors[jointName].Set_Value(self.robot, desiredAngle)

    def Think(self):
        self.nn.Update()
        # self.nn.Print()

    def Get_Fitness(self):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robot)
        basePosition = basePositionAndOrientation[0]
        xPosition = basePosition[0]
        with open('tmp{}.txt'.format(self.solutionID), 'w') as f:
            f.write(str(xPosition))
        os.rename('tmp{}.txt'.format(self.solutionID), 'fitness{}.txt'.format(self.solutionID))

    def Save_Values(self):
        for s in self.sensors.values():
            s.Save_Values()
        for m in self.motors.values():
            m.Save_Values()

