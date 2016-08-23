#!/usr/bin/python

import sys
import getopt
import qclib
import collections as col

q = None
def initqc(n):
	global q
	q = qclib.qcsim(n,qtrace=True)

def help():
	print "Commands:"
	for k in sorted(clidata.keys()):
		if not "qgate:" in clidata[k][2]:
			s = "  "+k+" "+clidata[k][1]
			if len(s) < 22:
				gap = " "*(22-len(s))
			else:
				gap = " "
			s = s + gap + " -- "+clidata[k][3]
			print s
	print "Gates:"
	for k in sorted(clidata.keys()):
		if "qgate:" in clidata[k][2]:
			s = "  "+k+" "+clidata[k][1]
			if len(s) < 22:
				gap = " "*(22-len(s))
			else:
				gap = " "
			s = s + gap + " -- "+clidata[k][3]
			print s

#####
## Aligned with v2.0
## aspec --
## 	<tag>:val,<tag>:val, ...
## tags --
## 	qcsim:		-- is a member function of qclib.qcsim
## 	args:[if]*	-- arguments list as a string of i and f, e.g., fiii (float, int, int, int)
## 	qlist:n		-- takes the last argument as a list of qubits. if n is '*', any number of qubits.
## 	qgate:		-- is a gate operation. Called as q.qgate(f(args),qlist)
#####

clidata = {
	"i":	[initqc,		"nqbits",	"args:i",		"Initialize QC"],
	"r":	[qclib.qcsim.qreset,	"",		"qcsim:",		"Reset to init"],
	"q":	[quit,			"",		"",			"Quit"],
	"m":	[qclib.qcsim.qmeasure,	"bit1 bit2 ...","qcsim:,qlist:*",	"Measure qubits"],
	"?":	[help,			"",		"",			"Help"],
	"help": [help,			"",		"",			"Help"],
	"sqsw":	[qclib.qcsim.SQSWAP,	"bit1 bit2",	"qcsim:,qgate:,qlist:2","SQ root SWAP gate"],
	"h":	[qclib.qcsim.H,		"bit",		"qcsim:,qgate:,qlist:1","HADAMARD Gate"],
	"z":	[qclib.qcsim.Z,		"bit",		"qcsim:,qgate:,qlist:1","Z Gate"],
	"c":	[qclib.qcsim.C,		"cbit bit",	"qcsim:,qgate:,qlist:2","CNOT Gate"],
	"rk":	[qclib.qcsim.Rk,	"k bit",	"qcsim:,args:i,qgate:,qlist:1","ROT(k) Gate"],
	"y":	[qclib.qcsim.Y,		"bit",		"qcsim:,qgate:,qlist:1","Y Gate"],
	"x":	[qclib.qcsim.X,		"bit",		"qcsim:,qgate:,qlist:1","X Gate"],
	"rphi":	[qclib.qcsim.Rphi,	"phi bit",	"qcsim:,args:f,qgate:,qlist:1","ROT(Phi) Gate"],
	"t":	[qclib.qcsim.T,		"cbit1 cbit2 bit",	"qcsim:,qgate:,qlist:3","TOFFOLI Gate"],
	"csw":	[qclib.qcsim.CSWAP,	"cbit bit1 bit2",	"qcsim:,qgate:,qlist:3","C-SWAP Gate"],
	"sw":	[qclib.qcsim.SWAP,	"bit1 bit2",		"qcsim:,qgate:,qlist:2","SWAP Gate"],
	"rnd":	[qclib.qcsim.RND,	"bit",		"qcsim:,qgate:,qlist:1","Random aplitude Gate"],
	"qft":	[qclib.qcsim.QFT,	"n n-bits ...",	"qcsim:,args:i,qgate:,qlist:*","QFT(n) Gate"],
	"hn":	[qclib.qcsim.Hn,	"n n-bits ...",	"qcsim:,args:i,qgate:,qlist:*","Simultabeous n-HADAMARD Gates"]
	}

def parse_aspec(aspec):
	a = col.namedtuple("ArgSpec","isqcsim na isqlist nq isqlim isgate")
	a.isqcsim = False
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
		if tag == "qcsim":
			a.isqcsim = True
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
	# return isqcsim, na, isqlist, nq, isqlim, isgate

def main():
	# Process the command line arguments
	try:
		opts, args = getopt.getopt(sys.argv[1:],"h")
	except getopt.GetoptError:
		print sys.argv[0],"-h"
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			help()

	# Get into the main loop to get and process commands
	while True:
		try:
			sys.stdout.write("> ")
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
				# (isqcsim, na, isqlist, nq, isqlim, isgate) = parse_aspec(aspec)
				alist = []
				if a.isqcsim:
					alist = [q]
				if (len(a.na) <= len(cmdline)) and ((not a.isqlim) or ((len(a.na)+a.nq) == len(cmdline))):
					for i in a.na:
						if i == "i":
							av = int(cmdline.pop(0))
						elif i == "f":
							av = float(cmdline.pop(0))
						else:
							print "Incorrect argument spec -- ",i
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
					print "Usage:",desc
			else:
				print "Command not recognized"
		except ValueError:
			print "Error in value provided"
		except qclib.QClibError, m:
			print m

if __name__ == "__main__":
	main()
