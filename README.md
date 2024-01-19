# py-lisp-interpreter

## About
`py-lisp-interpreter` is a basic Lisp interpreter, written in Python. Running `pylisp` from the command line will allow the user to enter the Lisp REPL environment, or execute a .txt file from a provided file path. 

## Instructions
For Windows, create a folder named `Aliases` in your C drive: `C:/Aliases`. Add this folder to PATH. Next, create a batch file that will execute when you call the specified alias. For example, on my machine, I have a batch file named `pylisp.bat` located at `C:/Aliases`, that contains the following script:

```bat
@echo off
echo.
call C:\...\py-lisp-interpreter\pylisp_venv\Scripts\activate.bat
python C:\...\py-lisp-interpreter\main.py %*
```

So now, when I type `pylisp` in the command prompt, this batch file will execute, which in turn, launches the appropriate Python virtual environment, then runs the `py-lisp-interpreter` Python script. 

## Examples

Running `pylisp` from the command line launches a cli option to enter the REPL environment or execute a local file:

```cmd
C:\> pylisp

[?] Would you like to open the REPL environment, or execute a file?: file
 > file
   REPL

Enter the location of the file: test_script.txt
Defined function: HELLO
Defined function: MEANING_OF_LIFE
Defined function: MEANING_OF_LIFE_ANSWER
Defined function: DOUBLEN
Defined function: FIB
Defined function: FACT
Hello Coding Challenge World
42
The meaning of life is 42
The double of 5 is 10
The double of 21 is 42
The double of 107 is 214
Factorial of 5 is 120
Factorial of 6 is 720
Factorial of 7 is 5040
Factorial of 10 is 3628800
Factorial of 12 is 479001600
The 7th number of the Fibonacci sequence is 13
```

After running a local file, the user is then prompted to enter another file to execute, or they can exit the program:

```cmd
[?] Would you like to execute another file?: No
   Yes
 > No
```

If the user chooses to enter the REPL environment, they can then execute simple Lisp expressions:

```cmd
C:\> pylisp

[?] Would you like to open the REPL environment, or execute a file?: REPL
   file
 > REPL

pylisp> (+ 21 21)
42
pylisp> (pow 2 3)
8.0
pylisp> (sin (/ pi 2) )
1.0
pylisp> (sin (/ pi 4) )
0.7071067811865476
pylisp> (defun fact (n) (if (<= n 1) 1 (* n (fact (- n 1)))))
Defined function: FACT
pylisp> (fact 5)
120
pylisp> (fact 10)
3628800
pylisp> (defun add (a b) (+ a b))
Defined function: ADD
pylisp> (add 4 5)
9
pylisp> (add (add 21 21) 42 )
84
pylisp> (add (add 21 21) (fact 5) )
162
```

## Acknowledgements
Thanks to [John Crickett](https://github.com/JohnCrickett) for the idea from his site, [Coding Challenges](https://codingchallenges.substack.com/p/coding-challenge-30-lisp-interpreter)!

Feedback, bug reports, issues, and pull requests welcome!
