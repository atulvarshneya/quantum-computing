#!/usr/bin/python3

import qckt
import Registers as regs
import libgrover as grv
import random as rnd
import sys

### get the command line arguments
if len(sys.argv) != 2:
	print(f"Usage: {sys.argv[0]} in_register_size")
	quit()
ninreg = int(sys.argv[1])

### place the registers spreadout within the available qubits
inreg = regs.QRegister(ninreg)
outreg = regs.QRegister(1)
nqbits,ncbits,qplaced,cplaced = regs.placement(outreg,inreg)
print("nq,nc,qplaced,cplaced =",nqbits,ncbits,qplaced,cplaced)

### 'needle' in the haytack = key
marked = int(rnd.random() * (2**(len(inreg))-1))
print(("Marker to search = {0:0"+str(ninreg)+"b}, ({0:d})").format(marked))

### Build the Uf circuit
uf_ckt = qckt.QCkt(nqbits,ncbits,name="Uf")
x_list = []
for i in range(len(inreg)):
	if (marked & (0b1<<i)) == 0:
		x_list.append(inreg[len(inreg)-i-1])
if len(x_list) > 0:
	uf_ckt.X(x_list)
uf_ckt.CX(*(inreg + outreg ))
if len(x_list) > 0:
	uf_ckt.X(x_list)
# uf_ckt.draw()

### create a single gate representation of the Uf circuit, and replace the Uf circuit using that one gate
uf_op = uf_ckt.to_opMatrix()
uf_ckt = qckt.QCkt(nqbits,ncbits,name="Uf Circuit")
uf_ckt.custom_gate("Uf",uf_op)
uf_ckt.Uf(qplaced)
# uf_ckt.draw()

ginstance = grv.Grover(uf_ckt,inreg,outreg)
ginstance.getckt().draw()

solved,value = ginstance.solve(5)
if not solved:
	print("Did not find the solution")
else:
	print(("Solution: {0:d} ({0:0"+str(len(inreg))+"b})").format(value))
