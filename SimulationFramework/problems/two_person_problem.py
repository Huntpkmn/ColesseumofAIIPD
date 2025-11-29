from problems.abstract_problem import AbstractProblem
from agents.abstract_agent import AbstractAgent, Decision
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

        name_A = self._pa._name
        name_B = self._pb._name
        
        lore = {name_A: [], name_B: []}
        score = {name_A: [], name_B: []}

        for _ in range(self._iters):
            choice_a = self._pa.decide(lore)
            choice_b = self._pb.decide(lore)

            change_A = 0
            change_B = 0

            win_index = 0
            lose_index = 1
            if choice_a == Decision.DEFECT and choice_b == Decision.DEFECT:
                # Both tried to condemn the other. Bad ending.
                change_A = self._dual_condemn_r[win_index]
                change_B += self._dual_condemn_r[lose_index]
            elif choice_a == Decision.COOPERATE and choice_b == Decision.COOPERATE:
                # Both help eachother. Good ending :)
                change_A = self._dual_coop_r[win_index]
                change_B += self._dual_coop_r[lose_index]
            elif choice_a == Decision.DEFECT and choice_b == Decision.COOPERATE:
                # A kills B
                change_A = self._condemn_r[win_index]
                change_B += self._condemn_r[lose_index]
            elif choice_a == Decision.COOPERATE and choice_b == Decision.DEFECT:
                # B kills A
                change_A = self._condemn_r[lose_index]
                change_B += self._condemn_r[win_index]
            else:
                raise ValueError(f"Agent choices must be made using Decision enumeration")

            # apply appropriate score change.
            if len(score[name_A]) == 0:
                a_last_score = 0
                b_last_score = 0
            else:
                a_last_score = score[name_A][-1]
                b_last_score = score[name_B][-1]

            score[name_A].append(a_last_score + change_A)
            score[name_B].append(b_last_score + change_B)

            # record the agents decisions to the lore
            lore[name_A].append(choice_a)
            lore[name_B].append(choice_b)

        # Experiment ended, store events in class.
        self.results_lore = lore
        self.results_score = score
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

        # transcribe events
        output += "~~~~~\n"

        a_moves = self.results_lore[self._pa._name]
        b_moves = self.results_lore[self._pb._name]
        a_score = self.results_score[self._pa._name]
        b_score = self.results_score[self._pb._name]

        output += "round,a_move,b_move,a_score,b_score\n"

        for i, (amvs, bmvs, ascr, bscr) in enumerate(zip(a_moves, b_moves, a_score, b_score)):
            if amvs == Decision.COOPERATE:
                amvs = 'COOPERATE'
            else:
                amvs = 'DEFECT'
            if bmvs == Decision.COOPERATE:
                bmvs = 'COOPERATE'
            else:
                bmvs = 'DEFECT'
            output += f"{i},{amvs},{bmvs},{ascr},{bscr}\n"

        with open('this_will_be_more_descript_later.txt', 'w') as file:
            file.write(output)