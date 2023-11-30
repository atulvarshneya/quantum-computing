import math
import qsim
import numpy as np

## Noise
# kraus channel is specified as a sequence of pairs of series of operations, and a state probability multiplier
# 	= (operations_seq,state_prob_multiplier)
#	= (
#		  [ (op1,prob1_mult), (op2,prob2_mult), ...  ],
#		  state_prob_multiplier
#	  )
#
# operations_seq = [(op1,op_prob_multiplier), (op2,op_prob_multiplier), ...]
#	op is in the same format as gates, i.e., ['name', opmatrix]
#		note that mostly the opmatrix is unitary, but cases such as Amplitude Damping is not [[1.0, 0.0],[0.0, sqrt(gamma)]]
#	op_prob_multiplier is gives the noise contribution by this op, i.e., = op_prob_multiplier * (op * state * op.dagger)
# state_prob_multiplier is the factor by which state is multiplied when noise is added
#	typically, state_prob_multiplier = 1 - sum(op_prob_multiplier)
#	however, in some cases, e.g., Amplitude Damping, the operator itself gives the state with noise added
#   	so in those cases the state_prob_multiplier will be 0.0; and op_orob_multiplier for those ops will be 1.0
#
# so, in math terms, rho = state_prob_multiplier * rho + prob1_mult * (op1 * rho * op1.dag) + prob2_mult * (op2 * rho * op2.dag) + ...
#
#                                                        |---------------------------- noise_add --------------------------------------|

# Canned noise channels
def bit_flip(s=0.05):
    return ([(qsim.X(),s)],(1-s))


def phase_flip(s=0.05):
    return ([(qsim.Z(),s)],(1-s))


def depolarizing(s=0.05):
    return ([(qsim.X(),s/3.0),(qsim.Y(),s/3.0),(qsim.Z(),s/3.0)],(1-s))


def amplitude_damping(gamma=0.05):
    AD_K1 = ['K1',np.matrix([[1.0,0.0],[0.0,math.sqrt(1-gamma)]], dtype=complex)]
    AD_K2 = ['K2',np.matrix([[0.0,math.sqrt(gamma)],[0.0,0.0]], dtype=complex)]
    return ([(AD_K1,1.0),(AD_K2,1.0)],0.0)


def phase_damping(gamma=0.05):
    PD_K0 = ['K0',np.matrix([[1.0,0.0],[0.0,math.sqrt(1-gamma)]], dtype=complex)]
    PD_K1 = ['K1',np.matrix([[0.0,0.0],[0.0,math.sqrt(gamma)]], dtype=complex)]
    return ([(PD_K0,1.0),(PD_K1,1.0)],0.0)


def pauli_channel(px=0.05, py=0.05, pz=0.05):
    return ([(qsim.X(),px),(qsim.Y(),py),(qsim.Z(),pz)],(1-px-py-pz))


# !!! Kraus operators normalization condition fails for Generalized Amplitude Damping
def generalized_amplitude_damping(gamma):
    print('Generalized Amplitude Damping is in EXPERIMENTAL stage, expected to fail sometimes.')
    GAD_K0 = ['K0',math.sqrt(p)*np.matrix([[1.0,0.0],[0.0,math.sqrt(1-gamma)]], dtype=complex)]
    GAD_K1 = ['K1',math.sqrt(p)*np.matrix([[1.0,math.sqrt(gamma)],[0.0,0.0]], dtype=complex)]
    GAD_K2 = ['K2',math.sqrt(1-p)*np.matrix([[math.sqrt(1-gamma),0.0],[0.0,1.0]], dtype=complex)]
    GAD_K3 = ['K3',math.sqrt(1-p)*np.matrix([[0.0,0.0],[math.sqrt(gamma),0.0]], dtype=complex)]
    return ([(GAD_K0,1.0),(GAD_K1,1.0),(GAD_K2,1.0),(GAD_K3,1.0)],0.0)


kraus_channels = {
    'BitFlip': bit_flip,
    'PhaseFlip': phase_flip,
    'Depolarizing': depolarizing,
    'AmplitudeDamping': amplitude_damping,
    # 'GeneralizedAmplitudeDamping': generalized_amplitude_damping,
    'PhaseDamping': phase_damping,
    'PauliChannel': pauli_channel,
    }


def kraus_channel_list():
    return kraus_channels.keys()


def kraus_channel_spec(kraus_channel_name):
    return kraus_channels[kraus_channel_name]