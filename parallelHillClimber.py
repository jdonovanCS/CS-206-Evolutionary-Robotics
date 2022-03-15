import solution
import constants as c
import copy
import os

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system("del fitness*.txt")
        os.system("del brain*.nndf")
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(c.populationSize):
            self.parents[i] = solution.SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
    
    def Evolve(self):
        for k in self.parents:
            self.parents[k].Start_Simulation('DIRECT')

        for k in self.parents:
            self.parents[k].Wait_For_Simulation_To_End()
        
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        pass
        # self.Spawn()
        # self.Mutate()
        # self.child.Evaluate('DIRECT')
        # self.Print()
        # self.Select()

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)
        self.child.Set_ID(self.nextAvailableID)
        self.nextAvailableID += 1

    def Mutate(self):
        self.child.Mutate()

    def Select(self):
        if self.child.fitness < self.parent.fitness:
            self.parent = copy.deepcopy(self.child)

    def Print(self):
        print('parent: {}, child: {}'.format(self.parent.fitness, self.child.fitness))

    def Show_Best(self):
        # self.parent.Evaluate('GUI')
        pass
        

