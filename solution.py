import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c

class SOLUTION:
    def __init__(self, myId):
        self.weights = np.random.rand(c.numSensorNeurons,c.numMotorNeurons)*2-1
        self.myID = myId
        self.length = 1
        self.width = 1
        self.height = 1

        self.x = 0
        self.y = 0
        self.z = self.height+self.height/2
        os.system("conda activate ER")

    def Set_ID(self, id):
        self.myID = id

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system("start /B python simulate.py {} {}".format(directOrGUI, self.myID))

    def Wait_For_Simulation_To_End(self):
        fitnessFileName = 'fitness{}.txt'.format(self.myID)
        while not os.path.exists(fitnessFileName):
            time.sleep(.01)
        with open(fitnessFileName, 'r') as f:
            self.fitness = np.double(f.read())
        os.system("del {}".format(fitnessFileName))
        
    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        # pyrosim.Send_Cube(name="Box", pos=[self.x-5,self.y,self.z], size=[self.length,self.width,self.height])
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0,0,1], size=[self.length,self.width,self.height])
        
        # back leg
        pyrosim.Send_Cube(name="BackLeg", pos=[0, -0.5, 0], size=[0.2, 1, 0.2])
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[0, -0.5, 1], jointAxis='1 0 0')
        pyrosim.Send_Cube(name="LowerBackLeg", pos=[0, 0, -0.5], size=[.2, .2, 1])
        pyrosim.Send_Joint(name="BackLeg_LowerBackLeg", parent="BackLeg", child="LowerBackLeg",type="revolute", position=[0, -1, 0], jointAxis = "1 0 0")

        # front leg
        pyrosim.Send_Cube(name="FrontLeg", pos=[0, 0.5, 0], size=[0.2, 1, 0.2])
        pyrosim.Send_Joint(name="Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [0,0.5,1], jointAxis='1 0 0')
        pyrosim.Send_Cube(name="LowerFrontLeg", pos=[0, 0, -0.5], size=[.2, .2, 1])
        pyrosim.Send_Joint(name="FrontLeg_LowerFrontLeg", parent="FrontLeg", child="LowerFrontLeg",type="revolute", position=[0, 1, 0], jointAxis = "1 0 0")

        # left leg
        pyrosim.Send_Cube(name="LeftLeg", pos=[-0.5, 0, 0], size=[1, 0.2, 0.2])
        pyrosim.Send_Joint(name="Torso_LeftLeg", parent="Torso", child="LeftLeg", type="revolute", position=[-0.5, 0, 1], jointAxis='0 1 0')
        pyrosim.Send_Cube(name="LowerLeftLeg", pos=[0, 0, -.5], size=[.2, .2, 1])
        pyrosim.Send_Joint(name="LeftLeg_LowerLeftLeg", parent="LeftLeg", child="LowerLeftLeg",type="revolute", position=[-1, 0, 0], jointAxis = "0 1 0")

        # right leg
        pyrosim.Send_Cube(name="RightLeg", pos=[0.5, 0, 0], size=[1, 0.2, 0.2])
        pyrosim.Send_Joint(name="Torso_RightLeg" , parent= "Torso" , child = "RightLeg" , type = "revolute", position = [0.5,0,1], jointAxis='0 1 0')
        pyrosim.Send_Cube(name="LowerRightLeg", pos=[0, 0, -.5], size=[.2, .2, 1]) 
        pyrosim.Send_Joint(name="RightLeg_LowerRightLeg", parent="RightLeg", child="LowerRightLeg", type="revolute", position=[1, 0, 0], jointAxis = "0 1 0")
        
        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain{}.nndf".format(self.myID))
        # pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        # pyrosim.Send_Sensor_Neuron(name=1, linkName="FrontLeg")
        # pyrosim.Send_Sensor_Neuron(name=2, linkName="BackLeg")
        # pyrosim.Send_Sensor_Neuron(name=3, linkName="LeftLeg")
        # pyrosim.Send_Sensor_Neuron(name=4, linkName="RightLeg")
                
        pyrosim.Send_Sensor_Neuron(name=0, linkName="LowerFrontLeg")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="LowerBackLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="LowerLeftLeg")
        pyrosim.Send_Sensor_Neuron(name=3, linkName="LowerRightLeg")
        
        pyrosim.Send_Motor_Neuron(name=4 , jointName="Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron(name=5, jointName="Torso_BackLeg")   
        pyrosim.Send_Motor_Neuron(name=6, jointName="Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron(name=7, jointName="Torso_RightLeg")
                
        pyrosim.Send_Motor_Neuron(name=8, jointName="FrontLeg_LowerFrontLeg")
        pyrosim.Send_Motor_Neuron(name=9, jointName="BackLeg_LowerBackLeg")   
        pyrosim.Send_Motor_Neuron(name=10, jointName="LeftLeg_LowerLeftLeg")
        pyrosim.Send_Motor_Neuron(name=11, jointName="RightLeg_LowerRightLeg")
        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn+c.numSensorNeurons, weight=self.weights[currentRow][currentColumn])

        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0, c.numSensorNeurons-1)
        randomColumn = random.randint(0, c.numMotorNeurons-1)
        self.weights[randomRow][randomColumn] = random.random() * 2 -1