from problems.abstract_problem import AbstractProblem
from agents.abstract_agent import AbstractAgent
from enums.choices import DecisionEnum, DescisionTranscript
from pathlib import Path
class TwoPersonProblem(AbstractProblem):

    def __init__(self, iterations, dual_coop_reward, condemn_reward, dual_condemn_reward):
        super().__init__(iterations, dual_coop_reward, condemn_reward, dual_condemn_reward)
        # Score tuple | 0 = winner add value , 1 = loser score add
        self.added_participants = False
        self.completed_experiment = False
        
    def add_participants(self, partnerA:AbstractAgent, partnerB:AbstractAgent):
        if not isinstance(partnerA, AbstractAgent) or not isinstance(partnerB, AbstractAgent):
            raise ValueError("Agents must inherit from class AbstractAgent")
        self._pa = partnerA
        self._pb = partnerB
        self.added_participants = True
        
    def run(self):

        if self.added_participants == False:
            raise ValueError("You must add participants using 'add_participants()'")

        history_a = self._pa.history
        history_b = self._pb.history

        for _ in range(self._iters):
            # Give each agent the history of the other agent.
            choice_a = self._pa.decide(history_b)
            choice_b = self._pb.decide(history_a)

            history_a.record_choice(choice_a)
            history_b.record_choice(choice_b)

            change_A = 0
            change_B = 0
            win_index = 0
            lose_index = 1
            if choice_a == DecisionEnum.DEFECT and choice_b == DecisionEnum.DEFECT:
                # Both tried to condemn the other. Bad ending.
                change_A = self._dual_condemn_r[win_index]
                change_B = self._dual_condemn_r[lose_index]
            elif choice_a == DecisionEnum.COOPERATE and choice_b == DecisionEnum.COOPERATE:
                # Both help eachother. Good ending :)
                change_A = self._dual_coop_r[win_index]
                change_B = self._dual_coop_r[lose_index]
            elif choice_a == DecisionEnum.DEFECT and choice_b == DecisionEnum.COOPERATE:
                # A kills B
                change_A = self._condemn_r[win_index]
                change_B = self._condemn_r[lose_index]
            elif choice_a == DecisionEnum.COOPERATE and choice_b == DecisionEnum.DEFECT:
                # B kills A
                change_A = self._condemn_r[lose_index]
                change_B = self._condemn_r[win_index]
            else:
                raise ValueError(f"Agent choices must be made using DecisionEnum enumeration")
            
            history_a.score_update(change_A)
            history_b.score_update(change_B)

        # Experiment ended, store events in class.
        self.results_a = history_a
        self.results_b = history_b
        self.completed_experiment = True
    
    def export_to_txt(self):

        if self.completed_experiment == False:
            raise ValueError("Must complete an experiment before attemping export!")

        output = str()

        # add metadata
        output += "Two Person Problem\n"
        output += f"Both Defect Cost: {self._dual_condemn_r}\n"
        output += f"Both Cooperate Cost: {self._dual_coop_r}\n"
        output += f"Single defect cost: {self._condemn_r}\n"

        # Record information about the players.
        output += "#####\n"
        output += f"A: {self._pa._name}\n"
        output += f"B: {self._pb._name}\n"

        # determine which agent is the winner.
        a_final_score = self.results_a.get_final_score()
        b_final_score = self.results_b.get_final_score()
        if a_final_score > b_final_score:
            winner = self._pa._name
        elif a_final_score < b_final_score:
            winner = self._pb._name
        else:
            winner = "STALEMATE"
        
        output += f"Winner: {winner}\n"
        output += f"{self._pa._name} final score: {self.results_a.get_final_score()}\n"
        output += f"{self._pb._name} final score: {self.results_b.get_final_score()}\n"
        # transcribe events
        output += "~~~~~\n"

        a_moves = self.results_a.get_choice_history()
        b_moves = self.results_b.get_choice_history()
        a_score = self.results_a.get_score_history()
        b_score = self.results_b.get_score_history()

        output += "round,a_move,b_move,a_score,b_score\n"

        for i, (amvs, bmvs, ascr, bscr) in enumerate(zip(a_moves, b_moves, a_score, b_score)):
            output += f"{i},{amvs},{bmvs},{ascr},{bscr}\n"

        file_name = str()
        folder_name = 'results' + '/'
        file_name += f"two_person_{self._pa._name}_{self._pb._name}_{self._iters}_run1.txt"
        path = Path(folder_name + file_name)

        # find an untaken file path
        counter = 0
        while path.exists():
            counter += 1
            path = path.with_name(f"two_person_{self._pa._name}_{self._pb._name}_{self._iters}_run{counter}.txt")

        with open(path, 'w') as file:
            file.write(output)

        print(f"\nCreated file: {path}")

        return (winner, a_score, b_score)