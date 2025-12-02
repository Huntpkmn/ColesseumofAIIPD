from agents.abstract_agent import AbstractAgent
from enums.choices import DecisionEnum
from enums.choices import DescisionTranscript

class TitForTatAgent(AbstractAgent):
    def __init__(self, name):
        super().__init__(name)
        self.first_move = True

    def get_history(self):
        return super().get_history()

    def decide(self, opponent_choices: DescisionTranscript) -> DecisionEnum:
        if self.first_move:
            self.first_move = False
            return DecisionEnum.COOPERATE
        else:
            return opponent_choices.get_last_choice()
