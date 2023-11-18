import operator as op
import math
from functools import reduce

Symbol = str
Number = (int, float)
Atom = (Symbol, Number)
List = list
Exp = (Atom, List)
Env = dict

symbol_table: Env = {
    '+': op.add,
    '-': op.sub,
    '*': op.mul,
    '/': op.truediv,
    '<=': op.le,
    '<': op.lt,
    '>': op.gt,
    '>=': op.ge,
    '!=': op.ne,
    '==': op.eq,
}
# add standard math library operators to symbol_table
symbol_table.update(math.__dict__)


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
    
def eval(x: Exp, symbol_table: Env = symbol_table):
    if isinstance(x, Number):
        return x
    elif isinstance(x, Symbol):
        return symbol_table.get(x, SyntaxError(f'"{x}" is not a valid symbol'))
    elif x[0] == 'if':
        condition, statement, alternative = x[1:4]

        # TODO - delete below
        if eval(condition, symbol_table):
            print('here')
        expression = statement if eval(condition, symbol_table) else alternative
        return eval(expression, symbol_table)
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
        symbol_table[func_name] = (params, func_body)
        return f"Defined function: {func_name.upper()}"
    elif x[0] == 'format':
        if isinstance(x[-1], list):
            fill_val = eval(x[-1], symbol_table)
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
        func = eval(x[0], symbol_table)
        args = [eval(arg, symbol_table) for arg in x[1:]]

        if isinstance(func, tuple):
            params, func_body = func
            if len(args) != len(params):
                raise ValueError(
                    f'Function "{func_name}" expects {len(params)} arguments, but {len(args)} were provided.'
                )
            symbol_table.update(zip(params, args))
            return eval(func_body, symbol_table)
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

    ### read lisp script from txt file
    # user_input = ""

    # file_path = 'test_script.txt'
    # with open(file_path, 'r') as file:
    #     lines = file.readlines()

    # # Now 'lines' is a list where each element is a line from the file
    # for line in lines:
    #     user_input += line.strip()
    #     try:
    #         if are_parens_matched_map_reduce(user_input):
    #             print(eval(generate_ast(tokenize(user_input))))
    #             user_input = ""
    #     except:
    #         continue

    # TODO - write fib function in pure python to make sure its implemented correctly, then re-visit the below

    # launch repl env
    while True:
        print(eval(generate_ast(tokenize("(defun fib (n)  (if (< n 2)      n      (+ (fib (- n 1))         (fib (- n 2)))))"))))
        print(eval(generate_ast(tokenize("(fib 5)"))))
        
        try: 
            user_input = input("pylisp> ")
            # first, validate user input
            # either returns True, or raises SyntaxError
            if are_parens_matched_map_reduce(user_input):
                print(eval(generate_ast(tokenize(user_input))))
        except EOFError: break

