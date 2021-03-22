#!/usr/bin/python3

import random as rnd
import numpy as np
import qcckt

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

def get_fxckt(nq):
	fxckt = qcckt.QCkt(nq)
	toss = int(rnd.random()*2.0)
	if toss == 0:
		print("fx is CONSTANT.")
	elif toss == 1:
		print("fx is BALANCED.")
		fxckt.C(1,0)
		# q.qgate(q.C(),[1,0])
	return fxckt

try:

	dj_ckt = qcckt.QCkt(nqbits)
	# q = qclib.qcsim(nqbits)
	dj_ckt.X(0)
	# q.qgate(q.X(),[0])
	dj_ckt.H(0)
	# q.qgate(q.H(),[0])

	for i in range(nqbits-1):
		dj_ckt.H(i+1)
		# q.qgate(q.H(),[i+1])

	dj_ckt.Border()
	fx_ckt = get_fxckt(nqbits)
	# fx(q)
	dj_ckt = dj_ckt.append(fx_ckt)
	# q.qmeasure([0]) # measure it if you like, does not change anything
	dj_ckt.Border()

	for i in range(nqbits-1):
		dj_ckt.H(i+1)
		# q.qgate(q.H(),[i+1])

	qbits_list = list(range(nqbits-1,0,-1))
	dj_ckt.M(qbits_list, qbits_list)
	# v = q.qmeasure(list(range(nqbits-1,0,-1)),qtrace=False)
	
	dj_ckt.draw()

	bk = qcckt.Backend()
	bk.run(dj_ckt,qtrace=False)
	res = bk.get_creg()
	print(res)

	if 1 in res.value[1:nqbits]:
		print("Found fx is BALANCED")
	else:
		print("Found fx is CONSTANT")

except qclib.QClibError as ex:
	print(ex.args)
