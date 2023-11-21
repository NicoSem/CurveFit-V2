#import matplotlib.pyplot as plt
import numpy as np
import csv
import random
import sys
import Polynomial

x2 = []
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

'''
def calcValues(c, x, d):
    err = 0
    for i in range(0, len(x)):
        result = c[len(c)-1]
        for j in range(1, d):
            result += c[j]*x[i]**(d-j)
        y2.append(result)
    return y2
'''

def rank(r: list[Polynomial.Poly]):
    
    for i in range(0,len(r)-1):
        s = len(r)
        a = r.pop(i)
        for j in range(0,len(r)-1):
            if a.error < r[j].error:
                r.insert(j, a)
                break
        if len(r) < s:
            r.append(a)
    return r


def mix(a, b, x, y):
    c = []
    for i in range(0, min(a.degree, b.degree)):
        c.append((a.coefficients[i] + b.coefficients[i])/2)
    '''
    if(random.uniform(0,1) > mutateChance):
        c[random.randint(1,len(c)-1)] *= -mutateMax + 2*mutateMax*random.uniform(0,1)
    '''
    p = Polynomial.Poly(c, x, y)
    
    return p


def generate(d, x, y):
    c = []
    for i in range(0, d+1):
        c.append(random.randint(-cRange,cRange))
    p = Polynomial.Poly(c, x, y)
    return p

'''
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
'''
    
def fit(x, y):
    population = [Polynomial.Poly([0], x, y)]
    best = population[0]
    for i in range(1, maxDegree+1):
        for j in range(0,size):
            population.append(generate(i, x, y))
        for k in range(1, iterations):
            population = rank(population)
            for l in range(1,6):
                population.pop(len(population)-1)

            population.append(generate(i, x, y))
            population.append(generate(i, x, y))
            population.append(generate(i, x, y))
            population.append(mix(population[0], population[1], x, y))
            population.append(mix(population[2], population[3], x, y))
            population.append(mix(population[4], population[5], x, y))
        if population[0].error < best.error:
            best = population[0]
        population.clear()
    return best
    
    
'''
printPoly(best)

plt.figure(1)
plt.scatter(x, y)

plt.figure(1)
plt.plot(x2, calcValues(best, x2, len(best)-2), color='red')
plt.show()
'''


    