import random
from agents.abstract_agent import AbstractAgent
from enums.choices import DecisionEnum, DescisionTranscript

class RandomAgent(AbstractAgent):
    """
    Example of a simple agent that makes a random choice between defecting or cooperating.
    """

    def __init__(self, name, seed=42):
        super().__init__(name)
        object.__setattr__(self,'choices',(DecisionEnum.COOPERATE, DecisionEnum.DEFECT))
        random.seed(seed)

    def decide(self, opponent_choices: DescisionTranscript) -> DecisionEnum:
        return random.choice(self.choices)