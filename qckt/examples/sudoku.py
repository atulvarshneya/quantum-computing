#!/usr/bin/python3

import qckt
from qException import QCktException
import Registers as regs
import libgrover as grv


inreg = regs.QRegister(4)
work = regs.QRegister(4)
outreg = regs.QRegister(1)
rclreg = regs.CRegister(4)
nqbits,ncbits,allqreg,allcreg = regs.placement(outreg,work,inreg,rclreg)

### Sudoku validation circuit
sudo = qckt.QCkt(nqbits,name="Sudoku Validator")
rules = [[0,1],[1,3],[3,2],[2,0]]
for w,r in enumerate(rules):
	sudo.CX(inreg[r[0]],work[w])
	sudo.CX(inreg[r[1]],work[w])
sudo.CX(*work,outreg[0])
for w,r in enumerate(rules):
	sudo.CX(inreg[r[0]],work[w])
	sudo.CX(inreg[r[1]],work[w])
# sudo.draw()

### create a single gate representation of the sudoku circuit, and replace the Uf circuit using that one gate
sudo_op = sudo.to_opMatrix()
sudockt = qckt.QCkt(nqbits,ncbits,name="Sudoku Validator")
sudockt.CUSTOM("Sudo",sudo_op,allqreg)
# sudo.draw()

grv_ckt = grv.Grover(sudockt,inreg,outreg,nmarked=2).getckt()
grv_ckt.M(inreg,rclreg)
grv_ckt.draw()

maxattempts = 10
for m in range(maxattempts):  # Look for best of all attempts
	bk = qckt.Backend()
	bk.run(grv_ckt, qtrace=False)
	res = bk.get_creg()
	value = res.intvalue
	print(("Solution: {0:d} ({0:0"+str(len(inreg))+"b})").format(value))
