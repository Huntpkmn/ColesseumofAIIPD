from agents.abstract_agent import AbstractAgent
from enums.choices import DecisionEnum
import random

class HunterAgent(AbstractAgent):
    """
    The agent is Hunter's, it will cooperate for the first 2 rounds, 
    then defect in the next 3 rounds. If either they betray us
    when we're cooperating or they cooperate for all 5 arounds.
    We will continue to betray with a small chance to go into
    forgive mode where
    """
    states = ["Steal", "Happy", "Revenge"]

    def __init__(self, name, seed=42):
        super().__init__(name)
        object.__setattr__(self,'choices',(DecisionEnum.COOPERATE, DecisionEnum.DEFECT))
        random.seed(seed)
     
        self.othercooperates=0
        self.doublecooperates = 0
        self.otherdefects = 0
        self.doubledefects = 0
        self.recent_cooperates = 0
        self.lastmove = DecisionEnum.COOPERATE
        self.state = ""

    def decide(self, lore):

        old_state = lore.get_choice_history()

        if len(old_state) == 0:
            return DecisionEnum.COOPERATE
        if old_state[-1] == DecisionEnum.COOPERATE:
            if self.lastmove == DecisionEnum.COOPERATE:
                self.doublecooperates +=1
            elif self.lastmove == DecisionEnum.DEFECT:
                self.othercooperates +=1
        elif old_state[-1] == DecisionEnum.DEFECT:
            if self.lastmove == DecisionEnum.COOPERATE:
                self.otherdefects +=1
            elif self.lastmove == DecisionEnum.DEFECT:
                self.doubledefects +=1
            
        if len(old_state) < 2:
            self.lastmove = DecisionEnum.COOPERATE
        elif len(old_state) < 5:
            self.lastmove = DecisionEnum.DEFECT

        elif len(old_state) == 5:
            self.lastmove = DecisionEnum.DEFECT
            if self.othercooperates > 1:
                self.state = "Steal"
            elif self.doublecooperates == 2:
                self.state = "Happy"
            else:
                self.state = "Revenge"

        else:
            match self.state:
                case "Steal":
                    self.lastmove = DecisionEnum.DEFECT
                    if old_state[-1] == DecisionEnum.DEFECT:
                        self.state = "Revenge"
                case "Happy":
                    
                    if old_state[-1] == DecisionEnum.DEFECT:
                        self.state = "Revenge"
                        self.lastmove = DecisionEnum.DEFECT
                    else:
                        self.lastmove = DecisionEnum.COOPERATE
                
                case "Revenge":
                    cooperates = self.doublecooperates+self.othercooperates
                    defects = self.doubledefects+self.otherdefects
                    choice = random.random() > cooperates/(cooperates+defects)
                    if choice:
                        self.state = "Happy"
                    else:
                        self.lastmove = DecisionEnum.DEFECT
                    
        
        return self.lastmove
