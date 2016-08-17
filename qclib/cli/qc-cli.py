#!/usr/bin/python

import sys
import getopt
import qclib
from clidata import clidata

q = None
def initqc(n):
	global q
	q = qclib.qcsim(n,qtrace=True)

def help():
	for k in sorted(clidata.keys()):
		print k,"	",clidata[k][1]

def parse_aspec(aspec):
	isgate = False
	isqlim = True
	isnoq = False
	isqlist = False
	na = 0
	nq = 0
	if ',' in aspec:
		aparts = aspec.split(",")
	else:
		aparts = [aspec]
	for e in aparts:
		al = e.split(":")
		tag = al[0]
		if tag == "qgate":
			isgate = True
			if al[1] == "*":
				isqlim = False
			else:
				nq = int(al[1])
		if tag == "args":
			na = int(al[1])
		if tag == "noqc":
			isnoq = True
		if tag == "qlist":
			isqlist = True
			if al[1] == "*":
				isqlim = False
			else:
				nq = int(al[1])
	return isnoq, na, isgate, isqlim, nq, isqlist

#####
## aspec --
## 	<tag>:n,<tag>:m, ...
## tags --
## 	noqc:		-- is a function call NOT a member of qclib.qcsim
## 	args:n		-- is a function call, takes n arguments (all arguments are integers)
## 	qgate:n		-- is a gate operation and takes n qubits as argument.
## 	qclist:n	-- takes the last argument as a list of qubits. if n is *, any number of qubits.
#####

cmds = {
	"i": [initqc,"Command: init nqbits","noqc:,args:1"],
	"r": [qclib.qcsim.qreset, "Command: reset","args:0"],
	"q": [quit, "Command: quit","noqc:,args:0"],
	"m": [qclib.qcsim.qmeasure,"Command: measure bit1 bit2 ...","qlist:*"],
	"?": [help, "Command: list of commands","noqc:args:0"],
	"help": [help, "Command: list of commands","noqc:args:0"]
	}

def main():
	# copy in the commands into clidata
	for k in cmds.keys():
		clidata[k] = cmds[k]

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
				(isnoq, na, isgate, isqlim, nq, isqlist) = parse_aspec(aspec)
				if isnoq:
					alist = []
				else:
					alist = [q]
				if (na <= len(cmdline)) and ((not isqlim) or ((na+nq) == len(cmdline))):
					for i in range(na):
						av = int(cmdline.pop(0))
						alist.append(av)
					l = []
					for i in range(len(cmdline)):
						bit = int(cmdline.pop(0))
						l.append(bit)
					if isgate:
						q.qgate(f(*alist),l)
					else:
						if isqlist:
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
