#!/usr/bin/python

import random as rnd
import numpy as np
import qclib

print "-------------------------------------------------------------------------------------------------------"
print "Problem Statement:"
print "  Given a function whose output is CONSTANT (does not change the result register)"
print "  or BALANCED (result register is equally 0 and 1 across all possible input values"
print "  Problem is to find which fx it is."
print
print "This program randomly selects one of the two fx's and the algorithm determines which one it is."
print "-------------------------------------------------------------------------------------------------------"
print

nqbits = 8

def fx(q):
	toss = int(rnd.random()*2.0)
	if toss == 0:
		print "fx is CONSTANT."
	elif toss == 1:
		print "fx is BALANCED."
		q.qgate(q.C(),[1,0])

try:
	q = qclib.qcsim(nqbits)
	q.qgate(q.X(),[0])
	q.qgate(q.H(),[0])

	for i in range(nqbits-1):
		q.qgate(q.H(),[i+1])

	fx(q)
	# q.qmeasure([0]) # measure it if you like, does not change anything

	for i in range(nqbits-1):
		q.qgate(q.H(),[i+1])

	v = q.qmeasure(range(nqbits-1,0,-1),qtrace=False)
	if 1 in v:
		print "Found fx is BALANCED"
	else:
		print "Found fx is CONSTANT"

except qclib.QClibError,ex:
	print ex.args
