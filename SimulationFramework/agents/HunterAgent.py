from agents.abstract_agent import AbstractAgent, Decision
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
        object.__setattr__(self,'choices',(Decision.COOPERATE, Decision.DEFECT))
        random.seed(seed)
        self.othercooperates=0
        self.doublecooperates = 0
        self.otherdefects = 0
        self.doubledefects = 0
        self.recent_cooperates = 0
        self.lastmove = Decision.COOPERATE
        self.state = ""

    def decide(self, lore, points):

        old_state = lore[list(set(lore.keys())-set([self._name]))[0]]

        if len(old_state) == 0:
            return Decision.COOPERATE
        if old_state[-1] == Decision.COOPERATE:
            if self.lastmove == Decision.COOPERATE:
                self.doublecooperates +=1
            elif self.lastmove == Decision.DEFECT:
                self.othercooperates
        elif old_state[-1] == Decision.DEFECT:
            if self.lastmove == Decision.COOPERATE:
                self.otherdefects +=1
            elif self.lastmove == Decision.DEFECT:
                self.doubledefects +=1
            
        if len(old_state) < 2:
            self.lastmove = Decision.COOPERATE
        elif len(old_state) < 5:
            self.lastmove = Decision.DEFECT

        elif len(old_state) == 5:
            self.lastmove = Decision.DEFECT
            if self.othercooperates > 2:
                self.state = "Steal"
            elif self.doublecooperates == 2:
                self.state = "Happy"
            else:
                self.state = "Revenge"

        else:
            match self.state:
                case "Steal":
                    self.lastmove = Decision.DEFECT
                    if old_state[-1] == Decision.DEFECT:
                        self.state = "Revenge"
                case "Happy":
                    
                    if old_state[-1] == Decision.DEFECT:
                        self.state = "Revenge"
                        self.lastmove = Decision.DEFECT
                    else:
                        self.lastmove = Decision.COOPERATE
                
                case "Revenge":
                    cooperates = self.doublecooperates+self.othercooperates
                    defects = self.doubledefects+self.otherdefects
                    choice = random.random() > cooperates/(cooperates+defects)
                    if choice:
                        self.state = "Happy"
                    else:
                        self.lastmove = Decision.DEFECT
                    
        
        return self.lastmove
