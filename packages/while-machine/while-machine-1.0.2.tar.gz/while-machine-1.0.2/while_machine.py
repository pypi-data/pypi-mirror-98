import sys
import pyparsing as pp

class WhileMachine:
	def __init__(self):
		cmd = pp.Forward()
		reg = pp.Word(pp.nums).setParseAction(lambda toks: int(toks[0])).addCondition(lambda toks: toks[0]<21)
		inc = pp.Group('inc' + reg + reg)
		dec = pp.Group('dec' + reg + reg)
		zero = pp.Group('zero' + reg)
		wz = pp.Group('while' + reg + cmd)
		block = pp.Group('begin' + pp.Group(cmd[...]) + 'end')
		cmd <<=  inc | dec | zero | wz | block
		self._parser = cmd

	def compute(self, program, data):
		self._parse(program.lower())
		self._registers = [0]*21
		self._registers[1] = data		
		
		for cmd in self._program:
			self._compute_command(cmd)

		return self._registers[0]

	def _compute_command(self, cmd):
		if cmd[0] == 'inc':
			self._registers[cmd[1]] = self._registers[cmd[2]] + 1
		elif cmd[0] == 'dec':
			self._registers[cmd[1]] = max(0, self._registers[cmd[2]]-1)
		elif cmd[0] == 'zero':
			self._registers[cmd[1]] = 0
		elif cmd[0] == 'while':
			while self._registers[cmd[1]]:
				self._compute_command(cmd[2])	
		elif cmd[0] == 'begin':
			for c in cmd[1]:
				self._compute_command(c)	


	def compile_ram(self, program):
		self._parse(program.lower())
		self._ram = []
		self._jumps = []
		for cmd in self._program:
			self._compile_command(cmd)
		if max(self._jumps,default=0) > len(self._ram):
			self._ram.append('dec 21')
		return '\n'.join(self._ram)

	def _equalize(self, i, cmd):
		self._ram.append(f'jz {cmd[2]} {i+5}')
		self._ram.append(f'dec {cmd[2]}')
		self._ram.append(f'inc 22')
		self._ram.append(f'jz 21 {i+1}')
		self._ram.append(f'jz {cmd[1]} {i+8}')
		self._ram.append(f'dec {cmd[1]}')
		self._ram.append(f'jz 21 {i+5}')
		self._ram.append(f'jz 22 {i+13}')
		self._ram.append(f'dec 22')
		self._ram.append(f'inc {cmd[1]}')
		self._ram.append(f'inc {cmd[2]}')
		self._ram.append(f'jz 21 {i+8}')

	def _compile_command(self, cmd):
		i = len(self._ram)
		if cmd[0] == 'inc':
			if cmd[1] == cmd[2]:
				self._ram.append(f'inc {cmd[1]}')
			else:
				self._equalize(i, cmd)
				self._ram.append(f'inc {cmd[1]}')
		elif cmd[0] == 'dec':
			if cmd[1] == cmd[2]:
				self._ram.append(f'dec {cmd[1]}')
			else:
				self._equalize(i, cmd)
				self._ram.append(f'dec {cmd[1]}')
		elif cmd[0] == 'zero':
			self._ram.append(f'jz {cmd[1]} {i+4}')
			self._ram.append(f'dec {cmd[1]}')
			self._ram.append(f'jz 21 {i+1}')
		elif cmd[0] == 'while':
			self._ram.append(None)
			self._compile_command(cmd[2])	
			self._ram.append(f'jz 21 {i+1}')
			self._jumps.append(len(self._ram)+1)
			self._ram[i] = f'jz {cmd[1]} {self._jumps[-1]}'
		elif cmd[0] == 'begin':
			for c in cmd[1]:
				self._compile_command(c)

	def _parse(self, program):
		self._program = self._parser.parseString(program, parseAll=True)

def main():
	try:
		with open(sys.argv[1], 'r') as program:
			program = program.read()
		data = int(sys.argv[2])
	except:
		print('Usage: python -m while_machine <while source file> <input integer>')
	else:
		wm = WhileMachine()
		output = wm.compute(program, data)
		print(output)

if __name__ == '__main__':
	main()
