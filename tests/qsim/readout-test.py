import qsim

print()
print("Apply H on 0 then C on 0,3 then Measure 0")

# Test 01
print("Test 01:")
qc = qsim.QSimulator(8,qtrace=True)
qc.qgate(qsim.H(),[0])
qc.qgate(qsim.C(),[0,3])
qc.qreadout(nshots=1000)

_,_,cregcounts,_ = qc.qsnapshot()
c0 = cregcounts.get(0,0)
c9 = cregcounts.get(9,0)
print("creg_counts[0] + creg_counts[9] =",c0 + c9)  # Must add to nshots = 1000
# check creg_counts[0] is 500 +/- 50
if c0 > (500 - 50) and c0 < (500+50):
	print("creg_counts[0] is within range.")
else:
	print("creg_counts[0] not within range -- FAILED.")
# check creg_counts[9] is 500 +/- 50
if c9 > (500 - 50) and c9 < (500+50):
	print("creg_counts[9] is within range.")
else:
	print("creg_counts[9] not within range -- FAILED.")
print()



# Test 02
print("Test 02:")
qc = qsim.QSimulator(8)
qc.qgate(qsim.H(),[0])
qc.qgate(qsim.C(),[0,3])
qc.qmeasure([0])
qc.qreadout(nshots=1000)

_,_,cregcounts,_ = qc.qsnapshot()
c0 = cregcounts.get(0,0)
c9 = cregcounts.get(9,0)
print("creg_counts[0] + creg_counts[9] =",c0 + c9)  # Must add to nshots = 1000
# check creg_counts[0] or creg_counts[9] is 1000
if (c0 == 1000 and c9 == 0) or (c0 == 0 and c9 == 1000):
	print("only one of creg_counts[0] and creg_counts[9] is 1000.")
else:
	print("only one of creg_counts[0] and creg_counts[9] should be 1000 -- FAILED.")
print()



# Test 03
print("Test 03:")
qc = qsim.QSimulator(8)
qc.qgate(qsim.H(),[0])
qc.qgate(qsim.C(),[0,3])
qc.qmeasure([0])
qc.qreadout()

_,_,cregcounts,_ = qc.qsnapshot()
c0 = cregcounts.get(0,0)
c9 = cregcounts.get(9,0)
print("creg_counts[0] + creg_counts[9] =",c0 + c9)  # Must add to nshots = 1
# check creg_counts[0] or creg_counts[9] is 1
if (c0 == 1 and c9 == 0) or (c0 == 0 and c9 == 1):
	print("only one of creg_counts[0] and creg_counts[9] is 1.")
else:
	print("only one of creg_counts[0] and creg_counts[9] should be 1 -- FAILED.")
