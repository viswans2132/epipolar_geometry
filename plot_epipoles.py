import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import Epipole

def loadData(filename):
	condition = False
	p1 = np.empty((0,2))
	p2 = np.empty((0,2))
	F = np.empty((0,3))
	with open(filename) as file:
		lines = file.readlines()
		for i, line in enumerate(lines):
			if "img-1" in line:
				condition = True
				j = i+1
				while(condition):
					numbers = lines[j].replace('[','').replace(']','').split(',')[0].split()
					if "img-2" in lines[j]:
						condition = False
						break
					if len(numbers)==2:						
						p1 = np.vstack((p1, numbers))
					j+=1

			if "img-2" in line:
				condition = True
				j = i+1
				while(condition):
					numbers = lines[j].replace('[','').replace(']','').split(',')[0].split()
					if "F" in lines[j]:
						condition = False
						break
					if len(numbers)==2:						
						p2 = np.vstack((p2, numbers))
						
					j+=1

			if "F" in line:
				condition = True
				j = i+1
				while(condition):
					try:
						numbers = lines[j].replace('[','').replace(']','').split(',')[0].split()
						if len(numbers)==3:						
							F = np.append(F, numbers)
						j+=1
					except IndexError:
						break
	return p1.T.astype(np.float32), p2.T.astype(np.float32), F.reshape(-1,3).astype(np.float32)

def plot(F, XH, X2, e, img):
	start = 0
	end = img.shape[1] - 1
	if e[0] < start:
		start = e[0] - 1000
	if e[0] > end:
		end = e[0] + 1000

	l = np.array([F.dot(XH.T[i].reshape(3,1)) for i in range(10)]).reshape(10,3).T
	xline = np.vstack((start*np.ones(10), end*np.ones(10))).T
	yline = np.array([-(l[0,i]*xline[i] + l[2,i])/l[1,i] for i in range(10)])

	fig=plt.figure(figsize=(18, 16), dpi= 80, facecolor='w', edgecolor='k')
	plt.imshow(img)
	plt.scatter(X2[0],X2[1], c='red')
	plt.scatter(e[0],e[1], c='black')

	for i in range(10):
	    plt.plot(xline[i].reshape(2,), yline[i].reshape(2,), color='red')
	    pass
	    
	plt.show()


if __name__=="__main__":
	X1, X2, F21 = loadData('data.txt')
	F12 = F21.T
	print(X1)

	X1H = np.append(X1,np.ones((1,10)), axis=0)
	X2H = np.append(X2,np.ones((1,10)), axis=0)

	e2 = Epipole.findEpipole(F12)
	e1 = Epipole.findEpipole(F21)
	img1=mpimg.imread('img1.jpg')
	img2=mpimg.imread('img2.jpg')
	
	plot(F21, X1H, X2H, e1, img2)
	plot(F12, X2H, X1H, e2, img1)

