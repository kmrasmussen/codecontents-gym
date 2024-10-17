from cc_dataset import get_tasks_yielder
#from pygym4 import execute_code_string
from neogym1 import execute_code_with_input as execute_code_string

def eval_task(task):
    print('running task')
    output, stderr_output, result_returncode = execute_code_string(
    #output, stderr_output, final_namespace, trace_info, trace_store = execute_code_string(
        task['python_sol'],
        task['df_row']['public_tests']['input'][0]
    )
    print('output', output)
    print('stderr_output', stderr_output)
    print('done running task')

    captured_processed = output.strip().lower()
    print('captured output repr', repr(captured_processed))
    expected_processed = task['df_row']['public_tests']['output'][0].strip().replace('\r\n', '\n').lower()
    print('expected', repr(expected_processed))

    captured_processed_lines = [line.strip() for line in captured_processed.split('\n') if line != ""]
    print("Captured output lines:", captured_processed_lines)
    expected_processed_lines = [line.strip() for line in expected_processed.split('\n') if line != ""]

    n_correct_lines = 0
    for y_pred, y_true in zip(captured_processed_lines, expected_processed_lines):
        # Split the lines into words and compare
        y_pred_words = y_pred.split()
        y_true_words = y_true.split()
        if y_pred_words == y_true_words:
            n_correct_lines += 1
        else:
            print(f"Expected: {y_true}")
            print(f"Got: {y_pred}")
            print()
    print('n correct', n_correct_lines, '/', len(expected_processed_lines))
    if n_correct_lines != len(expected_processed_lines):
        print('source',task['df_row']['source'])
        print('public tests failed')
        return False

    return True

tasks_yielder = get_tasks_yielder()

black_list = [22,2,28,48,54,73,78,79,80,81,88,98,104,105,118,124,128]
# 105 - decimal precision
# 124 - permutation
# 128 - dec prec
n_works = 0
works_idx = []
for task_i, task in enumerate(tasks_yielder):
    if task_i in black_list:
        continue
    #if task_i < 13: continue
    print('YIELD', task_i)
    print('code:')
    print(task['python_sol'])
    print('in')
    print(repr(task['df_row']['public_tests']['input'][0]))
    print('task_i', task_i)
    result = eval_task(task)
    if result == False:
        break
    works_idx.append(task_i)
    n_works += 1
    print('NWORKS', n_works)
print('works', len(works_idx), works_idx)