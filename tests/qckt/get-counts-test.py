
# test get_counts(register)

import qckt
import qckt.backend as bknd

ckt = qckt.QCkt(3,3)
ckt.X(0)
ckt.H(1)
ckt.CX(1,2)
ckt.draw()

job = qckt.Job(ckt, shots=100)
bk = bknd.Qeng()
bk.runjob(job)

print("The only states produced are 001 (1) and 111 (7)")
counts = job.get_counts()
# since get_counts() returns dict with only those states that have non-zero counts
# hence for following, only 1 and 7 are expected to be printed
for s in sorted(counts.keys()):
    print(s)
print("So, counts for state 011 (counts.get(3,0)) - expected as 0")
print(counts.get(3,0))

print("and, counts for get_count(register=[0]) - expected {1: 100} because shots=100")
counts = job.get_counts(register=[0])
print(counts)