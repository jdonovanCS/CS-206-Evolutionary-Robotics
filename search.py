import os

for i in range(5):
    os.system("conda activate ER")
    os.system("python generate.py")
    os.system("python simulate.py")