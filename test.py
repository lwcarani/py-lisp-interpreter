import unittest
from unittest import TestCase
from parameterized.parameterized import parameterized
import math

from main import (
    are_parens_matched,
    are_parens_matched_functional,
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
    """Test py-lisp-interpreter functionality."""

    @parameterized.expand(
        [
            [
                '(+ 1 2)',
                True
            ],
            
            [
                '(+ 1 (* 3 4))', 
                True
            ],
            [
                '(*(+ 1 2)(+ 1 2))', 
                True
            ],
            [
                '(+ (/ 5 2) 2)', 
                True
            ],
            [
                '(defun doublen (n) (* n 2))', 
                True
            ],
            [
                '(defun fact (n) (if (<= n 1)  1 (* n (fact (- n 1)))))', 
                True
            ],
        ]
    )
    def test_matching_parens_helper_functional(
        self,
        input: str,
        expected_output: bool
    ) -> None:
        res: bool = are_parens_matched_functional(tokenize(input))
        self.assertEqual(res, expected_output)

    @parameterized.expand(
        [
            [
                ''
            ],
            [
                'fact 2'
            ],
            [
                '+ 1 2 (* 1 3)'
            ],
            [
                '(+ 1 2)))'
            ],
            [
                '(+ 1 2))'
            ],
            [
                '((+ 1{[([([{[([])]}])])]} 2)'
            ],
            [
                '((((((+ {}{}{}1 2)'
            ],
            [
                '((((+ 1 [][][][]2()())))))))))'
            ],
        ]
    )
    def test_matching_parens_helper_functional_throws_errors(
        self,
        input: str
    ) -> None:
        with self.assertRaises(SyntaxError):
            are_parens_matched_functional(tokenize(input))

    @parameterized.expand(
        [
            [
                '(+ 1 2)',
                True
            ],
            
            [
                '(+ 1 (* 3 4))', 
                True
            ],
            [
                '(*(+ 1 2)(+ 1 2))', 
                True
            ],
            [
                '(+ (/ 5 2) 2)', 
                True
            ],
            [
                '(defun doublen (n) (* n 2))', 
                True
            ],
            [
                '(defun fact (n) (if (<= n 1)  1 (* n (fact (- n 1)))))', 
                True
            ],
        ]
    )
    def test_matching_parens_helper(
        self,
        input: str,
        expected_output: bool
    ) -> None:
        res: bool = are_parens_matched(input)
        self.assertEqual(res, expected_output)

    @parameterized.expand(
        [
            [
                ''
            ],
            [
                'fact 2'
            ],
            [
                '+ 1 2 (* 1 3)'
            ],
            [
                '(+ 1 2)))'
            ],
            [
                '(+ 1 2))'
            ],
            [
                '((+ 1{[([([{[([])]}])])]} 2)'
            ],
            [
                '((((((+ {}{}{}1 2)'
            ],
            [
                '((((+ 1 [][][][]2()())))))))))'
            ],
        ]
    )
    def test_matching_parens_helper_throws_errors(
        self,
        input: str
    ) -> None:
        with self.assertRaises(SyntaxError):
            are_parens_matched(input)

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
                ['(', 'd', '2', ')'],
                [ 'd', 2]
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

            # pow
            ["(pow 2 2)", 4],
            ["(pow 2 3)", 8],
            ["(pow 2 4)", 16],
            ["(pow 3 3)", 27],

            # sqrt
            ["(sqrt 4)", 2],
            ["(sqrt 16)", 4],
            ["(sqrt 100)", 10],
            ["(sqrt 25)", 5],

            # pi
            ["(* pi 3)", math.pi * 3],
            ["(sqrt pi)", math.sqrt(math.pi)],
            ["(+ pi pi)", math.pi + math.pi],
            ["(/ pi (+ pi pi))", math.pi / (math.pi + math.pi)],

            # Chained Addition
            ["(+ 1 (+ 2 3))", 6],
            ["(+ 4 (+ 5 6))", 15],

            # Nested Chained Addition
            ["(+ 1 (+ 2 (+ 3 4)))", 10],
            ["(+ 4 (+ 5 (+ 6 7)))", 22],

            # Mixed Operators
            ["(* (+ 1 2) (+ 3 4))", 21],
            ["(* (+ 4 5) (+ 6 7))", 117],

            # conditionals
            ["(if (< 1 2) 1 2)", 1],
            ["(if (<= 1 2) 1 2)", 1],
            ["(if (> 1 2) 1 2)", 2],
            ["(if (>= 1 2) 1 2)", 2],
            ["(if (== 42 42) 42 -42)", 42],

            # nested if with pow, pi, sqrt
            ["(if (== 42 42) (if (== (pow 2 3) 8 ) 1 -2 ) -42)", 1],
            ["(if (== 42 42) (if (== (pow 2 3) 9 ) 1 -2 ) -42)", -2],
            ["(if (== 42 42) (if (== (sqrt 36) 6 ) 1 -2 ) -42)", 1],
            ["(if (== 42 42) (if (== (* pi 2) (+ pi pi) ) 1 -2 ) -42)", 1],

            # Define function
            ["(defun doublen (n) (* 2 n))", "Defined function: DOUBLEN"],
            ["(defun fib (n) (if (< n 2) n (+ (fib (- n 1)) (fib (- n 2)))))", "Defined function: FIB"],
            ["(defun fact (n) (if (<= n 1) 1 (* n (fact (- n 1)))))", "Defined function: FACT"],
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
