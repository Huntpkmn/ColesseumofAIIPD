import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from by_majority import ByMajorityAgent
from carter_agent import CartersAgent
from constant_agent import ConstantAgent
from HunterAgent import HunterAgent
from k83r import K83R
from MiniMax import MiniMax
from random_agent import RandomAgent
from tit_for_tat_agent import TitForTatAgent
from ZDGTFT2agent import ZDGTFT2

def load_agents():
    #Bad way to do this, but fine for now.
    agents = [ByMajorityAgent(), CartersAgent(), ConstantAgent(),
               HunterAgent(), K83R(), MiniMax(), RandomAgent(), TitForTatAgent(), ZDGTFT2()]
    
    
    return agents
    