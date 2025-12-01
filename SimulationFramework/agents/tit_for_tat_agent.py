from abstract_agent import AbstractAgent

class TitForTatAgent(AbstractAgent):
    def __init__(self, name):
        super().__init__(name)
        self.first_move = True

    def decide(self, lore):
        if self.first_move:
            self.first_move = False
            return DecisionEnum.COOPERATE
        else:
