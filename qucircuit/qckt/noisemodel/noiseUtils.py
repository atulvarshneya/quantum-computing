import qckt

## Noise
# noise channel is specified as a sequence of pairs of list of kraus operators and probability factor. 
# NoiseChannel has three fields
#   [ (op1,op1_prob_multiplier), (op2,op2_prob_multiplier), ...  ],
#	name,
#   num_target_qubits
#
#	op is in the same format as gates, i.e., ['name', opmatrix]
#		note that mostly the opmatrix is unitary, but cases such as Amplitude Damping is not [[1.0, 0.0],[0.0, sqrt(gamma)]]
#	op_prob_multiplier gives the noise contribution by this op, i.e., = op_prob_multiplier * (op * state * op_dagger)
#
# so, in math terms, rho = op1_prob_multipier * (op1 * rho * op1_dag) + op2_prob_multiplier * (op2 * rho * op2.dag) + ...
#
#   num_target_qubits is the number of qubits this noise channel acts on
# 

class NoiseChannel:
    def __init__(self, name, noise_chan, nqubits):
        self.name = name
        self.noise_chan = noise_chan
        self.nqubits = nqubits

    def __iter__(self):
        self.it = iter(self.noise_chan)
        return self.it
    def __next__(self):
        return next(self.it)

    def __str__(self):
        return f'name={self.name}\nnoise_chan={self.noise_chan}\nnqubits={self.nqubits}'

class NoiseChannelSequence:
    def __init__(self, *args):
        self.noise_chan_sequence = []
        for a in args:
            if a is None:
                pass
            elif type(a) is NoiseChannel:
                self.add_noise_chan(a)
            elif type(a) is NoiseChannelSequence:
                self.add_noise_chan_sequence(a)
            else:
                raise qckt.QCktException('ERROR: Invalid argument, only NoiseChannel and NoiseChannelSequence objects or None expected')
        self.name = self.__name__()

    def add_noise_chan_sequence(self, noise_chan_sequence):
        if noise_chan_sequence is None:
            addition = []
        elif type(noise_chan_sequence) is NoiseChannelSequence:
            addition = noise_chan_sequence.noise_chan_sequence
        else:
            raise qckt.QCktException('ERROR: NoiseChannelSequence object or None expected')
        self.noise_chan_sequence.extend(addition)
        self.name = self.__name__()
        return self

    def add_noise_chan(self, noise_chan):
        if noise_chan is None:
            pass
        elif type(noise_chan) is NoiseChannel:
            self.noise_chan_sequence.append(noise_chan)            
        else:
            raise qckt.QCktException('ERROR: NoiseChannel object expected')
        self.name = self.__name__()
        return self

    def __iter__(self):
        self.it = iter(self.noise_chan_sequence)
        return self.it
    def __next__(self):
        return next(self.it)

    def __name__(self):
        return ','.join([chan.name for chan in self.noise_chan_sequence])

    def __str__(self):
        return self.name

class NoiseChannelApplierSequense:
    def __init__(self, noise_chan=None, qubit_list=None):
        self.name = ''
        self.noise_chan_applier_sequence = []
        if noise_chan is not None:
            if qubit_list is None:
                raise qckt.QCktException('ERROR: qubits list required.')
            self.add(noise_chan, qubit_list)

    def add(self, noise_chan, qbit_list):
        if noise_chan is None:
            addition = []
        elif type(noise_chan) is NoiseChannelSequence:
            addition = [(chan,qbit_list) for chan in noise_chan]
        elif type(noise_chan) is NoiseChannel:
            addition = [(noise_chan, qbit_list)]
        else:
            raise qckt.QCktException('ERROR: NoiseChannelSequence, NoiseChannel object or None expected.')
        self.noise_chan_applier_sequence.extend(addition)
        self.name = self.__name__()
        return self

    def extend(self, noise_chan_applier_seq):
        if noise_chan_applier_seq is None:
            addition = []
        elif type(noise_chan_applier_seq) is NoiseChannelApplierSequense:
            addition = noise_chan_applier_seq.noise_chan_applier_sequence
        else:
            raise qckt.QCktException('ERROR: NoiseChannelApplierSequense object or None expected')
        self.noise_chan_applier_sequence.extend(addition)
        self.name = self.__name__()
        return self

    def new_with_filtered_qubits(self, qubit_list):
        new_noise_chan_applier_seq = NoiseChannelApplierSequense()
        for noise_channel,qblist in self.noise_chan_applier_sequence:
            filtered_qbits = [q for q in qblist if q in qubit_list]
            if len(filtered_qbits) > 0:
                new_noise_chan_applier_seq.add(noise_channel,filtered_qbits)
        return new_noise_chan_applier_seq

    def __name__(self):
        return ','.join([f'({chan.name},{qbits})' for chan,qbits in self.noise_chan_applier_sequence])

    def __iter__(self):
        self.it = iter(self.noise_chan_applier_sequence)
        return self.it
    def __next__(self):
        return next(self.it) 

    def __str__(self):
        return f'{self.name}'


class NoiseProfile:
    def __init__(self, noise_chan_init=None, noise_chan_qubits=None, noise_chan_allgates=None, noise_chan_allsteps=None):
        self.noise_chan_init = noise_chan_init
        self.noise_chan_qubits = noise_chan_qubits
        self.noise_chan_allgates = noise_chan_allgates
        self.noise_chan_allsteps = noise_chan_allsteps
    def get(self, field, defval):
        print(f'deprecated dict.get(key,default) style access, key={field}.')
        retval = defval
        if hasattr(self, field):
            retval = getattr(self, field)
        return retval
    def __getitem__(self, index):
        print(f'deprecated dict[key] style access, key={index}.')
        return self.get(index,None)
    def keys(self):
        print('deprecated dict.keys() access')
        return ['noise_chan_init', 'noise_chan_qubits', 'noise_chan_allgates', 'noise_chan_allsteps']
    

## create a NoiseChannelApplierSequence combining all components of noise to be applied when gate is applied on certain qubit_list
#
def consolidate_gate_noise(noise_profile, gate_noise, qubit_list):
    noise_chan_applier_sequence_overall = NoiseChannelApplierSequense()

    # 1. noise on specific qubits, noise_chan_qubits
    noise_chan_applier_sequence_qubits = NoiseChannelApplierSequense()
    if noise_profile is not None:
        noise_profile_qubits = noise_profile.noise_chan_qubits
        if noise_profile_qubits is not None:
            noise_chan_applier_sequence_qubits = noise_profile_qubits.new_with_filtered_qubits(qubit_list)
    noise_chan_applier_sequence_overall.extend(noise_chan_applier_sequence_qubits)
    # 2. noise on all gates, noise_chan_allgates
    noise_chan_applier_sequence_all_gates = NoiseChannelApplierSequense()
    if noise_profile is not None:
        noise_profile_allgates = noise_profile.noise_chan_allgates
        noise_chan_applier_sequence_all_gates = NoiseChannelApplierSequense(noise_chan=noise_profile_allgates, qubit_list=qubit_list)
    noise_chan_applier_sequence_overall.extend(noise_chan_applier_sequence_all_gates)
    # 3. current gate noise
    noise_chan_applier_sequence_this_gate = NoiseChannelApplierSequense()
    if gate_noise is not None:
        if type(gate_noise) is NoiseChannel:
            noise_chan_applier_sequence_this_gate.add(noise_chan=NoiseChannelSequence(gate_noise), qbit_list=qubit_list)            
        elif type(gate_noise) is NoiseChannelSequence:
            noise_chan_applier_sequence_this_gate.add(noise_chan=gate_noise, qbit_list=qubit_list)
        else:
            raise qckt.QCktException('ERROR: NoiseChannel, NoiseChannelSequence object or None expected.')
    noise_chan_applier_sequence_overall.extend(noise_chan_applier_sequence_this_gate)

    return noise_chan_applier_sequence_overall
