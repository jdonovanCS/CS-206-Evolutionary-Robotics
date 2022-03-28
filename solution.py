import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c

class SOLUTION:
    def __init__(self, myId):
        self.s_h_weights = np.random.rand(c.numSensorNeurons,c.numHiddenNeurons)*2-1
        self.h_m_weights = np.random.rand(c.numHiddenNeurons, c.numMotorNeurons)*2-1
        self.numHiddenNeurons = c.numHiddenNeurons
        self.h_rec_weights = np.random.rand(c.numHiddenNeurons)*2-1
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
            time.sleep(.1)
        with open(fitnessFileName, 'r') as f:
            self.fitness = np.double(f.read())
        os.system("del {}".format(fitnessFileName))
        
    def Create_World(self):
        pyrosim.Start_SDF("world{}.sdf".format(self.myID))
        # pyrosim.Send_Cube(name="Box", pos=[self.x-5,self.y,self.z], size=[self.length,self.width,self.height])
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body{}.urdf".format(self.myID))
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
        for i in range(c.numSensorNeurons):
            pyrosim.Send_Sensor_Neuron(name=i, linkName=pyrosim.links[i].name)

        for j in range(0, self.numHiddenNeurons):
            pyrosim.Send_Hidden_Neuron(name=j+c.numSensorNeurons)

        for k in range(0, c.numMotorNeurons):
            pyrosim.Send_Motor_Neuron(name=k+self.numHiddenNeurons+c.numSensorNeurons, jointName=pyrosim.joints[k].name)
        
        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(self.numHiddenNeurons):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn+c.numSensorNeurons, weight=self.s_h_weights[currentRow][currentColumn])
        for currentRow in range(self.numHiddenNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow+c.numSensorNeurons, targetNeuronName=currentColumn+c.numSensorNeurons+self.numHiddenNeurons, weight=self.h_m_weights[currentRow][currentColumn])
        for currentHidden in range(self.numHiddenNeurons):
            pyrosim.Send_Synapse(sourceNeuronName=c.numSensorNeurons+currentHidden, targetNeuronName=c.numSensorNeurons+currentHidden, weight=self.h_rec_weights[currentHidden])
            # for anotherHidden in range(self.numHiddenNeurons):


        pyrosim.End()

    def Mutate(self):
        action = random.randint(0, 3)
        match action:
            case 0: # modify random sensor->hidden weight
                randomRow = random.randint(0, c.numSensorNeurons-1)
                randomColumn = random.randint(0, self.numHiddenNeurons-1)
                self.s_h_weights[randomRow][randomColumn] *= (np.random.rand() * 2 -1)
            case 1: # modify random hidden->motor weight
                randomRow = random.randint(0, self.numHiddenNeurons-1)
                randomColumn = random.randint(0, c.numMotorNeurons-1)
                self.h_m_weights[randomRow][randomColumn] *= (np.random.rand() * 2 -1)
            case 2: # modify random recurrent weight
                randomHidden = random.randint(0, self.numHiddenNeurons-1)
                self.h_rec_weights[randomHidden] *= (np.random.rand() * 2 - 1)
            case 3: # add hidden neuron with random weight connections from sensors, to motors, and recurrent
                self.numHiddenNeurons += 1
                new_col = (np.random.rand(c.numSensorNeurons) * 2 - 1).reshape(c.numSensorNeurons, 1)
                self.s_h_weights = np.concatenate((self.s_h_weights, new_col), 1)
                new_row = (np.random.rand(c.numMotorNeurons)*2-1).reshape(1,c.numMotorNeurons)
                self.h_m_weights = np.concatenate((self.h_m_weights, new_row))
                self.h_rec_weights = np.append(self.h_rec_weights, np.random.rand()*2-1)
            case 4:
                return
