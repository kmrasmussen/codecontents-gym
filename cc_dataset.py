# %%
from datasets import load_dataset
import numpy as np
from typing import List, Dict, Any, Generator

class CodeContestsProblem:
    def __init__(self, problem_data: Dict[str, Any], id):
        self.problem_data = problem_data
        self.description = problem_data['description']
        self.python_solution_index = self._find_python_solution_index()
        self.python_solution = self._get_python_solution()
        self.public_tests = self._process_tests('public_tests')
        self.private_tests = self._process_tests('private_tests')
        self.generated_tests = self._process_tests('generated_tests')
        self.difficulty = problem_data['difficulty']
        self.name = problem_data['name']
        self.id = id

    def _find_python_solution_index(self) -> int:
        return next((i for i, lang in enumerate(self.problem_data['solutions']['language']) if lang == 3), None)

    def _get_python_solution(self) -> str:
        if self.python_solution_index is not None:
            return self.problem_data['solutions']['solution'][self.python_solution_index]
        return None

    def _process_tests(self, test_type: str) -> Dict[str, List[str]]:
        try:
            output = self.problem_data[test_type]['output'][0].split('\n')
            input_lines = self.problem_data[test_type]['input'][0].split('\n')
            return {
                'output': [line.strip() for line in output if line.strip()],
                'input': input_lines,
                'input_raw': self.problem_data[test_type]['input'][0]
            }
        except Exception as e:
            #print(f"Error processing {test_type}: {e}")
            return None

    def __repr__(self) -> str:
        return f"CodeContestsProblem(difficulty={self.difficulty}, has_python_solution={self.python_solution is not None})"

class CodeContestsDataset:
    def __init__(self):
        self.dataset = load_dataset("deepmind/code_contests")
        self.train_data = self.dataset['train']

    def get_problems(self) -> Generator[CodeContestsProblem, None, None]:
        for i, problem_data in enumerate(self.train_data):
            #print('dsid', i)
            problem = CodeContestsProblem(problem_data, id=i)
            if problem.python_solution is not None and problem.private_tests is not None and problem.public_tests is not None:
                #print('has python', i)
                yield problem

# Usage example
def main():
    dataset = CodeContestsDataset()
    p_counter = 0
    for i, problem in enumerate(dataset.get_problems()):
        p_counter += 1
        '''
        print(f"Problem {i}:", problem)
        print("Python solution:", problem.python_solution[:100] + "..." if problem.python_solution else "N/A")
        print("Public tests input:", problem.public_tests['input'][:2] if problem.public_tests else "N/A")
        print("Public tests output:", problem.public_tests['output'][:2] if problem.public_tests else "N/A")
        print("Private tests input:", problem.private_tests['input'][:2] if problem.private_tests else "N/A")
        print("Private tests output:", problem.private_tests['output'][:2] if problem.private_tests else "N/A")
        print("Difficulty:", problem.difficulty)
        print("\n" + "="*50 + "\n")
        if i == 0:  # Only print the first problem for demonstration
            break
        '''
        print('p_counter',p_counter)
    print(p_counter)

if __name__ == "__main__":
    main()
# %%
