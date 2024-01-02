
from qsim.qSimException import QSimError
from qsim.Qsim import QSimulator
from qsim.DMQsim import DMQSimulator
from qsim.qgates import X, Y, Z, H, Rphi, Rk, SQSWAP, SWAP, CSWAP, QFT, Hn, RND, CTL, C, T, BELL_BASIS, HDM_BASIS
from qsim.qgatesUtils import qcombine_seq, qcombine_par

__version__ = '2.0'
__author__ = 'Atul Varshneya'
__author_email__ = 'atul.varshneya@gmail.com'
__email__ = __author_email__
__url__ = 'https://github.com/atulvarshneya/quantum-computing'
