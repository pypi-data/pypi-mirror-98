# while-machine
While Abstract Machine implemented in python.

While Machine is an abstract machine that is turing complete and can compute any partial recursive function. Find out more here https://en.wikipedia.org/wiki/Abstract_machine

Its simpler brother is called Random Access Machine and you can find its implementation here https://github.com/GabrieleMaurina/random-access-machine

### Install

Run inside terminal:

```python -m pip install while-machine```

### Usage

To execute a ram source file:

```python -m while_machine <while source file> <integer input>```

To import it in your script:

```python
from while_machine import WhileMachine

data = 4
program = 'begin inc 0 inc 0 end'

wm = WhileMachine()
result = wm.compute(program, data)

print(result) # 2
```

### How it works

A while machine has 21 registers numbered from 0, 1, 2..., the input is loaded on register 1 before the execution starts, the output is taken from register 0 when the execution ends.

### Instructions:

A while machine supports only 4 basic instructions:

Increment register k by 1:

```inc k```

Decrement register k by 1:

```dec k```

Set register k to zero:

```zero k```

While register k is not zero, do the following command:

```while k```

Commands can be grouped with:

```
begin
	...
	...

end
```

### Example

An example program that will double whatever input you give to the machine:

```
while 1
begin
	inc 0
	inc 0
	dec 1
end
```

### RAM compiler

It is possible to compile a While program into a Ram program using the method compile_ram of the class WhileMachine. You can find an implementation of the ram machine here https://github.com/GabrieleMaurina/random-access-machine

Here is an example of how to compile from While to RAM:

```python
from while_machine import WhileMachine
import sys

def main():
	wm = WhileMachine()
	with open(sys.argv[1],'r') as while_prog, open(sys.argv[2],'w') as ram_prog:
		while_prog = while_prog.read()
		compiled = wm.compile_ram(while_prog)
		ram_prog.write(compiled)

if __name__ == '__main__':
	main()
```
