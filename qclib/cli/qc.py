#!/usr/bin/python

import sys
import qclib
from qcdata import qcdata

cmds = {
	"i": "init nqbits",
	"r": "reset",
	"q": "quit",
	"m": "measure bit1 bit2 ...",
	"?": "list of commands",
	"help": "list of commands"
	}

q = None
while True:
	try:
		sys.stdout.write("> ")
		l = sys.stdin.readline()
		cmdline = l.split()
		if len(cmdline) < 1:
			continue
		cmd = cmdline[0]
		if cmd == 'q' or cmd == 'Q':
			quit()
		elif cmd == 'init' or cmd == 'i':
			if len(cmdline) != 2:
				print "Usage:",cmds['i']
			else:
				nqbits = int(cmdline[1])
				q = qclib.qcsim(nqbits,qtrace=True)
		elif cmd == 'r' or cmd == 'reset':
			if len(cmdline) != 1:
				print "Usage:",cmds['r']
			else:
				q.qreset()
		elif cmd == '?' :
			print "Commands ------"
			for k in cmds.keys():
				print k,"	",cmds[k]
			print "Gates ------"
			for k in qcdata.keys():
				print k,"	",qcdata[k][1]
		elif cmd == 'm' or cmd == "measure":
			if len(cmdline) < 2:
				print "Usage:",cmds['m']
			blist = []
			for b in range(len(cmdline)-1):
				blist.append(int(cmdline[b+1]))
			q.qmeasure(blist)
			pass
		elif cmd in qcdata.keys():
			f = (qcdata[cmd])[0]
			desc = (qcdata[cmd])[1]
			aspec = (qcdata[cmd])[2]
			(at,ac) = aspec.split(':')
			ac = int(ac)
			if ac == (len(cmdline)-1):
				l = []
				for i in range(ac):
					bit = int(cmdline[i+1])
					l.append(bit)
				print l
				q.qgate(f(q),l)
			else:
				print "Usage:",desc
		else:
			print "Command not recognized"
	except ValueError:
		print "Error in value provided"
	except qclib.QClibError, m:
		print m
