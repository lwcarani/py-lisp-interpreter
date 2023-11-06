import operator as op

Symbol = str
Number = (int, float)
Atom = (Symbol, Number)
List = list
Exp = (Atom, List)
Env = dict

lookup_table = {
    '+': op.add,
    '-': op.sub,
    '*': op.mul,
    '/': op.truediv,
    '<=': op.le,
    '>=': op.ge,
    '!=': op.ne,
    '==': op.eq,
}


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
    
def eval(x: Exp):
    if isinstance(x, Number):
        return x
    elif isinstance(x, Symbol):
        return lookup_table.get(x, SyntaxError(f'"{x}" is not a valid symbol'))
    else:
        op = eval(x[0])
        args = [eval(x[i]) for i in range(1, len(x))]
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
        try: print(generate_ast(tokenize(input("pylisp> "))))
        except EOFError: break
