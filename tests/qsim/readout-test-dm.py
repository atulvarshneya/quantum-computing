import qsim

print()
print("Apply H on 0 then C on 0,3 then Measure 0")

# Test 01
print("Test 01:")
qc = qsim.DMQSimulator(8,qtrace=True)
qc.qgate(qsim.H(),[0])
qc.qgate(qsim.C(),[0,3])
qc.qreadout(nshots=1000)

_,_,cregcounts,_ = qc.qsnapshot()
c0 = cregcounts[0]
c9 = cregcounts[9]
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
qc = qsim.DMQSimulator(8)
qc.qgate(qsim.H(),[0])
qc.qgate(qsim.C(),[0,3])
qc.qmeasure([0])
qc.qreadout(nshots=1000)

_,_,cregcounts,_ = qc.qsnapshot()
c0 = cregcounts[0]
c9 = cregcounts[9]
print("creg_counts[0] + creg_counts[9] =",c0 + c9)  # Must add to nshots = 1000
# check creg_counts[0] or creg_counts[9] is 1000
if (c0 == 1000 and c9 == 0) or (c0 == 0 and c9 == 1000):
	print("only one of creg_counts[0] and creg_counts[9] is 1000.")
else:
	print("only one of creg_counts[0] and creg_counts[9] should be 1000 -- FAILED.")
print()



# Test 03
print("Test 03:")

qc = qsim.DMQSimulator(8)
qc.qgate(qsim.H(),[0])
qc.qgate(qsim.C(),[0,3])
qc.qmeasure([0])
qc.qreadout()

_,_,cregcounts,_ = qc.qsnapshot()
c0 = cregcounts[0]
c9 = cregcounts[9]
print("creg_counts[0] + creg_counts[9] =",c0 + c9)  # Must add to nshots = 1
# check creg_counts[0] or creg_counts[9] is 1
if (c0 == 1 and c9 == 0) or (c0 == 0 and c9 == 1):
	print("only one of creg_counts[0] and creg_counts[9] is 1.")
else:
	print("only one of creg_counts[0] and creg_counts[9] should be 1 -- FAILED.")
print()


## Now some noise related tests
import qsim.noisemodel as nmdl

# Test 04
print("Test 04:")
# Adding small noise

noise_ops = nmdl.bit_flip(probability=0.0025)
noise_all_gates = nmdl.qNoiseChannelSequence(noise_ops)
noise_model = {
	'noise_chan_allgates': noise_all_gates
}

qc = qsim.DMQSimulator(2,noise_profile=noise_model, qtrace=True, verbose=True)
qc.qgate(qsim.H(),[0])
qc.qgate(qsim.C(),[0,1])
qc.qreadout(nshots=1000)

_,_,cregcounts,_ = qc.qsnapshot()
c0 = cregcounts[0]
c1 = cregcounts[1]
c2 = cregcounts[2]
c3 = cregcounts[3]
# print("creg_counts:",cregcounts)
print("creg_counts[0] + creg_counts[1] + creg_counts[2] + creg_counts[3] =",c0 + c1 + c2 + c3)  # Must add to nshots = 1000

# Check there is indeed some little noise added
if c1 > 0 or c2 > 0:
	print("Some noise detected in creg_counts[1] or creg_counts[2].")
else:
	print("No noise detected -- FAILED.")

# check the noise is not too much either
if c1 < 15 and c2 < 15:
	print("Noise within range.")
else:
	print("Noise too high -- FAILED.")

# Check c0 and c3 counts are still within reasonable range
if c0 > (500 - 65) and c0 < (500+65):
	print("creg_counts[0] is within range.")
else:
	print("creg_counts[0] not within range -- FAILED.")
if c3 > (500 - 65) and c3 < (500+65):
	print("creg_counts[3] is within range.")
else:
	print("creg_counts[3] not within range -- FAILED.")

print()


# Test 05
print("Test 05:")
# Adding significant noise

noise_ops = nmdl.bit_flip(probability=0.25)
noise_all_gates = nmdl.qNoiseChannelSequence(noise_ops)
noise_model = {
	'noise_chan_allgates': noise_all_gates
}

qc = qsim.DMQSimulator(2,noise_profile=noise_model, qtrace=True, verbose=True)
qc.qgate(qsim.H(),[0])
qc.qgate(qsim.C(),[0,1])
qc.qreadout(nshots=1000)

_,_,cregcounts,_ = qc.qsnapshot()
c0 = cregcounts[0]
c1 = cregcounts[1]
c2 = cregcounts[2]
c3 = cregcounts[3]
# print("creg_counts:",cregcounts)
print("creg_counts[0] + creg_counts[1] + creg_counts[2] + creg_counts[3] =",c0 + c1 + c2 + c3)  # Must add to nshots = 1000

# Check there is indeed some little noise added
if c1 > 0 or c2 > 0:
	print("Some noise detected in creg_counts[1] or creg_counts[2].")
else:
	print("No noise detected -- FAILED.")

# check the noise is high enough
if c1 > 100 and c2 > 100:
	print("Readout shows noise is high enough.")
else:
	print("Readout does not show noise high enough -- FAILED.")

print()