import matplotlib.pyplot as plt
import numpy as np
import csv
import random

x = []
y = []

yMin = -100
yMax = 200
yInt = 0
points = 50
degree = 4
noise = 10**degree
coef = [2,-120, 37,-4,25,3,0]

f = open('points.csv', 'w')
writer = csv.DictWriter(f, fieldnames=['x', 'y'])
writer.writeheader()

for i in np.arange(yMin, yMax, (yMax - yMin)/points):
    result = yInt
    for j in range(0, degree+1):
        if j < len(coef):
            result += coef[j]*i**(degree-j) + 2*noise*random.uniform(0,1)
    y.append(result)
    x.append(i)
    print(result)
    writer.writerow({'x': str(i), 'y': result})

plt.plot(x, y)
plt.show()