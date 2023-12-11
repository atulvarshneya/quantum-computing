#!/usr/bin/env python

import numpy as np
import qsim
import qsim.noisemodel as nmdl


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
			op_list.append(qsim.X())
		else:
			op_list.append(["I",np.matrix(np.eye(2),dtype=complex)])
	op_list.append(["I",np.matrix(np.eye(2),dtype=complex)])
	uprep = qsim.qcombine_par("U-Prep",op_list)

	uflip = qsim.X()
	for i in range(n-1,0,-1):
		uflip = qsim.CTL(uflip)

	return qsim.qcombine_seq(name,[uprep,uflip,uprep])

#################################################################################

def main(n):
	intro()

	# bit flip probality of around 0.002 is about the max that this circuit can tolerate
	noise_ops = nmdl.bit_flip(probability=0.0025)
	noise_all_gates = nmdl.NoiseOperatorSequence(noise_ops)
	noise_model = {
		'noise_opseq_allgates': noise_all_gates
	}

	q = qsim.NISQSimulator(n)

	print("Building Uf operator ...")
	Ufgate = Uf(q)
	print("Buiding UinvM operator ...")
	UinvMgate = UinvM(q)

	print("Take from the following, best of 5 results...")
	for m in range(5):  # Look for best of 5
		q = qsim.NISQSimulator(n, noise_model=noise_model, qtrace=False)
		# Hn on x-register
		q.qgate(qsim.Hn(n-1), list(range(n-1,0,-1)))
		# prepare b as |->
		q.qgate(qsim.X(),[0])
		q.qgate(qsim.H(),[0])

		numitrs = int(q.pi * (2.0**((n-1.0)/2.0))/4.0) # optimal # iter, less or more dont work
		for itr in range(numitrs):
			q.qgate(Ufgate,list(reversed(range(n))))
			q.qgate(qsim.Hn(n-1), list(range(n-1,0,-1)))
			q.qgate(UinvMgate,list(reversed(range(n))))
			q.qgate(qsim.Hn(n-1), list(range(n-1,0,-1)))
		res = q.qmeasure(list(range(n-1,0,-1)))
		print("Result",m,"=",res)

if __name__ == "__main__":
	main(8)
