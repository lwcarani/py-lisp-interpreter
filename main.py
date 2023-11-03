Symbol = str
Number = (int, float)
Atom = (Symbol, Number)
List = list
Exp = (Atom, List)
Env = dict

def tokenize(input: str) -> List:
    """
    Split input string into a list of tokens. Note that we pad
    parentheses with white space before splitting to separate
    parentheses from Atoms.

    Example:
    '(+ 1 2)' --> ['+', '1', '2']
    """
    return input.replace('(', ' ( ').replace(')', ' ) ').split()


def parse(tokens: list) -> list:
    # for t in tokens:
    #     pass
    return tokens

def atomize(token: str) -> Atom:
    """
    Atomize input tokens. Every token is either an int, float, or Symbol.
    
    Note that
        Symbol := str
        Number := (int, float)
        Atom := (Symbol, Number)
    """
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)


if __name__ == '__main__':
    while True:
        try: print(parse(tokenize(input("pylisp> "))))
        except EOFError: break