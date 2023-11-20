import operator as op
import math
from functools import reduce

Symbol = str
Number = (int, float)
Atom = (Symbol, Number)
List = list
Exp = (Atom, List)
Env = dict

class Env(dict):
    def __init__(self, params=[], args=[], outer: Env = None):
        self.update(zip(params, args))
        self.outer: Env = outer

    def find(self, var):
        if var in self:
            return self[var]
        elif self.outer is not None:
            return self.outer.find(var)
        else:
            raise NameError(f"NameError: name '{var}' is not defined")

global_env: Env = Env()

global_env.update({
    '+': op.add,
    'n': 999
})


def fib(n, env):
    env.update({'n': n})
    if env.find('n') < 2:
        return env.find('n')
    else:
        return fib(env.find('n')-1, Env(env.keys(), env.values(), env)) + fib(env.find('n')-2, Env(env.keys(), env.values(), env))
    

print(fib(8, Env(global_env.keys(), global_env.values(), global_env)))