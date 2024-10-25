from .data.cc_dataset import CodeContestsDataset, CodeContestsProblem
from .pythongym import execute_code_with_input as execute_code_string

def eval_problem(problem: CodeContestsProblem, tests_type='public_tests', pol=False):
    if tests_type == 'public_tests':
        tests = problem.public_tests
    elif tests_type == 'private_tests':
        tests = problem.private_tests
    else:
        raise ValueError(f'Unknown tests type: {tests_type}')

    if pol: print('Running problem')
    output, stderr_output, result_returncode = execute_code_string(
        problem.python_solution,
        tests['input_raw']
    )
    if pol:
        print('Output:', repr(output))
        print('Stderr output:', stderr_output)
        print('Done running problem')
        print('public tests', repr(tests['input_raw']))

    captured_processed = output.strip().lower()
    if pol: print('Captured output repr:', repr(captured_processed))
    expected_processed = '\n'.join(tests['output']).strip().lower()
    if pol: print('Expected:', repr(expected_processed))

    captured_processed_lines = [line.strip() for line in captured_processed.split('\n') if line != ""]
    if pol: print("Captured output lines:", captured_processed_lines)
    expected_processed_lines = [line.strip() for line in expected_processed.split('\n') if line != ""]

    n_correct_lines = 0
    for y_pred, y_true in zip(captured_processed_lines, expected_processed_lines):
        # Split the lines into words and compare
        y_pred_words = y_pred.split()
        y_true_words = y_true.split()
        if y_pred_words == y_true_words:
            n_correct_lines += 1
        else:
            if pol: 
                print(f"Expected: {y_true}")
                print(f"Got: {y_pred}")
                print()
    if pol: print('Correct lines:', n_correct_lines, '/', len(expected_processed_lines))
    if n_correct_lines != len(expected_processed_lines):
        if pol:
            print('Source:', problem.problem_data['source'])
            print('Public tests failed')
        return False

    return True

def valid_problem_yielder(difficulty=None, eval_test=True):
    dataset = CodeContestsDataset()
    for problem_i, problem in enumerate(dataset.get_problems()):
        if difficulty is not None and problem.difficulty != difficulty:
            continue
        
        if eval_test:
            public_result = eval_problem(problem, tests_type='public_tests')
            if public_result == False:
                continue

            private_result = eval_problem(problem, tests_type='private_tests')
            if private_result == False:
                continue
        
        yield problem

def main():
    works_idx = []
    for problem_i, problem in enumerate(valid_problem_yielder()):
        #print(problem)
        works_idx.append(problem.id)
    print(works_idx)
    '''
    dataset = CodeContestsDataset()
    
    n_works = 0
    
    pol = False
    works_names = []
    works_idx = []
    not_works_idx = []
    not_works_names = []
    for problem_i, problem in enumerate(dataset.get_problems()):
        if pol:
            print('YIELD', problem_i)
            print('name', problem.name)
            print('Code:')
            print(problem.python_solution)
            print('Input:')
            print(repr(problem.public_tests['input'][0]))
            print('Problem index:', problem_i)
        print('Problem', problem_i)
            
        public_result = eval_problem(problem, tests_type='public_tests')
        if public_result == False:
            not_works_idx.append(problem_i)
            not_works_names.append(problem.name)
            continue

        private_result = eval_problem(problem, tests_type='private_tests')
        if private_result == False:
            not_works_idx.append(problem_i)
            not_works_names.append(problem.name)
            continue

        works_idx.append(problem_i)
        works_names.append(problem.name)
        n_works += 1
        print('NWORKS', n_works)
    print('last name', problem.name)
    #print('problem is with', problem_is_with)
    print('Works:', len(works_idx), works_idx)
    print('Not works:', len(not_works_idx), not_works_idx)
    '''

if __name__ == "__main__":
    main()