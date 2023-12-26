import qckt

## Noise
# noise operator (kraus operator) is specified as a sequence of pairs of list of operators. 
# KrausOperator has three fields
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
#   num_target_qubits is the number of qubits this kraus operator acts on
# 

class KrausOperator:
    def __init__(self, name, kraus_op, nqubits):
        self.name = name
        self.kraus_op = kraus_op
        self.nqubits = nqubits

    def __iter__(self):
        self.it = iter(self.kraus_op)
        return self.it
    def __next__(self):
        return next(self.it)

    def __str__(self):
        return f'name={self.name}\nkraus_op={self.kraus_op}\nnqubits={self.nqubits}'

class KrausOperatorSequence:
    def __init__(self, *args):
        self.kraus_op_sequence = []
        for a in args:
            if a is None:
                pass
            elif type(a) is KrausOperator:
                self.add_kraus_op(a)
            elif type(a) is KrausOperatorSequence:
                self.add_kraus_op_sequence(a)
            else:
                raise qckt.QCktException('ERROR: Invalid argument, only KrausOperator and KrausOperatorSeuence objects or None expected')
        self.name = self.__name__()

    def add_kraus_op_sequence(self, kraus_op_sequence):
        if kraus_op_sequence is None:
            addition = []
        elif type(kraus_op_sequence) is KrausOperatorSequence:
            addition = kraus_op_sequence.kraus_op_sequence
        else:
            raise qckt.QCktException('ERROR: KrausOperatorSequence object or None expected')
        self.kraus_op_sequence.extend(addition)
        self.name = self.__name__()

    def add_kraus_op(self, kraus_op):
        if kraus_op is None:
            pass
        elif type(kraus_op) is KrausOperator:
            self.kraus_op_sequence.append(kraus_op)            
        else:
            raise qckt.QCktException('ERROR: KrausOperator object expected')
        self.name = self.__name__()

    def __iter__(self):
        self.it = iter(self.kraus_op_sequence)
        return self.it
    def __next__(self):
        return next(self.it)

    def __name__(self):
        return ','.join([oper.name for oper in self.kraus_op_sequence])

    def __str__(self):
        return self.name

class KrausOperatorApplierSequense:
    def __init__(self, noise_ops=None, qubit_list=None):
        self.name = ''
        self.kraus_op_sequence_applier = []
        if noise_ops is not None:
            if qubit_list is None:
                raise qckt.QCktException('ERROR: qubits list required.')
            self.add(noise_ops, qubit_list)

    def add(self, kraus_ops, qbit_list):
        if kraus_ops is None:
            addition = []
        elif type(kraus_ops) is KrausOperatorSequence:
            addition = [(op,qbit_list) for op in kraus_ops]
        elif type(kraus_ops) is KrausOperator:
            addition = [(kraus_ops, qbit_list)]
        else:
            raise qckt.QCktException('ERROR: KrausOperatorSequence, KrausOperator object or None expected.')
        self.kraus_op_sequence_applier.extend(addition)
        self.name = self.__name__()

    def extend(self, kraus_op_applier_seq):
        if kraus_op_applier_seq is None:
            addition = []
        elif type(kraus_op_applier_seq) is KrausOperatorApplierSequense:
            addition = kraus_op_applier_seq.kraus_op_sequence_applier
        else:
            raise qckt.QCktException('ERROR: KrausOperatorApplierSequense object or None expected')
        self.kraus_op_sequence_applier.extend(addition)
        self.name = self.__name__()

    def new_with_filtered_qubits(self, qubit_list):
        new_noise_op_applier_seq = KrausOperatorApplierSequense()
        for noise_operator,qblist in self.kraus_op_sequence_applier:
            filtered_qbits = [q for q in qblist if q in qubit_list]
            if len(filtered_qbits) > 0:
                new_noise_op_applier_seq.add(noise_operator,filtered_qbits)
        return new_noise_op_applier_seq

    def __name__(self):
        return ','.join([f'({oper.name},{qbits})' for oper,qbits in self.kraus_op_sequence_applier])

    def __iter__(self):
        self.it = iter(self.kraus_op_sequence_applier)
        return self.it
    def __next__(self):
        return next(self.it) 

    def __str__(self):
        return f'{self.name}'


## Noise Model fields
#   kraus_opseq_init: KrausOperatorSequence,
#   kraus_opseq_qubits: KrausOperatorApplierSequence,
#   kraus_opseq_allgates: KrausOperatorSequence,
#
class NoiseModel:
    def __init__(self, kraus_opseq_init=None, kraus_opseq_qubits=None, kraus_opseq_allgates=None):
        self.kraus_opseq_init = kraus_opseq_init
        self.kraus_opseq_qubits = kraus_opseq_qubits
        self.kraus_opseq_allgates = kraus_opseq_allgates
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
        return ['kraus_opseq_init', 'kraus_opseq_qubits', 'kraus_opseq_allgates']
    

## create a KrausOperatorApplierSequence combining all components of noise to be applied when gate is applied on certain qubit_list
#
def consolidate_gate_noise(noise_model, gate_noise, qubit_list):
    noise_op_applier_sequence_overall = KrausOperatorApplierSequense()

    # 1. noise on specific qubits, kraus_opseq_qubits
    noise_op_applier_sequence_qubits = KrausOperatorApplierSequense()
    if noise_model is not None:
        noise_model_qubits = noise_model.kraus_opseq_qubits
        if noise_model_qubits is not None:
            noise_op_applier_sequence_qubits = noise_model_qubits.new_with_filtered_qubits(qubit_list)
    noise_op_applier_sequence_overall.extend(noise_op_applier_sequence_qubits)
    # 2. noise on all gates, kraus_opseq_allgates
    noise_op_applier_sequence_all_gates = KrausOperatorApplierSequense()
    if noise_model is not None:
        noise_model_allgates = noise_model.kraus_opseq_allgates
        noise_op_applier_sequence_all_gates = KrausOperatorApplierSequense(noise_ops=noise_model_allgates, qubit_list=qubit_list)
    noise_op_applier_sequence_overall.extend(noise_op_applier_sequence_all_gates)
    # 3. current gate noise
    noise_op_applier_sequence_this_gate = KrausOperatorApplierSequense()
    if gate_noise is not None:
        if type(gate_noise) is KrausOperator:
            noise_op_applier_sequence_this_gate.add(kraus_ops=KrausOperatorSequence(gate_noise), qbit_list=qubit_list)            
        elif type(gate_noise) is KrausOperatorSequence:
            noise_op_applier_sequence_this_gate.add(kraus_ops=gate_noise, qbit_list=qubit_list)
        else:
            raise qckt.QCktException('ERROR: KrausOperator, KrausOperatorSequence object or None expected.')
    noise_op_applier_sequence_overall.extend(noise_op_applier_sequence_this_gate)

    return noise_op_applier_sequence_overall
