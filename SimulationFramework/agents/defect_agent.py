from agents.constant_agent import ConstantAgent
from enums.choices import DecisionEnum

class DefectAgent(ConstantAgent):

    def __init__(self, name):
        super().__init__(name, DecisionEnum.DEFECT)