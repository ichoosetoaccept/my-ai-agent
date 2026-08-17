from functions.run_python_file import run_python_file

print("Usage instructions")
print(run_python_file("calculator", "main.py"))

print("Calculate 3 + 5")
print(run_python_file("calculator", "main.py", ["3 + 5"]))

print("Calculator tests")
print(run_python_file("calculator", "tests.py"))

print("Outside working directory")
print(run_python_file("calculator", "../main.py"))

print("Nonexistent file")
print(run_python_file("calculator", "nonexistent.py"))

print("Not a Python file")
print(run_python_file("calculator", "lorem.txt"))
