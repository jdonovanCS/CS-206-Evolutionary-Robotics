import os
import parallelHillClimber


phc = parallelHillClimber.PARALLEL_HILL_CLIMBER()
phc.Evolve()
phc.Show_Best()


# hc = hillclimber.HILL_CLIMBER()
# hc.Evolve()
# hc.Show_Best()

# for i in range(5):
#     os.system("conda activate ER")
#     os.system("python generate.py")
#     os.system("python simulate.py")