#!/usr/bin/env python

import sys
import ntpath
import getopt
import qsim
import collections as col

q = None
def initqc(n):
	global q
	q = qsim.QSimulator(n,qtrace=True)

def help():
	print("Commands:")
	for k in sorted(clidata.keys()):
		if not "qgate:" in clidata[k][2]:
			s = "  "+k+" "+clidata[k][1]
			if len(s) < 22:
				gap = " "*(22-len(s))
			else:
				gap = " "
			s = s + gap + " -- "+clidata[k][3]
			print(s)
	print("Gates:")
	for k in sorted(clidata.keys()):
		if "qgate:" in clidata[k][2]:
			s = "  "+k+" "+clidata[k][1]
			if len(s) < 22:
				gap = " "*(22-len(s))
			else:
				gap = " "
			s = s + gap + " -- "+clidata[k][3]
			print(s)

#####
## Aligned with v2.0
## aspec --
## 	<tag>:val,<tag>:val, ...
## tags --
## 	qsim:		-- is a member function of qsim.QSimulator
## 	args:[if]*	-- arguments list as a string of i and f, e.g., fiii (float, int, int, int)
## 	qlist:n		-- takes the last argument as a list of qubits. if n is '*', any number of qubits.
## 	qgate:		-- is a gate operation. Called as q.qgate(f(args),qlist)
#####

clidata = {
	"i":	[initqc,		"nqbits",	"args:i",		"Initialize QC"],
	# "r":	[qsim.QSimulator.qreset,	"",		"qsim:",		"Reset to init"],
	"q":	[quit,			"",		"",			"Quit"],
	"m":	[qsim.QSimulator.qmeasure,	"bit1 bit2 ...","qsim:,qlist:*",	"Measure qubits"],
	"?":	[help,			"",		"",			"Help"],
	"help": [help,			"",		"",			"Help"],
	"sqsw":	[qsim.SQSWAP,	"bit1 bit2",	"qgate:,qlist:2","SQ root SWAP gate"],
	"h":	[qsim.H,		"bit",		"qgate:,qlist:1","HADAMARD Gate"],
	"z":	[qsim.Z,		"bit",		"qgate:,qlist:1","Z Gate"],
	"c":	[qsim.C,		"cbit bit",	"qgate:,qlist:2","CNOT Gate"],
	"rk":	[qsim.Rk,	"k bit",	"args:i,qgate:,qlist:1","ROT(k) Gate"],
	"y":	[qsim.Y,		"bit",		"qgate:,qlist:1","Y Gate"],
	"x":	[qsim.X,		"bit",		"qgate:,qlist:1","X Gate"],
	"rphi":	[qsim.Rphi,	"phi bit",	"args:f,qgate:,qlist:1","ROT(Phi) Gate"],
	"t":	[qsim.T,		"cbit1 cbit2 bit",	"qgate:,qlist:3","TOFFOLI Gate"],
	"csw":	[qsim.CSWAP,	"cbit bit1 bit2",	"qgate:,qlist:3","C-SWAP Gate"],
	"sw":	[qsim.SWAP,	"bit1 bit2",		"qgate:,qlist:2","SWAP Gate"],
	"rnd":	[qsim.RND,	"bit",		"qgate:,qlist:1","Random aplitude Gate"],
	"qft":	[qsim.QFT,	"n n-bits ...",	"args:i,qgate:,qlist:*","QFT(n) Gate"],
	"hn":	[qsim.Hn,	"n n-bits ...",	"args:i,qgate:,qlist:*","Simultaneous n-HADAMARD Gates"]
	}

def parse_aspec(aspec):
	a = col.namedtuple("ArgSpec","isqsim na isqlist nq isqlim isgate")
	a.isqsim = False
	a.na = ""
	a.isqlist = False
	a.nq = 0
	a.isqlim = True
	a.isgate = False
	if ',' in aspec:
		aparts = aspec.split(",")
	else:
		aparts = [aspec]
	for e in aparts:
		if ':' in e:
			al = e.split(":")
		else:
			al = [e,""]
		tag = al[0]
		if tag == "qsim":
			a.isqsim = True
		if tag == "args":
			a.na = al[1]
		if tag == "qlist":
			a.isqlist = True
			if al[1] == "*":
				a.isqlim = False
			else:
				a.nq = int(al[1])
		if tag == "qgate":
			a.isgate = True
	return a
	# return isqsim, na, isqlist, nq, isqlim, isgate

def main():
	# Process the command line arguments
	try:
		opts, args = getopt.getopt(sys.argv[1:],"h")
	except getopt.GetoptError:
		print("Usage: "+ntpath.basename(sys.argv[0])+" [-h]")
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			help()

	print("Type '?' for help.")
	# Get into the main loop to get and process commands
	while True:
		try:
			sys.stdout.write("> ")
			sys.stdout.flush()
			l = sys.stdin.readline()
			cmdline = l.split()
			if len(cmdline) < 1:
				continue
			cmd = cmdline.pop(0)
			if cmd in clidata.keys():
				f = (clidata[cmd])[0]
				desc = (clidata[cmd])[1]
				aspec = (clidata[cmd])[2]
				a = parse_aspec(aspec)
				# (isqsim, na, isqlist, nq, isqlim, isgate) = parse_aspec(aspec)
				alist = []
				if a.isqsim:
					alist = [q]
				if (len(a.na) <= len(cmdline)) and ((not a.isqlim) or ((len(a.na)+a.nq) == len(cmdline))):
					for i in a.na:
						if i == "i":
							av = int(cmdline.pop(0))
						elif i == "f":
							av = float(cmdline.pop(0))
						else:
							print("Incorrect argument spec -- ",i)
							av = 0
						alist.append(av)
					l = []
					for i in range(len(cmdline)):
						bit = int(cmdline.pop(0))
						l.append(bit)
					if a.isgate:
						q.qgate(f(*alist),l)
					else:
						if a.isqlist:
							alist.append(l)
						f(*alist)
				else:
					print("Usage:",desc)
			else:
				print("Command not recognized")
		except ValueError:
			print("Error in value provided")
		except qsim.QSimError as m:
			print(m)

if __name__ == "__main__":
	main()
