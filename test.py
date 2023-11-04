import unittest
from unittest import TestCase
from parameterized.parameterized import parameterized

from main import tokenize, generate_ast

Symbol = str
Number = (int, float)
Atom = (Symbol, Number)
List = list
Exp = (Atom, List)
Env = dict


class TestPyLispInterpreter(TestCase):
    """Test py-head functionality."""

    @parameterized.expand(
        [
            [
                '(+ 1 2)',
                ['(', '+', '1', '2', ')']
            ],
            [
                '(+ 1 (* 3 4))', 
                ['(', '+', '1', '(', '*', '3', '4', ')', ')']
            ],
            [
                '(*(+ 1 2)(+ 1 2))', 
                ['(', '*', '(', '+', '1', '2', ')', '(', '+', '1', '2', ')', ')']
            ],
            [
                '(+ (/ 5 2) 2)', 
                ['(', '+', '(', '/', '5', '2', ')', '2', ')']
            ],
            [
                '(defun doublen (n) (* n 2))', 
                ['(', 'defun', 'doublen', '(', 'n', ')', '(', '*', 'n', '2', ')', ')']
            ],
            [
                '(defun fact (n) (if (<= n 1)  1 (* n (fact (- n 1)))))', 
                [
                    '(', 'defun', 'fact', '(', 'n', ')', 
                    '(', 'if', '(', '<=', 'n', '1', ')', '1', 
                    '(', '*', 'n', 
                    '(', 'fact', '(', '-', 'n', '1', ')', ')', ')', ')', ')'
                ]
            ],
        ]
    )
    def test_tokenize(
        self,
        input: str,
        expected_output: str
    ) -> None:
        res = tokenize(input)
        self.assertEqual(res, expected_output)


    @parameterized.expand(
        [
            [
                ['(', '+', '1', '2', ')'],
                [ '+', 1, 2]
            ],
            [
                ['(', '+', '1', '(', '*', '3', '3', ')', ')'],
                [ '+', 1, ['*', 3, 3]]
            ],
            [
                ['(', 'defun', 'doublen', '(', 'n', ')', '(', '*', 'n', '2', ')', ')'],
                ['defun', 'doublen', ['n'], ['*', 'n', 2]]
            ],
        ]
    )
    def test_ast_generator(
        self,
        tokens: List,
        expected_output: List
    ) -> None:
        res = generate_ast(tokens)
        self.assertEqual(res, expected_output)

if __name__ == '__main__':
    unittest.main()
