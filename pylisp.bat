::=======================================================================
:: The below will launch the py-lisp program, a basic Lisp interpreter,
:: written in Python. For Windows, place this batch file in the user's
:: C:/Aliases folder, after adding C:/Aliases to PATH.
::=======================================================================
@echo off
echo.
call C:\...\py-lisp-interpreter\pylisp_venv\Scripts\activate.bat
python C:\...\py-lisp-interpreter\main.py %*