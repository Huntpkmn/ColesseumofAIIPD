from agents.random_agent import RandomAgent
from problems.two_person_problem import TwoPersonProblem


iters = 10
dcoop = (3,3)
dfct = (5,0)
ddfct = (1,1)
prob = TwoPersonProblem(iters, dcoop, dfct, ddfct)
prob.add_participants(RandomAgent('a'), RandomAgent('b'))
prob.run()
prob.export_to_txt()