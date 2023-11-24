import unittest
from unittest import TestCase
from parameterized.parameterized import parameterized
import math

from main import (
    are_parens_matched_map_reduce,
    are_parens_matched_stack,
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
        res: bool = are_parens_matched_map_reduce(input)
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
                ')))((('
            ],
            [
                '+ 1 2 (* 1 3)'
            ],
            [
                '(+ 1 2 (* 1 3'
            ],
            [
                '(+ 1 2 (* 1 3)'
            ],
            [
                '(+ 1 2)))'
            ],
            [
                '(+ 1 2))'
            ],
            [
                '(* 2 1((((((((())))))))'
            ],
            [
                '((((((+ 1 2)'
            ],
            [
                '((((+ 1 (((- 65 789)))))))2(* 1 2)(/ 5 5))))* 8 8))))))'
            ],
        ]
    )
    def test_matching_parens_helper_functional_throws_errors(
        self,
        input: str
    ) -> None:
        with self.assertRaises(SyntaxError):
            are_parens_matched_map_reduce(input)

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
        res: bool = are_parens_matched_stack(input)
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
                ')))((('
            ],
            [
                '+ 1 2 (* 1 3)'
            ],
            [
                '(+ 1 2 (* 1 3'
            ],
            [
                '(+ 1 2 (* 1 3)'
            ],
            [
                '(+ 1 2)))'
            ],
            [
                '(+ 1 2))'
            ],
            [
                '(* 2 1((((((((())))))))'
            ],
            [
                '((((((+ 1 2)'
            ],
            [
                '((((+ 1 (((- 65 789)))))))2(* 1 2)(/ 5 5))))* 8 8))))))'
            ],
        ]
    )
    def test_matching_parens_helper_throws_errors(
        self,
        input: str
    ) -> None:
        with self.assertRaises(SyntaxError):
            are_parens_matched_stack(input)

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
                '(format t "The double of 5 is ~D~%" (doublen 5))', 
                ['(', 'format', 't', '"The', 'double', 'of', '5', 'is', '~D~%"', '(', 'doublen', '5', ')', ')']
            ],
            [
                '(format t "Hello Coding Challenge World~%")', 
                ['(', 'format', 't', '"Hello', 'Coding', 'Challenge', 'World~%"', ')']
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
                ['(', 'format', 't', '"The', 'double', 'of', '5', 'is', '~D~%"', '(', 'doublen', '5', ')', ')'],
                ['format', 't', '"The', 'double', 'of', 5, 'is', '~D~%"', ['doublen', 5]]
            ],
            [
                ['(', 'format', 't', '"Hello', 'Coding', 'Challenge', 'World~%"', ')'],
                ['format', 't', '"Hello', 'Coding', 'Challenge', 'World~%"']
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
            ["(- (+ 5 (- 105 100)) (+ 1 2 ) )", 7],

            # sin
            ["(sin 0)", 0.0],
            ["(sin (/ pi (* (+ 1 1) (* 1 1))))", 1.0],

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
            ["(if (= 42 42) 42 -42)", 42],

            # nested if with pow, pi, sqrt
            ["(if (= 42 42) (if (= (pow 2 3) 8 ) 1 -2 ) -42)", 1],
            ["(if (= 42 42) (if (= (pow 2 3) 9 ) 1 -2 ) -42)", -2],
            ["(if (= 42 42) (if (= (sqrt 36) 6 ) 1 -2 ) -42)", 1],
            ["(if (= 42 42) (if (= (* pi 2) (+ pi pi) ) 1 -2 ) -42)", 1],

            # Define function
            ["(defun doublen (n) (* 2 n))", "Defined function: DOUBLEN"],
            ["(defun sum (a b) (+ a b))", "Defined function: SUM"],
            ["(defun mult (a b) (* a b))", "Defined function: MULT"],
            ["(defun meaning_of_life () (42))", "Defined function: MEANING_OF_LIFE"],
            ["(defun meaning_of_life_float () (42.0))", "Defined function: MEANING_OF_LIFE_FLOAT"],
            ["(defun fib (n) (if (< n 2) n (+ (fib (- n 1)) (fib (- n 2)))))", "Defined function: FIB"],
            ["(defun fact (n) (if (<= n 1) 1 (* n (fact (- n 1)))))", "Defined function: FACT"],
            ["(meaning_of_life)", 42],
            ["(meaning_of_life_float)", 42.0],
            ["(doublen 1)", 2],
            ["(doublen 25)", 50],
            ["(doublen 21)", 42],
            ["(doublen 617)", 1234],
            ["(sum 1 2)", 3],
            ["(sum 10 11)", 21],
            ["(sum 1 29)", 30],
            ["(    sum 5 25)", 30],
            ["(sum 11 19   )", 30],
            ["(sum 15    15)", 30],
            ["(mult 1 2)", 2],
            ["(mult 3 1)", 3],
            ["(mult 2 2)", 4],
            ["(/ (mult 567 2   ) 2 ) ", 567],
            ["(fact 0)", 1],
            ["(fact 1)", 1],
            ["(fact 2)", 2],
            ["(fact 3)", 6],
            ["(fact 4)", 24],
            ["(fact 5)", 120],
            ["(fact 6)", 720],
            ["(fib 0)", 0],
            ["(fib 1)", 1],
            ["(fib 2)", 1], 
            ["(fib 3)", 2],
            ["(fib 4)", 3],
            ["(fib 5)", 5],
            ["(fib 6)", 8],
            ["(fib 7)", 13],
            ["(fib 8)", 21],
            ["(fib 9)", 34],
            ["(fib 10)", 55],

            # format t
            ['(format t "The double of 5 is ~D~%" (doublen 5))', "The double of 5 is 10"],
            ['(format t "Hello Coding Challenge World~%")', "Hello Coding Challenge World"]
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
