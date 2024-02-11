#!/usr/bin/env python

import qckt
from qckt.backend import *
import libgrover as grv
import random as rnd
import sys

### get the command line arguments
if len(sys.argv) != 2:
	print(f"Usage: {sys.argv[0]} in_register_size")
	quit()
ninreg = int(sys.argv[1])
nwkreg = 2
noutreg = 1

### input, output, and (dummy) work registers
inreg = [i for i in reversed(range(ninreg))]
wkreg = [i+ninreg for i in reversed(range(nwkreg))]
outreg = [i+ninreg+nwkreg for i in reversed(range(noutreg))]
nqbits = ninreg + +nwkreg + noutreg

### 'needle' in the haytack = key
marked = int(rnd.random() * (2**ninreg-1))
print(("Marked to search = {0:0"+str(ninreg)+"b}, ({0:d})").format(marked))

### Build the Oracle circuit
uf_ckt = qckt.QCkt(nqbits,nqbits,name="Oracle")
x_list = []
for i in range(ninreg):
	if (marked & (0b1<<i)) == 0:
		x_list.append(inreg[ninreg-i-1])
if len(x_list) > 0:
	uf_ckt.X(x_list)
uf_ckt.CX(*inreg, *outreg)
if len(x_list) > 0:
	uf_ckt.X(x_list)
# uf_ckt.draw()

### create a single gate representation of the Oracle circuit, and replace the Oracle circuit using that one gate
uf_op = uf_ckt.to_opMatrix()
qckt.define_gate("Oracle", uf_op)
uf_ckt = qckt.QCkt(nqbits,nqbits,name="Oracle Circuit")
uf_ckt.Oracle(*outreg, *wkreg, *inreg)
# uf_ckt.draw()

grv_ckt = grv.Grover(uf_ckt,inreg,outreg).getckt()
grv_ckt.M(inreg)
grv_ckt.draw()

correct_res = 0
job = qckt.Job(grv_ckt, shots=100)
bk = Qeng()
bk.runjob(job)
job.plot_counts(verbose=False)