from agents.abstract_agent import AbstractAgent
from enums.choices import DecisionEnum, DescisionTranscript

class ByMajorityAgent(AbstractAgent):
    def __init__(self, name):
        super().__init__(name)

    def get_history(self):
        return super().get_history()

    def decide(self, other_agents_history: DescisionTranscript):
        count_d = other_agents_history.get_choice_history().count(DecisionEnum.DEFECT)
        count_c = other_agents_history.get_choice_history().count(DecisionEnum.COOPERATE)
        if count_d >= count_c:
            return DecisionEnum.DEFECT
        else:
            return DecisionEnum.COOPERATE