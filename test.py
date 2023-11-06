import unittest
from unittest import TestCase
from parameterized.parameterized import parameterized

from main import (
    tokenize, 
    generate_ast, 
    eval,
)

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

    @parameterized.expand(
        [
            [
                '(*(+ 1 2)(+ 1 2))',
                9,
            ],
            [
                '(*(+ 3 3)(+ 1 2) )',
                18,
            ],

            # Addition
            ["(+ 1 2) ", 3],
            ["(+ 0 0)", 0],
            ["(+ -1 1)", 0],
            ["(+ 2 3 )", 5],
            
            # Multiplication
            ["(* 2 3)", 6],
            ["(* 0 5)", 0],
            ["(* -2 4)", -8],
            ["(* 1 2)", 2],
            
            # Division
            ["(/ 6 2)", 3],
            ["(/ 9 3)", 3],
            ["(/ 1 2)", 0.5],
            ["(/ 8 2 )", 4],
            
            # Subtraction
            ["(- 5 2)", 3],
            ["(- 0 0)", 0],
            ["(- 2 5)", -3],
            ["(- 10 3 )", 7],

            # Basic Addition
            ["(+ 1 2)", 3],
            ["(+ 4 5)", 9],

            # Chained Addition
            ["(+ 1 (+ 2 3))", 6],
            ["(+ 4 (+ 5 6))", 15],

            # Nested Chained Addition
            ["(+ 1 (+ 2 (+ 3 4)))", 10],
            ["(+ 4 (+ 5 (+ 6 7)))", 22],

            # Mixed Operators
            ["(* (+ 1 2) (+ 3 4))", 21],
            ["(* (+ 4 5) (+ 6 7))", 117],
        ]
    )
    def test_ast_evaluator(
        self,
        input: str,
        expected_output: Number
    ) -> None:
        res = eval(generate_ast(tokenize(input)))
        self.assertEqual(res, expected_output)

if __name__ == '__main__':
    unittest.main()
