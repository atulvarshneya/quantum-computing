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
noutreg = 1

### place the registers spreadout within the available qubits
inreg = qckt.QRegister(ninreg)
outreg = qckt.QRegister(noutreg)
rclreg = qckt.CRegister(ninreg)
nqbits,ncbits,qplaced,cplaced = qckt.placement(outreg,inreg,rclreg)
print("nq,nc,qplaced,cplaced =",nqbits,ncbits,qplaced,cplaced)

### 'needle' in the haytack = key
marked = int(rnd.random() * (2**ninreg-1))
print(("Marked to search = {0:0"+str(ninreg)+"b}, ({0:d})").format(marked))

### Build the Uf circuit
uf_ckt = qckt.QCkt(nqbits,ncbits,name="Uf")
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

### create a single gate representation of the Uf circuit, and replace the Uf circuit using that one gate
uf_op = uf_ckt.to_opMatrix()
uf_ckt = qckt.QCkt(nqbits,ncbits,name="Uf Circuit")
uf_ckt.CUSTOM("Uf",uf_op,qplaced)
# uf_ckt.draw()

grv_ckt = grv.Grover(uf_ckt,inreg,outreg).getckt()
grv_ckt.M(inreg,rclreg)
grv_ckt.draw()

correct_res = 0
job = qckt.Job(grv_ckt, shots=100)
bk = Qeng()
bk.runjob(job)
job.plot_counts(verbose=False)