import solution
import constants as c
import copy
import os

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system('del \"fitness*.txt\"')
        os.system('del \"brain*.nndf\"')
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(c.populationSize):
            self.parents[i] = solution.SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
    
    def Evolve(self):
        self.Evaluate(self.parents)
        
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()

    def Spawn(self):
        self.children = {}
        for k in self.parents:
            self.children[k] = copy.deepcopy(self.parents[k])
            self.children[k].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for k in self.children:
           self.children[k].Mutate()

    def Evaluate(self, solutions):
        for k in solutions:
            solutions[k].Start_Simulation('DIRECT')

        for k in solutions:
            solutions[k].Wait_For_Simulation_To_End()

    def Select(self):
        for k in self.parents:
            if self.children[k].fitness < self.parents[k].fitness:
                self.parents[k] = copy.deepcopy(self.children[k])

    def Print(self):
        print()
        for k in self.parents:
            print('parent: {}, child: {}'.format(self.parents[k].fitness, self.children[k].fitness))
        print()

    def Show_Best(self):
        best_key = 0
        best_value = 0
        for k in self.parents:
            if self.parents[k].fitness < best_value:
                best_value = self.parents[k].fitness
                best_key = k
        self.parents[best_key].Start_Simulation('GUI')
        

