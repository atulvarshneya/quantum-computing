#!/usr/bin/env python

import qckt
import qckt.backend as bknd
import qckt.noisemodel as ns

def ghz_ck(n_qubits: int):
    ck = qckt.QCkt(n_qubits, n_qubits)
    ck.H(0)
    for ii in range(0, n_qubits-1):
        ck.CX(ii,ii+1)
	# For multiple shots leverage the inherent READOUT instead of M
    # ck.M(list(range(n_qubits)))
    return ck

print('bit_flip')
ck = ghz_ck(3)
noiseop = ns.bit_flip(0.1)
noise_profile = ns.NoiseProfile(noise_chan_allgates=ns.NoiseChannelSequence(noiseop))
ck.set_noise_profile(noise_profile=noise_profile)
ck.draw()
shots = 10000
job = qckt.Job(ck, shots=shots)
bk = bknd.DMQeng()
bk.runjob(job=job)
creg_counts = job.get_counts()
creg_pct = [float(ct)/shots for ct in creg_counts]
# print(creg_pct)

expected_pct = [
    0.33300000,
    0.07700000,
    0.04500000,
    0.04500000,
    0.04500000,
    0.04500000,
    0.07700000,
    0.33300000,
    ]

# basic sanity test
allerrors = []
margin_allowed = 0.1
looksgood = True
for i,e in enumerate(expected_pct):
    errval = abs(creg_pct[i]-e)/e
    allerrors.append(errval)
    if errval > margin_allowed:
        looksgood = False

print(f'Measurements within margin of error? {looksgood}')
if not looksgood:
    print('Errors in %')
    for i,e in enumerate(allerrors):
        print(f'  {i:03b} {e*100:.2f}%')

# Expected measurements
# 000  0.33300000+0.00000000j
# 001  0.07700000+0.00000000j
# 010  0.04500000+0.00000000j
# 011  0.04500000+0.00000000j
# 100  0.04500000+0.00000000j
# 101  0.04500000+0.00000000j
# 110  0.07700000+0.00000000j
# 111  0.33300000+0.00000000j
