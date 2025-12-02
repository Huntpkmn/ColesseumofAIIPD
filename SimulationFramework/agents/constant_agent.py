from agents.abstract_agent import AbstractAgent
from enums.choices import DecisionEnum, DescisionTranscript

class ConstantAgent(AbstractAgent):
    """
    This class can be configured to always make a given choice.
    IE Always defect or always cooperate.
    """

    def __init__(self, name: str, behaviour: DecisionEnum):
        """
        This class need to be configured for its constant behvaiour.
        
        :param self: This class.
        :param name: Identifier for this class. Used during simulation and transcription generation.
        Make it descriptive!
        :type name: str
        :param behaviour: The descision that this agent will always take.
        :type behaviour: DecisionEnum
        """
        super().__init__(name)
        if not isinstance(behaviour, DecisionEnum):
            raise ValueError("Agent decisions must be configured using descision enumeration!")
        self._behav = behaviour

    def decide(self, opponent_choices: DescisionTranscript) -> DecisionEnum:
        """
        Return agents action for this turn.

        :param opponent_choices: Ignored 
        """
        return self._behav