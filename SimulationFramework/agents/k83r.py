from agents.abstract_agent import AbstractAgent
from enums.choices import DecisionEnum, DescisionTranscript


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
        random.seed(seed)

    def decide(self, opponent_choices: DescisionTranscript) -> DecisionEnum:
        old_state = opponent_choices.get_choice_history()
        if len(old_state) < 5:
            return DecisionEnum.DEFECT
        else:
            counts = 0
            for i in range(5):
                if old_state[-i] == DecisionEnum.COOPERATE:
                    counts+=1
            answer = DecisionEnum.COOPERATE if (counts**2-1)/25 > random.random() else DecisionEnum.DEFECT
            return answer
