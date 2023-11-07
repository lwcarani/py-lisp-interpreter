import operator as op
import math

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
    'defun': lambda func, args: func(*args),
}
symbol_table.update(math.__dict__)


def tokenize(input: str) -> List:
    """
    Split input string into a list of tokens. Note that we pad
    parentheses with white space before splitting to separate
    parentheses from Atoms (we want ['(', '2'] not ['(2']).

    Example:
    '(+ 1 2)' --> ['(', '+', '1', '2', ')']
    """
    return input.replace('(', ' ( ').replace(')', ' ) ').split()

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
        # TODO - fix this
        func_name, params, func = x[1:4]
        symbol_table[func_name] = lambda *params: eval(func, symbol_table)
        return func_name.upper()
    else:
        op = eval(x[0], symbol_table)
        args = [eval(arg, symbol_table) for arg in x[1:]]
        return op(*args)

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
        try: print(eval(generate_ast(tokenize(input("pylisp> ")))))
        except EOFError: break
