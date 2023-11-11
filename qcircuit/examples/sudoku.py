#!/usr/bin/env python

import qckt
from qckt.backend import *
from qckt import QCktException
import libgrover as grv


inreg = qckt.QRegister(4)
work = qckt.QRegister(4)
outreg = qckt.QRegister(1)
rclreg = qckt.CRegister(4)
nqbits,ncbits,allqreg,allcreg = qckt.placement(outreg,work,inreg,rclreg)

### Sudoku validation circuit
sudo = qckt.QCkt(nqbits,name="Sudoku Validator")
rules = [[0,1],[1,3],[3,2],[2,0]] # rule is that the qubits in a tuple cannot be equal
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

job = qckt.Job(grv_ckt,shots=40)
q = Qeng()
q.runjob(job)
job.plot_counts()
