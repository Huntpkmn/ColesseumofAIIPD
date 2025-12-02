from abc import ABC
from enums.choices import DescisionTranscript, DecisionEnum
from problems.abstract_problem import AbstractProblem

class AbstractAgent(ABC):

    def __init__(self, name:str):
        """
        This method enforces the collection of the minimum information needed for simulation to run.
        """
        self._name = name
        self.problem = None
        self.history = DescisionTranscript()
        if len(name) == 0:
            raise ValueError("Name cannot be empty!")
    
    def get_history(self) -> DecisionEnum:
        """
        Returns a ledger to this instances internal score and decision ledger.
        """
        return self.history
 
    def set_problem(self, problem: AbstractProblem):
        """
        This method is used to provide a reference of the problem this agent is currently being simulated in.
        This is here so that, if desired, an agent can generate a look ahead datastructure using the problems
        own score assesment method.

        IE an agent can calulate future scores using the same math the problem is using to generate score changes.

        ## Most agents will not need to use this.
        """
        self.problem = problem

    def decide(self, opponent_choices: DescisionTranscript) -> DecisionEnum:
        """
        This is how an agent submits its cooperate or defect descision each round.

        ## AbstractAgents version of this method does not have to be run.
        """
        pass