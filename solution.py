import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random

class SOLUTION:
    def __init__(self):
        self.weights = np.random.rand(3,2)*2-1
        self.length = 1
        self.width = 1
        self.height = 1

        self.x = 0
        self.y = 0
        self.z = self.height+self.height/2

    def Evaluate(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system("conda activate ER")
        os.system("python simulate.py " + directOrGUI)
        with open('fitness.txt', 'r') as f:
            self.fitness = np.double(f.read())  
        
    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[self.x-5,self.y,self.z], size=[self.length,self.width,self.height])
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0,0,1.5], size=[self.length,self.width,self.height])
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[-.5, 0, 1])
        pyrosim.Send_Cube(name="BackLeg", pos=[-.5, 0, -.5], size=[self.length, self.width, self.height])
        pyrosim.Send_Joint(name="Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [.5,0,1])
        pyrosim.Send_Cube(name="FrontLeg", pos=[.5, 0, -.5], size=[self.length, self.width, self.height])
        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain.nndf")
        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")
        pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")
        for currentRow in range(self.weights.shape[0]):
            for currentColumn in range(self.weights.shape[1]):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn+3, weight=self.weights[currentRow][currentColumn])

        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0, self.weights.shape[0]-1)
        randomColumn = random.randint(0, self.weights.shape[1]-1)
        self.weights[randomRow][randomColumn] = random.random() * 2 -1