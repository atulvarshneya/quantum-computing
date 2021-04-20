#!/usr/bin/python3

import random as rnd
import numpy as np
import qsim
import qgates as qgt
from qSimException import *

print("""
-------------------------------------------------------------------------------------------------------
Problem Statement:
  Given a function whose output is CONSTANT (fixed output in the result
  register) or BALANCED (result register is equally 0 and 1 across all
  possible input values. Problem is to find which fx it is.

This program randomly selects one of the two fx's and the algorithm
determines which one it is.
-------------------------------------------------------------------------------------------------------
""")

nqbits = 8

def fx(q):
	toss = int(rnd.random()*2.0)
	if toss == 0:
		print("fx is CONSTANT.")
	elif toss == 1:
		print("fx is BALANCED.")
		q.qgate(qgt.C(),[1,0])

try:
	q = qsim.QSimulator(nqbits)
	q.qgate(qgt.X(),[0])
	q.qgate(qgt.H(),[0])

	for i in range(nqbits-1):
		q.qgate(qgt.H(),[i+1])

	fx(q)
	# q.qmeasure([0]) # measure it if you like, does not change anything

	for i in range(nqbits-1):
		q.qgate(qgt.H(),[i+1])

	v = q.qmeasure(list(range(nqbits-1,0,-1)),qtrace=False)
	if 1 in v:
		print("Found fx is BALANCED")
	else:
		print("Found fx is CONSTANT")

except QSimError as ex:
	print(ex.args)
