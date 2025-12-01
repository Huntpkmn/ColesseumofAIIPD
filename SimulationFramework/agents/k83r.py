from agents.abstract_agent import AbstractAgent, Decision
import random

class K83R(AbstractAgent):
    """
    The agent is K83R, it will defect for the first 5 rounds, 
    then will randomly forgive depending on how many times the 
    opponent was cooperative in the past 5 moves based on 
    probability of (num_times_cooperated^2-1)/25.
    """

    def __init__(self, name, seed=42):
        super().__init__(name)
        object.__setattr__(self,'choices',(Decision.COOPERATE, Decision.DEFECT))
        random.seed(seed)

    def decide(self, lore):
        old_state = lore[list(set(lore.keys())-set([self._name]))[0]]
        if len(old_state) < 5:
            return Decision.DEFECT
        else:
            counts = 0
            for i in range(5):
                if old_state[-i] == Decision.COOPERATE:
                    counts+=1
            answer = Decision.COOPERATE if (counts**2-1)/25 > random.random() else Decision.DEFECT
            return answer
