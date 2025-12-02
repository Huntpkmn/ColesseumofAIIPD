from agents.constant_agent import ConstantAgent
from problems.two_person_problem import TwoPersonProblem
from agents.tit_for_tat_agent import TitForTatAgent
from agents.MiniMax import MiniMax
from enums.choices import DecisionEnum


iters = 10
dual_cooperation = (3,3)
defect_cooperation = (5,0)
dual_defect = (1,1)
problem = TwoPersonProblem(iters, dual_cooperation, defect_cooperation, dual_defect)
problem.add_participants(ConstantAgent('evil-hugh', DecisionEnum.DEFECT), MiniMax('minimax'))
problem.run()
problem.export_to_txt()