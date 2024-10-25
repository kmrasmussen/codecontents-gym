# %%
def get_convo_llama3_templated(system_content, user_content, assistant_content):
    return f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{system_content}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{user_content}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n{assistant_content}<|eot_id|>"

def cc_problem_to_llama3_convo(problem):
    system_content = "You are a competitive programming Python bot. The user presents you with the description of a competitive programming problem, and you output Python code that solves the problem."

    user_content = problem.description

    assistant_content = '```python3\n' + problem.python_solution + '\n```'

    convo_llama3_templated = get_convo_llama3_templated(system_content, user_content, assistant_content)
    return convo_llama3_templated