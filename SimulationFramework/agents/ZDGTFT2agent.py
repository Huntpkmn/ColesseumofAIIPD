from agents.abstract_agent import AbstractAgent
from enums.choices import DecisionEnum
from enums.choices import DescisionTranscript
import random

class ZDGTFT2(AbstractAgent):
    def __init__(self, name):
        super().__init__(name)

    def decide(self, other_agents_transcript: DescisionTranscript):
        size = len(other_agents_transcript.get_choice_history())
        
        if size == 0:
            return DecisionEnum.COOPERATE
        else:
            last_move = other_agents_transcript.get_last_choice()
            if last_move == DecisionEnum.COOPERATE:
                return DecisionEnum.COOPERATE
            else:
                chance = 1/8 if self.history.get_last_choice() == DecisionEnum.COOPERATE else 1/4
                return DecisionEnum.COOPERATE if random.random() < chance else DecisionEnum.DEFECT
