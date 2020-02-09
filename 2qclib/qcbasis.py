

# Basis Matrices
def BELL_BASIS(self):
	return np.matrix([[1,0,0,1],[1,0,0,-1],[0,1,1,0],[0,1,-1,0]], dtype=complex)/np.sqrt(2)

def HDM_BASIS(self):
	sq2 = np.sqrt(2)
	return np.matrix([[1,1],[1,-1]], dtype=complex)/np.sqrt(2)

