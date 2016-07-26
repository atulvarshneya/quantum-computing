

import qclib

vec_x_sz = 6 # size of the vector |x>
qc = qclib.qcsim(vec_x_sz+1)

code_fmt = "{:0"+"{:d}".format(vec_x_sz)+"b}"

def get_fx():
	secret_code = 0b11101
	print "Pssst... the secret code is ",code_fmt.format(secret_code)
	fx_oplist = []
	for i in range(vec_x_sz):
		if secret_code & (0x1<<i):
			sn_optep = qc.qstretch(qc.C(),[i,vec_x_sz])
			fx_oplist.append(sn_optep)
	fx = qc.qcombine_seq("FX",fx_oplist)
	return fx
print "Getting the secret function box..."
fx = get_fx()
print "OK, FX is ready."

###########################################################################
## Start of the Bernstien-Vazirani algorithm
###########################################################################
print
print "Starting the VB algorithm..."

###########################################################################
# Step 0: Prepare the result bit |b> to |->
qc.qgate(qc.X(),[vec_x_sz])
qc.qgate(qc.H(),[vec_x_sz])
print "Step 0: Preparing |b> as |->"

###########################################################################
## Step 1: Apply H on all qbits of |x>
for i in range(vec_x_sz):
	qc.qgate(qc.H(),[i])
print "Step 1: Applied H to all |x> qbits"

###########################################################################
## Step 2: Now apply the secret function f()
qbit_list = range(vec_x_sz+1)
qbit_list.reverse()
qc.qgate(fx,qbit_list)
print "Step 2: Applied FX to |b>|x>"

###########################################################################
## Step 3: Again apply H on all qbits of |x>
for i in range(vec_x_sz):
	qc.qgate(qc.H(),[i])
print "Step 3: Again Applied H to all |x> qbits"

###########################################################################
## Step 4: Measure all qbits of |x>
v = qc.qmeasure(range(vec_x_sz)) # this will give [LSB, ..., MSB]
res = 0
for i in range(vec_x_sz):
	res += (v[i] << i)
print "Step 4: Measured all qbits of |x>"

print "Result = "+code_fmt.format(res)
