# %%
from codegen_gym import valid_problem_yielder
# %%
hey = next(valid_problem_yielder())
# %%
print(hey.description)
# %%
from codegen_gym.data import cc_problem_to_llama3_convo
# %%
x = cc_problem_to_llama3_convo(problem=hey)
# %%
x
# %%
print(x)
# %%
