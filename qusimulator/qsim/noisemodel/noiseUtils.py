import qsim

## Noise
# kraus map (noise channel) is specified as a sequence of pairs of list of operators and probabilty factors. 
# NoiseOperator has three fields
#	name,
#   [ (op1,op1_prob_multiplier), (op2,op2_prob_multiplier), ...  ],
#   num_target_qubits
#
#	op is in the same format as gates, i.e., ['name', opmatrix]
#		note that mostly the opmatrix is unitary, but cases such as Amplitude Damping is not [[1.0, 0.0],[0.0, sqrt(gamma)]]
#	op_prob_multiplier gives the noise contribution by this op, i.e., = op_prob_multiplier * (op * state * op_dagger)
#
# so, in math terms, rho = op1_prob_multipier * (op1 * rho * op1_dag) + op2_prob_multiplier * (op2 * rho * op2.dag) + ...
#
#   num_target_qubits is the number of qubits this noise acts on
# 

class qNoiseChannel:
    def __init__(self, name, operator_prob_set, nqubits):
        self.name = name
        self.operator_prob_set = operator_prob_set
        self.nqubits = nqubits

    def __iter__(self):
        self.it = iter(self.operator_prob_set)
        return self.it
    def __next__(self):
        return next(self.it)

    def __str__(self):
        return f'name={self.name}\noperator_prob_set={self.operator_prob_set}\nnqubits={self.nqubits}'

class qNoiseChannelSequence:
    def __init__(self, *args):
        self.noise_channel_sequence = []
        for a in args:
            if a is None:
                pass
            elif type(a) is qNoiseChannel:
                self.add_noise_channel(a)
            elif type(a) is qNoiseChannelSequence:
                self.add_noise_channel_sequence(a)
            else:
                raise qsim.QSimError('ERROR: Invalid argument, only qNoiseChannel and qNoiseChannelSequence objects or None expected')
        self.name = self.__name__()

    def add_noise_channel_sequence(self, noise_channel_sequence):
        if noise_channel_sequence is None:
            addition = []
        elif type(noise_channel_sequence) is qNoiseChannelSequence:
            addition = noise_channel_sequence.noise_channel_sequence
        else:
            raise qsim.QSimError('ERROR: qNoiseChannelSequence object or None expected')
        self.noise_channel_sequence.extend(addition)
        self.name = self.__name__()

    def add_noise_channel(self, noise_channel):
        if noise_channel is None:
            pass
        if type(noise_channel) is  qNoiseChannel:
            self.noise_channel_sequence.append(noise_channel)
        else:
            raise qsim.QSimError('ERROR: qNoiseChannel object or None expected')
        self.name = self.__name__()

    def __iter__(self):
        self.it = iter(self.noise_channel_sequence)
        return self.it
    def __next__(self):
        return next(self.it)

    def __name__(self):
        return ','.join([chan.name for chan in self.noise_channel_sequence])

    def __str__(self):
        return self.name

class qNoiseChannelApplierSequense:
    def __init__(self, noise_chan=None, qubit_list=None):
        self.name = ''
        self.noise_channel_sequence_applier = []
        if noise_chan is not None:
            if qubit_list is None:
                raise qsim.QSimError('ERROR: qubits list required.')
            self.add(noise_chan, qubit_list)

    def add(self, noise_chan, qubit_list):
        if noise_chan is None:
            addition = []
        elif type(noise_chan) is qNoiseChannelSequence:
            addition = [(chan,qubit_list) for chan in noise_chan]
        elif type(noise_chan) is qNoiseChannel:
            addition = [(noise_chan, qubit_list)]
        else:
            raise qsim.QSimError('ERROR: qNoiseChannelSequence, qNoiseChannel object or None expected.')
        self.noise_channel_sequence_applier.extend(addition)
        self.name = self.__name__()

    def extend(self, noise_chan_applier_seq):
        if noise_chan_applier_seq is None:
            addition = []
        elif type(noise_chan_applier_seq) is qNoiseChannelApplierSequense:
            addition = noise_chan_applier_seq.noise_channel_sequence_applier
        else:
            raise qsim.QSimError('ERROR: qNoiseChannelApplierSequense object or None expected')
        self.noise_channel_sequence_applier.extend(addition)
        self.name = self.__name__()

    def new_with_filtered_qubits(self, qubit_list):
        new_noise_chan_applier_seq = qNoiseChannelApplierSequense()
        for noise_channel,qblist in self.noise_channel_sequence_applier:
            filtered_qbits = [q for q in qblist if q in qubit_list]
            if len(filtered_qbits) > 0:
                new_noise_chan_applier_seq.add(noise_channel,filtered_qbits)
        return new_noise_chan_applier_seq

    def __name__(self):
        return ','.join([f'({chan.name},{qbits})' for chan,qbits in self.noise_channel_sequence_applier])

    def __iter__(self):
        self.it = iter(self.noise_channel_sequence_applier)
        return self.it
    def __next__(self):
        return next(self.it) 

    def __str__(self):
        return f'{self.name}'


