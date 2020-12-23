ingestion_dir = 'ingestion_program/'
input_dir = 'sample_data'
agent_dir = 'sample_code_submission/'
output_dir = 'sample_result_submission'
scoring_dir = 'scoring_program/'

from sys import path

path.append(ingestion_dir)
from core import Game
import random
path.append(agent_dir)
from agent import agent, predict

for i in range(0, 500):
    print(i)
    g = Game(random.randint(2,25), random.randint(2,25), i)
    predict(g)

#g = Game(25, 1, 4)
#agent(g)
