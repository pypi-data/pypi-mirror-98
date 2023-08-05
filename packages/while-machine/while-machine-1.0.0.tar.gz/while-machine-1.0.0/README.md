# while-machine
While Abstract Machine implemented in python.

While Machine is an abstract machine that is turing complete and can compute any partial recursive function. Find out more here https://en.wikipedia.org/wiki/Abstract_machine

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

