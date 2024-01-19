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


class Mode(Enum):
    FILE = "file"
    REPL = "REPL"


class SymbolTable(dict):
    def __init__(self, params=[], args=[], outer_scope=None):
        self.update(zip(params, args))
        self.outer_scope = outer_scope

    # def __call__(self, outer_scope)
    #     self.outer_scope = outer_scope

    def find(self, var):
        if var in self:
            return self[var]
        elif self.outer_scope is not None:
            return self.outer_scope.find(var)
        else:
            raise NameError(f"NameError: name '{var}' is not defined")


global_symbol_table = SymbolTable()
global_symbol_table.update(
    {
        "+": op.add,
        "-": op.sub,
        "*": op.mul,
        "/": op.truediv,
        "<=": op.le,
        "<": op.lt,
        ">": op.gt,
        ">=": op.ge,
        "!=": op.ne,
        "=": op.eq,
    }
)
# add standard math library operators to symbol_table
global_symbol_table.update(math.__dict__)


def are_parens_matched_stack(s: str) -> SyntaxError | bool:
    """
    Iterate over input string, using a stack
    to keep track of open and closed parens.
    """
    stack = []

    if len(s) == 0:
        raise SyntaxError(f"Input string cannot be empty.")
    # make sure that user input starts and end with open/close parens
    elif s[0] != "(" or s[-1] != ")":
        raise SyntaxError(
            f'Input string "{s}" must start and end with open/closed parens.'
        )

    for char in s:
        if char == "(":
            stack.append(char)
        elif char == ")":
            if len(stack) == 0 or stack.pop() != "(":
                raise SyntaxError(f'Input string "{s}" contains mismatched parens.')

    # stack should be empty at this point, if not, throw error
    if len(stack) > 0:
        raise SyntaxError(f'Input string "{s}" contains mismatched parens.')
    else:
        return True


def are_parens_matched_map_reduce(s: str) -> SyntaxError | bool:
    """
    A more functional approach to check that all parens are matching.
    Uses built-in Python `map` and `reduce` functions.
    """
    t: List = tokenize(s)
    if len(t) == 0:
        raise SyntaxError(f"Input string cannot be empty.")
    # make sure that user input starts and end with open/close parens
    elif t[0] != "(" or t[-1] != ")":
        raise SyntaxError(
            f'Input string "{s}" must start and end with open/closed parens.'
        )

    ### transform-reduce
    # transform (map) open parens to 1, close parens to -1,
    # and all other chars to 0, then sum the resulting iterator
    # if all parens are matched, res will be 0, otherwise, throw
    # a SyntaxError, because there are mismatched parens
    d = {"(": 1, ")": -1}
    res = reduce(lambda a, b: a + b, map(lambda x: d.get(x, 0), t))
    if res != 0:
        raise SyntaxError(f'Input string "{s}" contains mismatched parens.')
    else:
        return True


def tokenize(input: str) -> List[str]:
    """
    Split input string into a list of tokens. Note that we pad
    parentheses with white space before splitting to separate
    parentheses from Atoms
    --> we want '(+ 1 2)' to tokenize to ['(', '+', '1', '2', ')']
    not ['(+', '1', '2)']
    """

    tokenized_input: List[str] = input.replace("(", " ( ").replace(")", " ) ").split()
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

    # start a new sublist everytime we encounter an open parens
    if t == "(":
        ast = []
        # append tokens to sublist until we encounter a close parens
        while tokens[0] != ")":
            ast.append(generate_ast(tokens))
        tokens.pop(0)  # pop off ')'
        return ast
    elif t == ")":
        raise SyntaxError("Mismatched parens.")
    else:
        return atomize(t)


def eval(x: Exp, st=global_symbol_table):
    """Evaluate the abstract syntax tree"""
    if isinstance(x, Number):
        return x
    elif isinstance(x, Symbol):
        # start with the innermost scope of the symbol table
        # to find symbol definition, searching outer scope until
        # symbol definition is found
        return st.find(x)
    elif x[0] == "if":
        condition, statement, alternative = x[1:4]
        expression = (
            statement
            if eval(condition, SymbolTable(st.keys(), st.values(), st))
            else alternative
        )
        return eval(expression, SymbolTable(st.keys(), st.values(), st))
    elif x[0] == "defun":
        # `func_name`: str
        # `params`: List[str]
        # `func_body`: List
        # Example:
        #   "(defun doublen (n) (* 2 n))" -->
        #   `func_name`: "doublen"
        #   `params`: ["n"]
        #   `func_body`: ["*", 2, "n"]
        func_name, params, func_body = x[1:4]
        st[func_name] = (params, func_body)
        return f"Defined function: {func_name.upper()}"
    elif x[0] == "format":
        if isinstance(x[-1], list):
            fill_val = eval(x[-1], SymbolTable(st.keys(), st.values(), st))
            res = " ".join(str(i) for i in x[2:-1])
        else:
            fill_val = ""
            res = " ".join(str(i) for i in x[2:])
        if "~D~%" in res:
            res = res.replace('"', "").replace("~D~%", str(fill_val))
        else:
            res = res.replace('"', "").replace("~%", str(fill_val))
        return res
    else:
        func_name = x[0]
        func = eval(x[0], SymbolTable(st.keys(), st.values(), st))
        args = [eval(arg, SymbolTable(st.keys(), st.values(), st)) for arg in x[1:]]

        # if `func` is a tuple, it is a user defined function, so update local scoping
        # of symbol table with user-provided parameters
        if isinstance(func, tuple):
            params, func_body = func
            if len(args) != len(params):
                raise ValueError(
                    f'Function "{func_name}" expects {len(params)} arguments, but {len(args)} were provided.'
                )
            st.update(zip(params, args))
            return eval(func_body, SymbolTable(st.keys(), st.values(), st))
        elif isinstance(func, (int, float, str)):
            return func
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


if __name__ == "__main__":
    questions = [
        inquirer.List(
            name="mode",
            message="Would you like to open the REPL environment, or execute a file?",
            choices=[m.value for m in Mode],
        ),
    ]
    mode = inquirer.prompt(questions)["mode"]

    if mode == Mode.REPL.value:
        ### launch REPL env
        while True:
            try:
                user_input = input("pylisp> ")
                # first, validate user input
                # either returns True, or raises SyntaxError
                if are_parens_matched_map_reduce(user_input):
                    print(eval(generate_ast(tokenize(user_input))))
            except EOFError:
                break
    elif mode == Mode.FILE.value:
        ### read lisp script from txt file
        while True:
            input_file = input("Enter the location of the file: ")
            with open(input_file, "r") as file:
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
                    name="cont",
                    message="Would you like to execute another file?",
                    choices=["Yes", "No"],
                ),
            ]
            ans = inquirer.prompt(continue_yes_no)["cont"]

            match ans:
                case "Yes":
                    continue
                case "No":
                    break
                case _:
                    break
