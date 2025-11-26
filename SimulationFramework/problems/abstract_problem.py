from abc import ABC

class AbstractProblem(ABC):
    def __init__(self, iterations:int, dual_coop_reward: list[int, int], condemn_reward: list[int, int], dual_condemn_reward: list[int, int]):
        """
        Rewards should be in format (reward for winner, reward for loser)
        """
        self._iters = iterations
        self._dual_coop_r = dual_coop_reward
        self._condemn_r = condemn_reward
        self._dual_condemn_r = dual_condemn_reward
        self.added_participants = False
        for score in (self._condemn_r, self._dual_condemn_r, self._dual_coop_r):
            if len(score) != 2:
                raise ValueError(f"Problem reward {score} must be in form (int, int)")
            for i in score:
                if not isinstance(i, int):
                    raise ValueError(f"Problem reward can only contain int, not {type(i)}")

    def add_participants(self):
        "Use this method to add some agents to this problem."
        pass

    def run(self):
        "Use this method to run your problem as you have configured it"
        if self.added_participants == False:
            raise ValueError("You must implement and use 'add_participants()' before running an experiment!")

    def export_to_txt():
        """
        The problem should record what happens step by step,
        use this method to turn that play-by-play into a txt file export
        """
        pass