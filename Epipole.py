import numpy as np


def nullspace(A, atol=1e-13, rtol=0):
    u, d, v = np.linalg.svd(A)
    rank = (d>1e-13).sum()
    e = v[rank:].conj().T
    return(e/e[2])

def findEpipole(A):
	return nullspace(A.T)

if __name__ == "__main__":
	F = np.array([[-1.29750186e-06,  8.07894025e-07,  1.84071967e-03],
		[3.54098411e-06,  1.05620725e-06, -8.90168709e-03],
		[-3.29878312e-03,  5.14822628e-03,  1.00000000e+00]])
	print(findEpipole(F))
