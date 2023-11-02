from typing import List

def tokenize(input: str) -> List[str]:
    return input.replace('(', ' ( ').replace(')', ' ) ').split()


while True:
    try: print(tokenize(input("pylisp> ")))
    except EOFError: break