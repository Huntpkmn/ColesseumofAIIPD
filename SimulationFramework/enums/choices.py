from enum import StrEnum

class DecisionEnum(StrEnum):
        COOPERATE = "COOPERATE",
        DEFECT = "DEFECT"

class DescisionTranscript():
    """
    This class exists to control the flow of information throughout the program.
    """
    def __init__(self):
        self.choices = list()
        self.scores = list()

    def _ledger_check_similar(self):
         """
         Checks the integrity of score and decision ledgers.
         
         :param self: Description
         """
         if abs(len(self.choices) - len(self.scores)) > 1:
              raise ValueError("Score history and decision history are not being updated concurrently." \
              "Make sure that you are using both score_update and record_choice in each loop!")

    def _ledger_check_same(self):
         """
         Makes sure that score and choice history are equal before allowing information out.
         
         """
         if abs(len(self.choices) - len(self.scores)) > 0:
              raise ValueError("Score history and decision history are not being updated concurrently." \
              "Make sure that you are using both score_update and record_choice in each loop!")
        
    def record_choice(self, choice: DecisionEnum):
        if not isinstance(choice, DecisionEnum):
            raise ValueError("Can only submit choices using descision enumeration!")
        else:
            self.choices.append(choice)
        self._ledger_check_similar()

    def score_update(self, change: int):
        if len(self.scores) == 0:
             last = 0
        else:
             last = self.scores[-1]
        last += change
        self.scores.append(last)
        self._ledger_check_similar()

    def get_last_choice(self):
        self._ledger_check_same()
        return self.choices[-1]
    
    def get_final_score(self):
        self._ledger_check_same()
        return self.scores[-1]
    
    def get_choice_history(self):
        self._ledger_check_same()
        return self.choices
    
    def get_score_history(self):
        self._ledger_check_same()
        return self.scores
    
    def get_tuple(self):
        self._ledger_check_same()
        return (self.choices, self.scores)
    
    def is_empty(self):
        if len(self.choices) == 0 or len(self.scores) == 0:
             return True
        else:
             return False
    

    
    