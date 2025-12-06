import os
import importlib.util
import inspect
import itertools
from agents.abstract_agent import AbstractAgent
from problems.two_person_problem import TwoPersonProblem
from typing import Generator

def import_classes_from_directory(directory: str = 'agents') -> list[type[AbstractAgent]]:
    """
    Search evreyfile in given folder for python classes and create
    
    :param directory: Name of folder to search through.
    :type directory: str
    :return: A list of class types found in the folder provided.
    :rtype: list[AbstractAgent]
    """
    ignore_these_files = {'abstract_agent.py', 'mlp_agent.py', 'constant_agent.py'}
    classes = list()
    for filename in os.listdir(directory):
        if filename.endswith('.py') and filename not in ignore_these_files: # Don't try to make an abstract agent.
            module_name = filename[:-3]  # strip .py
            module_path = os.path.join(directory, filename)

            # Search for every module in the subfolder.
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Inspect module members and collect classes found in each module (should be one per module).
            for name, obj in inspect.getmembers(module, inspect.isclass):
                # Check if the class is defined in this module (not imported)
                # This step makes sure only a class that is defined within the file.
                if obj.__module__ == module_name:
                    classes.append(obj)
    return classes


def create_round_robin_matchups(all_agents: list[type[AbstractAgent]]) -> Generator[tuple[type[AbstractAgent], type[AbstractAgent]], None, None]:
    """
    This method creates a generator to test every combination of two agents.
    
    :param all_agents: The list containing the type() of each agent found in the file heirarchy.
    :type all_agents: list[type[AbstractAgent]]
    :return: A reference to a generator yielding every combination of agent types.
    :rtype: Generator[tuple[type[AbstractAgent], type[AbstractAgent]]]]
    """
    return itertools.combinations(all_agents, 2)

def run_experiments(
        matchups: Generator[tuple[type[AbstractAgent], type[AbstractAgent]], None, None],
        scores: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
        i: int = 10
                    ):
    """
    This method runs a two_person_problem() for every combination of agents found and retuns the collection of results.
    
    :param matchups: Reference to generator producing Agent type() combinations.
    :type matchups: Generator[tuple[type[AbstractAgent], type[AbstractAgent]]]
    :return: A list of all of the returned victors and scores of the run experiments.
    :rtype: list[tuple[str, int, int]]
    """
    results = {}
    for type_a, type_b in matchups:
        dual_cooperation, defect_cooperation, dual_defect = scores
        problem = TwoPersonProblem(i, dual_cooperation, defect_cooperation, dual_defect)
        problem.add_participants(type_a(type_a.__name__), type_b(type_b.__name__))
        results[(type_a.__name__, type_b.__name__)] = problem.run()
    return results

classes = import_classes_from_directory()
gen = create_round_robin_matchups(classes)
dual_cooperation = (3,3)
defect_cooperation = (5,0)
dual_defect = (0,0)
out = run_experiments(gen, (dual_cooperation, defect_cooperation, dual_defect))

print(out)
        