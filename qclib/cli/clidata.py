import qclib
igbld = [
	"qclib.qcsim.qzerosON",
	"qclib.qcsim.qsize",
	"qclib.qcsim.qreport",
	"qclib.qcsim.qstate",
	"qclib.qcsim._qcsim__stretched_mat",
	"qclib.qcsim.Rphi",
	"qclib.qcsim.qisunitary",
	"qclib.qcsim.CTL",
	"qclib.qcsim.__init__",
	"qclib.qcsim.Rk",
	"qclib.qcsim.qmeasure",
	"qclib.qcsim.qgate",
	"qclib.qcsim.qstretch",
	"qclib.qcsim._qcsim__rmat_rrmat",
	"qclib.qcsim._qcsim__qbit_realign_list",
	"qclib.qcsim.BELL_BASIS",
	"qclib.qcsim._qcsim__valid_qbit_list",
	"qclib.qcsim.qinverse",
	"qclib.qcsim.QFT",
	"qclib.qcsim._qcsim__aligned_op",
	"qclib.qcsim.qtraceON",
	"qclib.qcsim.HDM_BASIS",
	"qclib.qcsim.qreset",
	"qclib.qcsim.qcombine_seq",
	"qclib.qcsim.qcombine_par",
	"qclib.qcsim._qcsim__shuffled_count"
	]
qcbld = {
	"qclib.qcsim.CSWAP": ["csw","Gate: csw cbit bit1 bit2","qgate:3"],
	"qclib.qcsim.SWAP": ["sw","Gate: sw bit1 bit2","qgate:2"],
	"qclib.qcsim.RND": ["rnd","Gate: rnd bit","qgate:1"],
	"qclib.qcsim.Y": ["y","Gate: y bit","qgate:1"],
	"qclib.qcsim.X": ["x","Gate: x bit","qgate:1"],
	"qclib.qcsim.Z": ["z","Gate: z bit","qgate:1"],
	"qclib.qcsim.T": ["t","Gate: t cbit1 cbit2 bit","qgate:3"],
	"qclib.qcsim.SQSWAP": ["sqsw","Gate: sqsw bit1 bit2","qgate:2"],
	"qclib.qcsim.C": ["c","Gate: c cbit bit","qgate:2"],
	"qclib.qcsim.H": ["h","Gate: h bit","qgate:1"]
	}
clidata = {
	"csw": [qclib.qcsim.CSWAP,"Gate: csw cbit bit1 bit2","qgate:3"],
	"sw": [qclib.qcsim.SWAP,"Gate: sw bit1 bit2","qgate:2"],
	"rnd": [qclib.qcsim.RND,"Gate: rnd bit","qgate:1"],
	"y": [qclib.qcsim.Y,"Gate: y bit","qgate:1"],
	"x": [qclib.qcsim.X,"Gate: x bit","qgate:1"],
	"z": [qclib.qcsim.Z,"Gate: z bit","qgate:1"],
	"t": [qclib.qcsim.T,"Gate: t cbit1 cbit2 bit","qgate:3"],
	"sqsw": [qclib.qcsim.SQSWAP,"Gate: sqsw bit1 bit2","qgate:2"],
	"c": [qclib.qcsim.C,"Gate: c cbit bit","qgate:2"],
	"h": [qclib.qcsim.H,"Gate: h bit","qgate:1"]
	}
