#!/usr/bin/python3

import qckt
from QSystems import *
from Job import Job
import Registers as regs
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
inreg = regs.QRegister(ninreg)
outreg = regs.QRegister(noutreg)
rclreg = regs.CRegister(ninreg)
nqbits,ncbits,qplaced,cplaced = regs.placement(outreg,inreg,rclreg)
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

maxattempts = 5
solved = False
for m in range(maxattempts):  # Look for best of all attempts
	job = Job(grv_ckt, qtrace=False)
	bk = Qdeb()
	bk.runjob(job)
	res = job.get_creg()[0]
	value = res.intvalue

	### Verify if the result is correct
	verifyckt = qckt.QCkt(nqbits,ncbits,name="Verify")
	x_list = []
	for i in inreg:
		if (res.intvalue & (0b1<<i)) != 0:
			x_list.append(i)
	if len(x_list) > 0:
		verifyckt.X(x_list)
	# verifyckt = verifyckt.realign(self.fullnqbits, self.fullncbits,self.uf_outreg+self.uf_inreg)
	verifyckt = verifyckt.append(uf_ckt)
	verifyckt.M(outreg,[0])
	# print("### Verification Circuit ################################")
	# verifyckt.draw()

	job = Job(verifyckt)
	bk = Qdeb()
	bk.runjob(job)
	creg = job.get_creg()[0]
	if creg.intvalue == 1:
		solved = True
		break

if not solved:
	print("Did not find the solution")
else:
	# print(("Solution: {0:d} ({0:0"+str(ninreg)+"b})").format(value))
	print(("Solution: {0:0"+str(ninreg)+"b}, ({0:d})").format(value))
