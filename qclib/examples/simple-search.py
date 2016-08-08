#!/usr/bin/python

import random as rnd
import numpy as np
import qclib


def fx(q):
	toss = int(rnd.random()*4.0)
	print "Selected fx is {:02b}".format(toss)
	if toss == 0:
		q.qgate(q.X(),[2])
		q.qgate(q.X(),[1])
		q.qgate(q.T(),[2,1,0])
		q.qgate(q.X(),[1])
		q.qgate(q.X(),[2])
	elif toss == 1:
		q.qgate(q.X(),[2])
		q.qgate(q.T(),[2,1,0])
		q.qgate(q.X(),[2])
	elif toss == 2:
		q.qgate(q.X(),[1])
		q.qgate(q.T(),[2,1,0])
		q.qgate(q.X(),[1])
	elif toss == 3:
		q.qgate(q.T(),[2,1,0])

def U():
	return ["U",np.matrix([
		[-0.5,0.5,0.5,0.5],
		[0.5,-0.5,0.5,0.5],
		[0.5,0.5,-0.5,0.5],
		[0.5,0.5,0.5,-0.5]],dtype=complex)]

print "-------------------------------------------------------------------------------------------------------"
print "Problem Statement:"
print "  Given a function which outputs 1 either on inputs of 00 (fx=00), 01 (fx=01), 10 (fx=10) or 11 (fx=11)"
print "  Problem is to find which fx it is."
print
print "This program randomly selects one of the four fx's and the algorithm determines which one it is."
print "-------------------------------------------------------------------------------------------------------"
print

q = qclib.qcsim(3)
q.qgate(q.X(),[0])
q.qgate(q.H(),[0])
q.qgate(q.H(),[2])
q.qgate(q.H(),[1])
fx(q)
# q.qmeasure([0])
q.qgate(U(),[2,1])
v = q.qmeasure([2,1])
print "Found fx = {:d}{:d}".format(v[0],v[1])
