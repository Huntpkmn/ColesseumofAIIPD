from abstract_agent import AbstractAgent, Decision
import random

class RandomAgent(AbstractAgent):
    """
    Example of a simple agent that makes a random choice between defecting or cooperating.
    """

    def __init__(self, name, seed=42):
        super().__init__(name)
        object.__setattr__(self,'choices',(Decision.COOPERATE, Decision.DEFECT))
        random.seed(seed)

    def __setattr__(self, *args):
        raise TypeError("Cannot modify immutable object")
    
    def __delattr__(self, *args):
        raise TypeError("Cannot delete attributes")

    def decide(self):
        return random.choice(self.choices)