## Noise Profile fields
#   noise_chan_init: qNoiseChannelSequence,
#   noise_chan_qubits: qNoiseChannelApplierSequense,
#   noise_chan_allgates: qNoiseChannelSequence,
#
class qNoiseProfile:
    def __init__(self, noise_chan_init, noise_chan_qubits, noise_chan_allgates):
        self.noise_chan_init = noise_chan_init
        self.noise_chan_qubits = noise_chan_qubits
        self.noise_chan_allgates = noise_chan_allgates
    def get(self, field, defval):
        print(f'deprecated dict.get(key,default) style access, key={index}.')
        retval = defval
        if hasattr(self, field):
            retval = getattr(self, field)
        return retval
    def __getitem__(self, index):
        print(f'deprecated dict[key] style access, key={index}.')
        return self.get(index,None)
    def keys(self):
        print('deprecated dict.keys() access')
        return ['noise_chan_init', 'noise_chan_qubits', 'noise_chan_allgates']


## create a qNoiseChannelApplierSequense combining all components of noise to be applied when qgate() is called with certain qubit_list
#
def consolidate_gate_noise(noise_profile, gate_noise, qubit_list):
    noise_chan_applier_sequence_overall = qNoiseChannelApplierSequense()

    # 1. noise on specific qubits, noise_chan_qubits
    noise_chan_applier_sequence_qubits = qNoiseChannelApplierSequense()
    if noise_profile is not None:
        noise_profile_qubits = noise_profile.get('noise_chan_qubits', None)
        if noise_profile_qubits is not None:
            noise_chan_applier_sequence_qubits = noise_profile_qubits.new_with_filtered_qubits(qubit_list)
    noise_chan_applier_sequence_overall.extend(noise_chan_applier_sequence_qubits)
    # 2. noise on all gates, noise_chan_allgates
    noise_chan_applier_sequence_all_gates = qNoiseChannelApplierSequense()
    if noise_profile is not None:
        noise_profile_allgates = noise_profile.get('noise_chan_allgates', None)
        noise_chan_applier_sequence_all_gates = qNoiseChannelApplierSequense(noise_chan=noise_profile_allgates, qubit_list=qubit_list)
    noise_chan_applier_sequence_overall.extend(noise_chan_applier_sequence_all_gates)
    # 3. current gate noise
    # Qckt uses its own noise_profile and passes a consolidated noise_applier at qgate invokation
    noise_chan_applier_sequence_this_gate = qNoiseChannelApplierSequense()
    if gate_noise is not None:
        if type(gate_noise) is qNoiseChannel:
            gate_noise_as_chan_seq = qNoiseChannelSequence(gate_noise)
            noise_chan_applier_sequence_this_gate.add(noise_chan=gate_noise_as_chan_seq, qubit_list=qubit_list)
        elif type(gate_noise) is qNoiseChannelSequence:
            noise_chan_applier_sequence_this_gate.add(noise_chan=gate_noise, qubit_list=qubit_list)
        elif type(gate_noise) is qNoiseChannelApplierSequense:
            # quantum computing programming frameworks (e.g., qckt) can combine any noise profile into 'applier sequences'
            # new_with_filtered_qubits() is just a defensive check, it is expected to be a NO-OP if qckt works correctly
            noise_chan_applier_sequence_this_gate = gate_noise.new_with_filtered_qubits(qubit_list=qubit_list)
        else:
            raise qsim.QSimError('ERROR: qNoiseChannelSequence or qNoiseChannelApplierSequense object or None expected.')
    noise_chan_applier_sequence_overall.extend(noise_chan_applier_sequence_this_gate)

    return noise_chan_applier_sequence_overall
