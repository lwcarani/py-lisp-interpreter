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
symbol_table.update(math.__dict__)


def are_parens_matched_functional(
    t: List[str]
) -> SyntaxError | bool:
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
            f'Input string "{t}" must start and end with open/closed parens.'
        )
    
    d = {'(': 1, ')': -1}
    res = reduce(
        lambda a,b: a+b,
        [d.get(i, 0) for i in t]
    )
    if res != 0:
        raise SyntaxError(
            f'Input string "{t}" contains mismatched parens.'
        )
    else:
        return True
    
def are_parens_matched(
    s: str
) -> SyntaxError | bool:
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
            if not stack or stack.pop() != '(':
                raise SyntaxError(
                    f'Input string "{s}" contains mismatched parens.'
                )

    if len(stack) > 0:
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
    """Generate abstract syntax tree from input tokens."""
    
    t = tokens.pop(0)

    if t == '(':
        ast = []
        while tokens[0] != ')':
            ast.append(generate_ast(tokens))
        tokens.pop(0)  # pop off ')'
        return ast
    elif t == ')':
        raise SyntaxError
    else:
        return atomize(t)
    
def eval(x: Exp, symbol_table: Env = symbol_table):
    if isinstance(x, Number):
        return x
    elif isinstance(x, Symbol):
        return symbol_table.get(x, SyntaxError(f'"{x}" is not a valid symbol'))
    elif x[0] == 'if':
        condition, statement, alternative = x[1:4]
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
    # launch repl env
    while True:
        try: 
            user_input = input("pylist> ")
            # first, validate user input
            # either returns True, or raises SyntaxError
            if are_parens_matched(user_input):
                tokenized_input = tokenize(user_input)
                ast = generate_ast(tokenized_input)
                output = eval(ast)
                # print("User input: ", user_input)
                # print("AST: ", ast)
                print("Final output: ", output)
            
            # print(eval(generate_ast(tokenize(input("pylisp> ")))))
        except EOFError: break
