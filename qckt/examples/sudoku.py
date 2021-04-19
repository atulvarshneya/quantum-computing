#!/usr/bin/python3

import qckt
from qException import QCktException
import Registers as regs
import libgrover as grv


inreg = regs.QRegister(4)
work = regs.QRegister(4)
outreg = regs.QRegister(1)
nqbits,_,qplaced,_ = regs.placement(outreg,work,inreg)

### Sudoku validation circuit
sudo = qckt.QCkt(nqbits,name="Sudoku Validator")
rules = [[0,1],[1,3],[3,2],[2,0]]
for w,r in enumerate(rules):
	sudo.CX(inreg[r[0]],work[w])
	sudo.CX(inreg[r[1]],work[w])
sudo.CX(*(work[:]),outreg[0])
for w,r in enumerate(rules):
	sudo.CX(inreg[r[0]],work[w])
	sudo.CX(inreg[r[1]],work[w])
# sudo.draw()

### create a single gate representation of the sudoku circuit, and replace the Uf circuit using that one gate
sudo_op = sudo.to_opMatrix()
sudo = qckt.QCkt(nqbits,name="Sudoku Validator")
sudo.CUSTOM("Sudo",sudo_op,qplaced)
# sudo.draw()

ginstance = grv.Grover(sudo,inreg,outreg,nmarked=2)
ginstance.getckt().draw()

solved, value = ginstance.solve(5)

if not solved:
	print("Did not find the solution")
else:
	print(("Solution: {0:d} ({0:0"+str(len(inreg))+"b})").format(value))
