import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from matplotlib import style
style.use("ggplot")

X = np.array([[1,1.5],
				[7,9],
				[0.6,1.1],
				[1.5,1.7],
				[10,11],
				[8,8.5]])

Y = [-1,1,-1,-1,1,1]

clf = svm.SVC(kernel = 'linear')
clf.fit(X,Y)

print clf.predict([2,2])

w = clf.coef_[0]
a = -w[0]/w[1]

x = np.linspace(0,12)
y = a*x - clf.intercept_[0] / w[1]

h = plt.plot(x, y, 'k-', label="non weighted div")
# k- is for black color
plt.scatter(X[:,0], X[:,1], c=y)
# c is also for color only
plt.legend()
plt.show()
