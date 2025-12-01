from agents.abstract_agent import AbstractAgent
from enums.choices import DecisionEnum
from enums.choices import DescisionTranscript

class TitForTatAgent(AbstractAgent):
    def __init__(self, name):
        super().__init__(name)
        self.first_move = True

    def decide(self, other_agents_transcript: DescisionTranscript):
        if self.first_move:
            self.first_move = False
            return DecisionEnum.COOPERATE
        else:
            return other_agents_transcript.get_last_choice()
