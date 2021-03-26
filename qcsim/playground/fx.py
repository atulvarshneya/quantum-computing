#!/usr/bin/python

import qclib

NQUBITS = 4
verbose = 0

def fx(qc):
	for i in range(NQUBITS-1):
		qc.qgate(qc.C(),[i+1,0])
	if verbose:
		qc.qreport(header="After f(x)")

def hnx(qc):
	for i in range(NQUBITS-1):
		qc.qgate(qc.H(),[i+1])
	if verbose:
		qc.qreport(header="After Hnx")

def measure_fx(qc):
	qc.qmeasure([0])
	if verbose:
		qc.qreport(header="After measureing f(x)")

def measure_x(qc):
	qc.qmeasure([ i for i in range(1,NQUBITS)])
	if verbose:
		qc.qreport(header="After measuring x")

# ===============================================

qc = qclib.qcsim(NQUBITS)

for i in range(16):
		qc.qreset()
		hnx(qc)
		fx(qc)
		# measure_fx(qc)
		hnx(qc)
		measure_x(qc)
		qc.qreport(header = "=================================")
