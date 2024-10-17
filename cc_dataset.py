# %%
import pyarrow.parquet as pq
import numpy as np

filename = './data/codecontests/train-00001.parquet'
table = pq.read_table(filename)

# %%
df = table.to_pandas()
# %%
def get_tasks_yielder():
    # get tasks where there is a python3 solution
    python3_n = 0
    python3_idx = []
    for i in range(len(df.index)):
        #print(i)
        cc_task = df.iloc[i]
        solution_langs = cc_task['solutions']['language']
        #print(solution_langs)
        if 3 in solution_langs:
            python3_n += 1
            python3_col = np.argwhere(solution_langs == 3)[0][0]
            python3_idx.append({
                "task_id": i,
                'first_python_sol': python3_col
            })
            #print(cc_task['solutions']['solution'][python3_col])
            public_tests = cc_task['public_tests']['output'][0].split('\n')
            stripped_public_tests = [line.strip() for line in public_tests if line != ""]
            public_input_lines = cc_task['public_tests']['input'][0].split('\n')
            
            try:
                private_tests = cc_task['private_tests']['output'][0].split('\n')
                stripped_private_tests = [line.strip() for line in private_tests if line != ""]
                private_input_lines = cc_task['private_tests']['input'][0].split('\n')
            except:
                print('problem with this', cc_task['private_tests'])
                continue
                raise Exception('problem')

            yield_dict = {
                'df_index': i,
                'python3_col': python3_col,
                'df_row': cc_task,
                'python_sol': cc_task['solutions']['solution'][python3_col],
                'public_tests_stripped': stripped_public_tests,
                'public_input_lines': public_input_lines,
                'private_tests_stripped': stripped_private_tests,
                'private_input_lines': private_input_lines,
                'difficulty': cc_task['difficulty']
            }
            yield yield_dict
    print('no more pythons!')