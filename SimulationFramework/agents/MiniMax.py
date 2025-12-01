from agents.abstract_agent import AbstractAgent, Decision
import random
import math

class MiniMax(AbstractAgent):
    """
    MiniMax agent
    """

    def __init__(self, name, depth_limit= 5, seed=42):
        super().__init__(name)
        object.__setattr__(self,'choices',(Decision.COOPERATE, Decision.DEFECT))
        random.seed(seed)
        self.depth_limit = depth_limit
        

    def decide(self, lore):
        old_state = lore[list(set(lore.keys())-set([self._name]))[0]]
        return self.minimax_search(old_state)


    def minimax_search(self,current_state) -> str:
        """
        Start of the Minimax algorithm

        :param current_state: Current state of the game.
        :param game: Game object with operations that are useful for a Minimax search.
        :return: Action to take in the current game state.
        """

        value, action = self.max_value(current_state, 0, float('-inf'), float('+inf'))
        return action

    def max_value(self, current_state, depth: int,
                  alpha: float, beta: float) :
        """
        Recursive function to find the max of possible successors.

        :param current_state: Current state of the game.
        :param game: Game object with operations that are useful for a Minimax search.
        :param depth: Current depth.
        :param alpha: Largest value seen on this path.
        :param beta: Smallest value seen on this path.
        :return: Action to take in the current game state.
        """
        if depth > self.depth_limit:
            return [game.utility(current_state, self.player), ""]
        v = -math.inf
        for a in self.choices:
            v2, a2 = self.min_value(self.problem.calculate_point(current_state, a), depth + 1, alpha, beta)
            # print(v2,a2)
            if v2 > v:

                v, move = v2, a
                alpha = max(alpha,v)
                # print(f"{v} action:{a2}")
            if v >= beta:
                return [v, move]

        return [v, move]



    def min_value(self, current_state, depth: int,
                  alpha: float, beta: float):
        """
        Recursive function to find the min of possible successors.

        :param current_state: Current state of the game.
        :param game: Game object with operations that are useful for a Minimax search.
        :param depth: Current depth.
        :param alpha: Largest value seen on this path.
        :param beta: Smallest value seen on this path.
        :return: Action to take in the current game state.
        """
        if depth > self.depth_limit:
            return [game.utility(current_state, self.player), ""]
        v = math.inf
        for a in self.choices:
            v2, a2 = self.max_value(self.calculate_point(current_state, a), depth + 1, alpha, beta)
            # print(v2,a2)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
                # print(f"{v} action:{a2}")
            if v <= alpha:
                return [v, move]

        return [v, move]

