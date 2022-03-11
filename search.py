import os
import hillclimber

hc = hillclimber.HILL_CLIMBER()
hc.Evolve()
hc.Show_Best()

# for i in range(5):
#     os.system("conda activate ER")
#     os.system("python generate.py")
#     os.system("python simulate.py")