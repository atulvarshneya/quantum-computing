

import qckt
import qckt.backend as bknd

ckt = qckt.QCkt(3,3)
ckt.H([0])
ckt.CX(0,1)
for _ in range(10):
    # basically run a few times till we get 1 count for 00 and 1 count for 11 state
    job = qckt.Job(ckt, shots=2)
    bk = bknd.Qdeb()
    bk.runjob(job)
    counts = job.get_counts()
    if counts.get(0,0) == 1:
        break
print("RESULT:")
job.plot_counts()


ckt = qckt.QCkt(3,3)
ckt.X([0])
job = qckt.Job(ckt, shots=10)
bk = bknd.Qdeb()
bk.runjob(job)

print("RESULT:")
job.plot_counts(verbose=True)