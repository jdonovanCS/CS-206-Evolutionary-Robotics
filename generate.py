import pyrosim.pyrosim as pyrosim
import random

length = 1
width = 1
height = 1

x = 0
y = 0
z = height+height/2



def createWorld():
    pyrosim.Start_SDF("world.sdf")
    pyrosim.Send_Cube(name="Box", pos=[x-5,y,z], size=[length,width,height])
    pyrosim.End()

def createRobot():
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name="Torso", pos=[0,0,1.5], size=[length,width,height])
    pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[-.5, 0, 1])
    pyrosim.Send_Cube(name="BackLeg", pos=[-.5, 0, -.5], size=[length, width, height])
    pyrosim.Send_Joint(name="Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [.5,0,1])
    pyrosim.Send_Cube(name="FrontLeg", pos=[.5, 0, -.5], size=[length, width, height])
    pyrosim.End()

def Generate_Body():
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name="Torso", pos=[0,0,1.5], size=[length,width,height])
    pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[-.5, 0, 1])
    pyrosim.Send_Cube(name="BackLeg", pos=[-.5, 0, -.5], size=[length, width, height])
    pyrosim.Send_Joint(name="Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [.5,0,1])
    pyrosim.Send_Cube(name="FrontLeg", pos=[.5, 0, -.5], size=[length, width, height])
    pyrosim.End()

def Generate_Brain():
    pyrosim.Start_NeuralNetwork("brain.nndf")
    pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
    pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
    pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")
    pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
    pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")
    pyrosim.Send_Synapse(sourceNeuronName=1, targetNeuronName=3, weight=1.0)
    pyrosim.Send_Synapse(sourceNeuronName=2, targetNeuronName=3, weight=.2)
    pyrosim.Send_Synapse(sourceNeuronName=0, targetNeuronName=4, weight=1.0)
    pyrosim.Send_Synapse(sourceNeuronName=1, targetNeuronName=4, weight=.2)
    pyrosim.Send_Synapse(sourceNeuronName=2, targetNeuronName=4, weight=1.0)
    pyrosim.End()

createWorld()  
createRobot()
Generate_Body()
Generate_Brain()

# pyrosim.Send_Cube(name="Box2", pos=[x+length,y,z+height], size=[length,width,height])

# num_blocks=10
# world_width = 6
# world_length = 6
# for k in range(world_width):
#     y = width*k
#     for j in range(world_length):
#         x = length*j
#         for i in range(num_blocks):
#             pyrosim.Send_Cube(name="Box{}".format(i), pos=[x,y,z+(height*i)], size=[length*(.9**i),width*(.9**i),height*(.9**i)])


