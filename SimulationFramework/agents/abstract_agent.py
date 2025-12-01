from abc import ABC
from enum import Enum

class Decision(Enum):
        COOPERATE = 1,
        DEFECT = 2

class AbstractAgent(ABC):

    def __init__(self, name:str):
        self._name = name
        self.problem = None
    
    def add_problem(self, problem):
         self.problem = problem

    def decide():
        pass
