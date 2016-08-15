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
	"qclib.qcsim.CSWAP": ["csw","csw cbit bit1 bit2","list:3"],
	"qclib.qcsim.SWAP": ["sw","sw bit1 bit2","list:2"],
	"qclib.qcsim.RND": ["rnd","rnd bit","list:1"],
	"qclib.qcsim.Y": ["y","y bit","list:1"],
	"qclib.qcsim.H": ["h","h bit","list:1"],
	"qclib.qcsim.Z": ["z","z bit","list:1"],
	"qclib.qcsim.T": ["t","t cbit1 cbit2 bit","list:3"],
	"qclib.qcsim.SQSWAP": ["sqsw","sqsw bit1 bit2","list:2"],
	"qclib.qcsim.C": ["c","c cbit bit","list:2"],
	"qclib.qcsim.X": ["x","x bit","list:1"]
	}
qcdata = {
	"csw": [qclib.qcsim.CSWAP,"csw cbit bit1 bit2","list:3"],
	"sw": [qclib.qcsim.SWAP,"sw bit1 bit2","list:2"],
	"rnd": [qclib.qcsim.RND,"rnd bit","list:1"],
	"y": [qclib.qcsim.Y,"y bit","list:1"],
	"h": [qclib.qcsim.H,"h bit","list:1"],
	"z": [qclib.qcsim.Z,"z bit","list:1"],
	"t": [qclib.qcsim.T,"t cbit1 cbit2 bit","list:3"],
	"sqsw": [qclib.qcsim.SQSWAP,"sqsw bit1 bit2","list:2"],
	"c": [qclib.qcsim.C,"c cbit bit","list:2"],
	"x": [qclib.qcsim.X,"x bit","list:1"]
	}
