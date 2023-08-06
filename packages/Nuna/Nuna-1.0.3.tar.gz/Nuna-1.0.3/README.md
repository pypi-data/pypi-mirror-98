# PyNuna
Nuna Language Interpreter Implemented with Python <br>
Original Details : [nunalang/nuna](https://github.com/nunalang/nuna)

## Download
```pip install nuna``` <br>
[View at Pypi](https://pypi.org/project/Nuna)

## Example
```Python
from nuna import Nuna, generate

code = '''눈나..나..주...나..........거나..........거....나..........거나..........거나....누........나.........응
누나..나..나..거나..나.....나.....거...나..나.....거나..나.....주..눈나..........나..........응!'''
# Nuna code that prints '누나'

n = Nuna() # Nuna Executer
print(n.execute(code)) # Execute, and Print Last Memory Status

n.clear() # Clear Stack

code2 = generate('Hello, World!') # Generate code that prints 'Hello, World!'
n.execute(code2) # Execute
```