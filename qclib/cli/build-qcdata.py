#!/usr/bin/python

import getopt
import qclib
import sys
import types
from qcdata import qcbld,igbld

def getint(prompt):
	gotit = False
	while gotit != True:
		sys.stdout.write(prompt)
		l = sys.stdin.readline()
		l = l[:-1]
		try:
			gotit = True
			n = int(l)
		except ValueError:
			gotit = False
			sys.stdout.write("Huh? please type an integer: ")
	return n

def getresp(prompt,defresp,otherresp):
	resp = defresp
	gotit = False
	while gotit != True:
		sys.stdout.write(prompt+" ["+defresp+"] : ")
		l = sys.stdin.readline()
		l = l[:-1]
		if l == "" or l == defresp:
			gotit = True
			resp = defresp
		elif l == otherresp:
			gotit = True
			resp = l
		else:
			sys.stdout.write("Huh?\n")
	return resp

def gettext(prompt):
	sys.stdout.write(prompt)
	l = sys.stdin.readline()
	l = l[:-1]
	return l

def main():
	# Process the command line arguments
	dontnew = True
	try:
		opts, args = getopt.getopt(sys.argv[1:],"n")
	except getopt.GetoptError:
		print sys.argv[0],"-n"
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-n':
			dontnew = True

	symtbl = qclib.qcsim.__dict__

	symkeys = symtbl.keys()
	for e in qcbld.keys():
		found = False
		for k in symkeys:
			if e == "qclib.qcsim."+k:
				found = True
				break
		if not found:
			del qcbld[e]

	qckeys = qcbld.keys()

	for i in symtbl:
		if isinstance(symtbl[i],types.FunctionType) and (not "qclib.qcsim."+i in igbld):
			k = "qclib.qcsim."+i
			procit = False
			if (k in qckeys) and (not dontnew):
				print
				print k,"--EXISTING INFORMATION-------------"
				print "Command: ",qcbld[k][0]
				print "Description: ",qcbld[k][1]
				print "Arguments: ",qcbld[k][2]

			if (not k in qckeys) or (not dontnew):
				resp = getresp( "{:s} ".format(k),"n","y")
				if resp == "n":
					procit = False
					if k in qckeys:
						re = getresp("type y to DELETE it, n to retain as is","n","y")
						if re == "y":
							igbld.append(k)
					else:
						igbld.append(k)
				elif resp == "y":
					procit = True
				else:
					sys.stdout.write("Internal error - getresp() returned something odd.")

			if procit:
				n = getint("Number of qubits: ")
				cmd = gettext("Command: ")
				desc = gettext("Usage: ")
				p1 = desc
				p2 = "qgate:{:d}".format(n)
				# print k,"[",p1,p2,"]"
				# print "qclib.qcsim.{:s}: [\"{:s}\" qgate:{:d}]".format(i,desc,n)
				qcbld[k] = [cmd,p1,p2]

	outf = open("qcdata.py","w")

	print "Writing qcdata.py - igbld[]..."
	outf.write("import qclib\n")
	outf.write("igbld = [\n")
	first = True
	for e in igbld:
		if first:
			first = False
		else:
			outf.write(",\n")
		outf.write("	\"{:s}\"".format(e))
	outf.write("\n	]\n")

	print "Writing qcdata.py - qcbld[]..."
	outf.write("qcbld = {\n")
	first = True
	for e in qcbld.keys():
		if first:
			first = False
		else:
			outf.write(",\n")
		outf.write("	\"{:s}\": [\"{:s}\",\"{:s}\",\"{:s}\"]".format(e,qcbld[e][0],qcbld[e][1],qcbld[e][2]))
	outf.write("\n	}\n")

	print "Writing qcdata.py - qcdata[]..."
	outf.write("qcdata = {\n")
	first = True
	for e in qcbld.keys():
		if first:
			first = False
		else:
			outf.write(",\n")
		outf.write("	\"{:s}\": [{:s},\"{:s}\",\"{:s}\"]".format(qcbld[e][0],e,qcbld[e][1],qcbld[e][2]))
	outf.write("\n	}\n")

if __name__ == "__main__":
	main()
