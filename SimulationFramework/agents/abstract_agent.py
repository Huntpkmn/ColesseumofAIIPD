from abc import ABC
from enums.choices import DescisionTranscript

class AbstractAgent(ABC):

    def __init__(self, name:str):
        self._name = name
        self.problem = None
        self.history = DescisionTranscript()
        if len(name) == 0:
            raise ValueError("Name cannot be empty!")
    
    def get_history(self):
        return self.history
 
    def decide(self, lore):
        pass