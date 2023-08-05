import sys
import pyparsing as pp

class WhileMachine:
	def __init__(self):
		cmd = pp.Forward()
		reg = pp.Word(pp.nums).setParseAction(lambda toks: int(toks[0])).addCondition(lambda toks: toks[0]<21)
		inc = pp.Group('inc' + reg)
		dec = pp.Group('dec' + reg)
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

	def _compute_command(self,cmd):
		if cmd[0] == 'inc':
			self._registers[cmd[1]] += 1
		elif cmd[0] == 'dec':
			self._registers[cmd[1]] = max(0, self._registers[cmd[1]]-1)
		elif cmd[0] == 'zero':
			self._registers[cmd[1]] = 0
		elif cmd[0] == 'while':
			while self._registers[cmd[1]]:
				self._compute_command(cmd[2])	
		elif cmd[0] == 'begin':
			for c in cmd[1]:
				self._compute_command(c)	

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
