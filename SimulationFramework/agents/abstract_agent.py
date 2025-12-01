from abc import ABC

class AbstractAgent(ABC):

    def __init__(self, name:str):
        self._name = name
        if len(name) == 0:
            raise ValueError("Name cannot be empty!")

    def decide(self, lore):
        pass