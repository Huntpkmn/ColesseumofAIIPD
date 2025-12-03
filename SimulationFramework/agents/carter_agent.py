from agents.abstract_agent import AbstractAgent
from agents.tit_for_tat_agent import TitForTatAgent
from enums.choices import DecisionEnum, DescisionTranscript
from enum import Enum

class CartersAgent(AbstractAgent):

    class Mood(Enum):
        INDIFFERENT = 1,
        HATRED = 2,
        FRIENDSHIP = 3,
        UNINIT = 4

    def __init__(self, name):
        super().__init__(name)
        self.feels = self.Mood.INDIFFERENT
        self.first = True
        self.second = True
        self.start_up = True

    def get_history(self):
        return super().get_history()
    
    def set_problem(self, problem):
        return super().set_problem(problem)
    
    def decide(self, opponent_choices: DescisionTranscript) -> DecisionEnum:
        if self.start_up:
            if self.first:
                self.first = False
                return DecisionEnum.COOPERATE
            elif self.second:
                self.second = False
                return DecisionEnum.DEFECT
            else:
                # start up is over, assess opponent.
                self.start_up = False
                other = opponent_choices.get_choice_history()
                if other[0] == DecisionEnum.COOPERATE and other[1] == DecisionEnum.DEFECT:
                    # It looks like you went out of your way to defect after I tried to cooperate. >:(
                    self.feels = self.Mood.HATRED
                elif other[0] == DecisionEnum.DEFECT and other[1] == DecisionEnum.COOPERATE:
                    # You might try to take advantage of my kindness.
                    self.feels = self.Mood.INDIFFERENT
                elif other[0] == DecisionEnum.COOPERATE and other[1] == DecisionEnum.COOPERATE:
                    self.feels = self.Mood.FRIENDSHIP
                else:
                    self.feels = self.Mood.HATRED
        else:
            if self.feels == self.Mood.HATRED:
                return DecisionEnum.DEFECT
            elif self.feels == self.Mood.FRIENDSHIP:
                return DecisionEnum.COOPERATE
            elif self.feels == self.Mood.INDIFFERENT:
                return opponent_choices.get_last_choice()
            else:
                raise ValueError("How did you get here?")