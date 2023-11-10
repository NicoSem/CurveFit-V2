import matplotlib.pyplot as plt
import numpy as np
import csv
import random
import sys


x = []
x2 = []
y = []
y2 = []
p = []
size = 10
cRange = 100
iterations = 100
mutateChance = 0.5
mutateMax = 10
norm = 0
maxDegree = 20


def sum(a):
    result = 0
    for i in a:
        result += abs(i)
    return result


def calcError(c, x, y, d):
    err = 0
    #print(c)
    for i in range(0, len(x)):
        result = c[len(c)-1]
        for j in range(1, d):
            result += c[j]*x[i]**(d-j)
        err += (y[i] - result)**2 + norm*sum(c)
    return err


def calcValues(c, x, d):
    err = 0
    for i in range(0, len(x)):
        result = c[len(c)-1]
        for j in range(1, d):
            result += c[j]*x[i]**(d-j)
        y2.append(result)
    return y2


def rank(r):
    #print("a" + str(len(r)))
    
    for i in range(0,len(r)-1):
        s = len(r)
        a = r.pop(i)
        #print(a)
        for j in range(0,len(r)-1):
            if a[0] < p[j][0]:
                r.insert(j, a)
                break
        if len(r) < s:
            r.append(a)
    #print("b" + str(len(r)))
    return r


def breed(a, b, d):
    c = [0]
    #print('degree ' + str(d))
    for i in range(1, d+2):
        #print(i)
        c.append((a[i] + b[i])/2)
    if(random.uniform(0,1) > mutateChance):
        c[random.randint(1,len(c)-1)] *= -mutateMax + 2*mutateMax*random.uniform(0,1)
    c[0] = calcError(c, x, y, d)
    return c


def gen(d):
    c = [0]
    for i in range(0, d+1):
        c.append(random.randint(-cRange,cRange))
    c[0] = calcError(c, x, y, d)
    return c

def printPoly(c):
    result = 'y = '
    for i in range(1, len(c)-2):
        result += str(c[i]) + 'x^' + str(len(c)-2 - i) + ' + '
    result += str(c[len(c)-1])
    print(result)


with open('points.csv', 'r') as f:
    reader = csv.reader(f)
    line = 0
    for row in reader:
        if line != 0:
            if(row):
                #print(row)
                x.append(float(row[0]))
                y.append(float(row[1]))
        line += 1
    x2 = range(int(min(x)), int(max(x)), 1)

p = rank(p)

best = [sys.maxsize]
for i in range(1, maxDegree+1):
    for j in range(0,size):
        p.append(gen(i))
    for k in range(1, iterations):
        p = rank(p)
        for l in range(1,6):
            p.pop(len(p)-1)

        p.append(gen(i))
        p.append(gen(i))
        p.append(gen(i))
        p.append(breed(p[0], p[1], i))
        p.append(breed(p[2], p[3], i))
        p.append(breed(p[4], p[5], i))
    if p[0][0] < best[0]:
        best = p[0]
    p.clear()
    

    
    

printPoly(best)

plt.figure(1)
plt.scatter(x, y)

plt.figure(1)
plt.plot(x2, calcValues(best, x2, len(best)-2), color='red')
plt.show()


    