import inquirer
from enum import Enum
import operator as op
import math
from functools import reduce

Symbol = str
Number = (int, float)
Atom = (Symbol, Number)
List = list
Exp = (Atom, List)
Env = dict

class Mode(Enum):
    FILE = 'file'
    REPL = 'REPL'

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
    '-': op.sub,
    '*': op.mul,
    '/': op.truediv,
    '<=': op.le,
    '<': op.lt,
    '>': op.gt,
    '>=': op.ge,
    '!=': op.ne,
    '=': op.eq,
})
# add standard math library operators to symbol_table
global_env.update(math.__dict__)


def are_parens_matched_stack(
    s: str
) -> SyntaxError | bool:
    """
    Iterate over entire input string, using a stack to keep track of open
    and closed parens. 
    """
    stack = []

    if len(s) == 0:
        raise SyntaxError(
            f'Input string cannot be empty.'
        )
    # make sure that user input starts and end with open/close parens
    elif (
        s[0] != '('
        or s[-1] != ')'
    ):
        raise SyntaxError(
            f'Input string "{s}" must start and end with open/closed parens.'
        )
    
    for char in s:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if (
                len(stack) == 0 
                or stack.pop() != '('
            ):
                raise SyntaxError(
                    f'Input string "{s}" contains mismatched parens.'
                )

    if len(stack) > 0:
        raise SyntaxError(
            f'Input string "{s}" contains mismatched parens.'
        )
    else:
        return True
    
def are_parens_matched_map_reduce(
    s: str
) -> SyntaxError | bool:
    """
    A more functional approach to checking that all parens are matching.
    Uses built-in Python `map` and `reduce` functions.
    """
    t = tokenize(s)
    if len(t) == 0:
        raise SyntaxError(
            f'Input string cannot be empty.'
        )
    # make sure that user input starts and end with open/close parens
    elif (
        t[0] != '('
        or t[-1] != ')'
    ):
        raise SyntaxError(
            f'Input string "{s}" must start and end with open/closed parens.'
        )
    
    ### transform-reduce
    # transform (map) open parens to 1, close parens to -1,
    # and all other chars to 0, then sum the resulting iterator
    # if all parens are matched, res will be 0, otherwise, throw
    # a SyntaxError, because there are mismatched parens
    d = {'(': 1, ')': -1}
    res = reduce(
        lambda a,b: a+b,
        map(lambda x: d.get(x, 0), t)
    )
    if res != 0:
        raise SyntaxError(
            f'Input string "{s}" contains mismatched parens.'
        )
    else:
        return True

def tokenize(input: str) -> List[str]:
    """
    Split input string into a list of tokens. Note that we pad
    parentheses with white space before splitting to separate
    parentheses from Atoms (we want ['(', '2'] not ['(2']).

    Example:
    '(+ 1 2)' --> ['(', '+', '1', '2', ')']
    """
    tokenized_input: List[str] = input.replace('(', ' ( ').replace(')', ' ) ').split()
    # print("Tokenized input: ", tokenized_input)
    return tokenized_input

def generate_ast(tokens: List) -> List:
    """
    Generate abstract syntax tree from input tokens.
    
    Example: 
    tokenized_input = ['(', 'defun', 'doublen', '(', 'n', ')', '(', '*', 'n', '2', ')', ')']
    -->
    ast = ['defun', 'doublen', ['n'], ['*', 'n', 2]]
    """
    t = tokens.pop(0)

    if t == '(':
        ast = []
        while tokens[0] != ')':
            ast.append(generate_ast(tokens))
        tokens.pop(0)  # pop off ')'
        return ast
    elif t == ')':
        raise SyntaxError('Mismatched parens.')
    else:
        return atomize(t)
    
def eval(x: Exp, env: Env = global_env):
    if isinstance(x, Number):
        return x
    elif isinstance(x, Symbol):
        return env.find(x)
    elif x[0] == 'if':
        condition, statement, alternative = x[1:4]
        expression = statement if eval(condition, Env(env.keys(), env.values(), env)) else alternative
        return eval(expression, Env(env.keys(), env.values(), env))
    elif x[0] == 'defun':
        # `func_name`: str
        # `params`: List[str]
        # `func_body`: List
        # Example:
        #   "(defun doublen (n) (* 2 n))" --> 
        #   `func_name`: "doublen"
        #   `params`: ["n"]
        #   `func_body`: ["*", 2, "n"]
        func_name, params, func_body = x[1:4]
        env[func_name] = (params, func_body)
        return f"Defined function: {func_name.upper()}"
    elif x[0] == 'format':
        if isinstance(x[-1], list):
            fill_val = eval(x[-1], Env(env.keys(), env.values(), env))
            res = " ".join(str(i) for i in x[2:-1])
        else:
            fill_val = ""
            res = " ".join(str(i) for i in x[2:])
        if '~D~%' in res:
            res = res.replace("\"", "").replace('~D~%', str(fill_val))
        else:
            res = res.replace("\"", "").replace('~%', str(fill_val))
        return res
    else:
        func_name = x[0]
        func = eval(x[0], Env(env.keys(), env.values(), env))
        args = [eval(arg, Env(env.keys(), env.values(), env)) for arg in x[1:]]

        if isinstance(func, tuple):
            params, func_body = func
            if len(args) != len(params):
                raise ValueError(
                    f'Function "{func_name}" expects {len(params)} arguments, but {len(args)} were provided.'
                )
            env.update(zip(params, args))
            return eval(func_body, Env(env.keys(), env.values(), env))
        else:
            return func(*args)

def atomize(token: str) -> Atom:
    """
    Atomize input tokens. Every token is either an int, float, or Symbol.
    
    Note that
        Symbol := str
        Number := (int, float)
        Atom   := (Symbol, Number)
    """
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)

if __name__ == '__main__':
    questions = [
        inquirer.List(
            name='mode',
            message="Would you like to open the REPL environment, or execute a file?",
            choices=[m.value for m in Mode]
        ),
    ]
    mode = inquirer.prompt(questions)['mode']

    if mode == Mode.REPL.value:
        ### launch REPL env
        while True:            
            try: 
                user_input = input("pylisp> ")
                # first, validate user input
                # either returns True, or raises SyntaxError
                if are_parens_matched_map_reduce(user_input):
                    print(eval(generate_ast(tokenize(user_input))))
            except EOFError: break
    elif mode == Mode.FILE.value:
        ### read lisp script from txt file
        while True:
            input_file = input('Enter the location of the file: ')
            with open(input_file, 'r') as file:
                lines = file.readlines()

            user_input = ""
            for line in lines:
                user_input += line.strip()
                if len(user_input) > 0:
                    try:
                        if are_parens_matched_map_reduce(user_input):
                            print(eval(generate_ast(tokenize(user_input))))
                            user_input = ""
                    except Exception as e:
                        continue
                else:
                    continue

            continue_yes_no = [
                inquirer.List(
                    name='cont',
                    message="Would you like to execute another file?",
                    choices=['Yes', 'No']
                ),
            ]
            ans = inquirer.prompt(continue_yes_no)['cont']

            match ans:
                case 'Yes':
                    continue
                case 'No':
                    break
                case _:
                    break
