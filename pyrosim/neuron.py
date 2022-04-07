import math

import pybullet

import pyrosim.pyrosim as pyrosim

import pyrosim.constants as c

class NEURON: 

    def __init__(self,line):

        self.Determine_Name(line)

        self.Determine_Type(line)

        self.Determine_Activation_Fn(line)

        self.Search_For_Link_Name(line)

        self.Search_For_Joint_Name(line)

        self.Set_Value(0.0)

    def Add_To_Value( self, value ):

        self.Set_Value( self.Get_Value() + value )

    def Get_Joint_Name(self):

        return self.jointName

    def Get_Link_Name(self):

        return self.linkName

    def Get_Name(self):

        return self.name

    def Get_Value(self):
            
        return self.value

    def Is_Sensor_Neuron(self):

        return self.type == c.SENSOR_NEURON

    def Update_Sensor_Neuron(self):

        self.Set_Value(pyrosim.Get_Touch_Sensor_Value_For_Link(self.Get_Link_Name()))

    def Is_Hidden_Neuron(self):

        return self.type == c.HIDDEN_NEURON

    def Is_Motor_Neuron(self):

        return self.type == c.MOTOR_NEURON

    def Update_Hidden_Or_Motor_Neuron(self, neurons, synapses):

        for k in synapses.keys():

            if k[1] == self.Get_Name():
                
                self.Allow_Presynaptic_Neuron_To_Influence_Me(synapses[k].Get_Weight(), neurons[k[0]].Get_Value())
        
        self.Threshold()


    # def Update_CPG_Neuron(self, neurons, synapses):

    #     for k in synapses.keys():

    #         if k[1] == self.Get_Name():

    #             self.Allow_Presynaptic_Neuron_To_Influence_Me(synapses[k].Get_Weight(), neurons[k[0]].Get_Value())


    def Allow_Presynaptic_Neuron_To_Influence_Me(self, weight, value):

        self.Add_To_Value(weight*value)

    def Print(self):

        # self.Print_Name()

        # self.Print_Type()

        self.Print_Value()

        # print("")

    def Set_Value(self,value):

        self.value = value

# -------------------------- Private methods -------------------------

    def Determine_Name(self,line):

        if "name" in line:

            splitLine = line.split('"')

            self.name = splitLine[1]

    def Determine_Type(self,line):

        if "sensor" in line:

            self.type = c.SENSOR_NEURON

        elif "motor" in line:

            self.type = c.MOTOR_NEURON

        else:

            self.type = c.HIDDEN_NEURON
    
    def Determine_Activation_Fn(self,line):

        if "activation_fn" in line:

            splitLine = line.split('"')

            self.activation_fn = splitLine[3]
        
        else:
            
            self.activation_fn = "tanh"

    def Print_Name(self):

       print(self.name)

    def Print_Type(self):

       print(self.type)

    def Print_Value(self):

       print(self.value , " " , end="" )

    def Search_For_Joint_Name(self,line):

        if "jointName" in line:

            splitLine = line.split('"')

            self.jointName = splitLine[5]

    def Search_For_Link_Name(self,line):

        if "linkName" in line:

            splitLine = line.split('"')

            self.linkName = splitLine[5]

    def Threshold(self):

        if self.activation_fn == "sin":
            
            self.value = math.sin(self.value)

        elif self.activation_fn == "sigmoid":

            if self.value >= 0:

                self.value = 1 / (1 + math.exp(-self.value))
            
            else:
                
                self.value = 1 / (1 + math.exp(self.value))

        elif self.activation_fn == "relu":

            self.value = max(0, self.value)

        elif self.activation_fn == "leakyrelu":

            if self.value < 0:
                
                self.value = 0.01 * self.value
        
        else:

            self.value = math.tanh(self.value)

        
