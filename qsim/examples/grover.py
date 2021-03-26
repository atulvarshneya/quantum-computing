#!/usr/bin/python3

import numpy as np
import qsim


def intro():
	print("""Grover's Algorithm.

Problem Statement:
Well known search algorithm by Lov Grover.

	      +----+     +------+     +----+    +------+    +----+
n-1	|0> --|    |-----|      |-----|    |----|      |----|    |--- ... --(/)
n-2	|0> --|    |-----|      |-----|    |----|      |----|    |--- ... --(/)
n-3	|0> --| Hn |-----|  Uf  |-----| Hn |----| UinvM|----| Hn |--- ... --(/)
	       ...         ...         ...        ...        ...
2	|0> --|    |-----|      |-----|    |----|      |----|    |--- ... --(/)
1	|0> --|    |-----|      |-----|    |----|      |----|    |--- ... --(/)
	      +----+     |      |     +----+    |      |    +----+
0	|-> -------------|      |---------------|      |-------------
			 +------+               +------+

	     \-Init-/  \------------------Iterate-------------------/  \-Measure-/
""")

#################################################################################
# Details @ https://en.wikipedia.org/wiki/Grover%27s_algorithm

# Functions to build Grover's algo gates- Phase-flip and Invert-around-mean
def Uf(q):
	n = q.qsize()
	key = 0b11011010 & (2**(n-1) - 1)
	fmt = "{:0"+str(n-1)+"b}"
	print("Uf(): Setup to search key =",fmt.format(key))
	return __u(q,key,"Uf")

def UinvM(q):
	'''
	Used for inverse around Mean
	'''
	key = 0
	return __u(q,key,"UinvM")

def __u(q,key,name):
	n = q.qsize()
	# 'needle' in the haytack = key
	op_list = []
	for i in range(n-1,0,-1):
		if (key & (0b1<<(i-1))) == 0:
			op_list.append(q.X())
		else:
			op_list.append(["I",np.matrix(np.eye(2),dtype=complex)])
	op_list.append(["I",np.matrix(np.eye(2),dtype=complex)])
	uprep = q.qcombine_par("U-Prep",op_list)

	uflip = q.X()
	for i in range(n-1,0,-1):
		uflip = q.CTL(uflip)

	return q.qcombine_seq(name,[uprep,uflip,uprep])

#################################################################################

def main(n):
	intro()

	q = qsim.QSimulator(n)

	print("Building Uf operator ...")
	Ufgate = Uf(q)
	print("Buiding UinvM operator ...")
	UinvMgate = UinvM(q)

	print("Take from the following, best of 5 results...")
	for m in range(5):  # Look for best of 5
		q.qreset()
		# Hn on x-register
		q.qgate(q.Hn(n-1), list(range(n-1,0,-1)))
		# prepare b as |->
		q.qgate(q.X(),[0])
		q.qgate(q.H(),[0])

		numitrs = int(q.pi * (2.0**((n-1.0)/2.0))/4.0) # optimal # iter, less or more dont work
		for itr in range(numitrs):
			q.qgate(Ufgate,list(reversed(range(n))))
			q.qgate(q.Hn(n-1), list(range(n-1,0,-1)))
			q.qgate(UinvMgate,list(reversed(range(n))))
			q.qgate(q.Hn(n-1), list(range(n-1,0,-1)))
		res = q.qmeasure(list(range(n-1,0,-1)))
		print("Result",m,"=",res)

if __name__ == "__main__":
	main(8)
