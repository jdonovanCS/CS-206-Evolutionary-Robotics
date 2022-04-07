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
        wandb.config.version='deliverable 3'
        wandb.config.population=c.populationSize
    
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
        print('Best Robot Fitness: {}\nBest Robot Num Hidden: {}\nBest Robot Weights:\n\tSensor_to_Hidden: {}\n\tHidden_to Hidden: {}\n\tHidden_to_Motor: {}\n\n'.format(best_value, self.parents[best_key].numHiddenNeurons, self.parents[best_key].s_h_weights, self.parents[best_key].h_rec_weights, self.parents[best_key].h_m_weights))
        self.parents[best_key].Start_Simulation('GUI')
        

