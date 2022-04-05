import solution
import constants as c
import copy
import os
import wandb

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system('del \"fitness*.txt\"')
        os.system('del \"brain*.nndf\"')
        os.system('del \"world*.sdf\"')
        os.system('del \"body*.urdf\"')
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(c.populationSize):
            self.parents[i] = solution.SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
        self.currentGeneration=0
        wandb.init('parallel-hill-climber')
        wandb.config.version='quadruped-before-fp'

    def Evolve(self):
        self.Evaluate(self.parents)

        for currentGeneration in range(c.numberOfGenerations):
            self.currentGeneration = currentGeneration
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Record()
        self.Select()

    def Spawn(self):
@@ -57,6 +63,15 @@ def Print(self):
            print('parent: {}, child: {}'.format(self.parents[k].fitness, self.children[k].fitness))
        print()

    def Record(self):
        best_key = 0
        best_value = 0
        for k in self.parents:
            if self.parents[k].fitness < best_value:
                best_value = self.parents[k].fitness
                best_key = k
        wandb.log({'gen': self.currentGeneration, 'best_fitness': best_value, 'num_hidden': self.parents[best_key].numHiddenNeurons})

    def Show_Best(self):
        best_key = 0
        best_value = 0
        for k in self.parents:
            if self.parents[k].fitness < best_value:
                best_value = self.parents[k].fitness
                best_key = k
        self.parents[best_key].Start_Simulation('GUI')
        