#import matplotlib.pyplot as plt
import numpy as np
import csv
import random
import sys
import Polynomial

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


def mix(a: Polynomial.Poly, b: Polynomial.Poly, x, y):
    c = []
    for i in range(0, max(a.degree, b.degree) + 1):
        try:
            c.append((a.coefficients[i] + b.coefficients[i])/2)
        except:
            try:
                c.append(a.coefficients[i] / 2)
            except:
                c.append(b.coefficients[i] / 2)

    if(random.uniform(0,1) > mutateChance):
        c[random.randint(0,len(c)-1)] *= -mutateMax + 2*mutateMax*random.uniform(0,1)

    p = Polynomial.Poly(c, x, y)
    
    return p


def generate(d, x, y):
    c = []
    for i in range(0, d+1):
        c.append(random.randint(-cRange,cRange))
    p = Polynomial.Poly(c, x, y)
    return p

    
def fit(x, y, p: Polynomial.Poly):
    population = [Polynomial.Poly(p.coefficients, x, y)]
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
p1 = Polynomial.Poly([2, 3, 4],[0],[0])
p2 = Polynomial.Poly([1],[0],[0])
print(mix(p1,p2,[0],[0]))
'''
