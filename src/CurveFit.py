#import matplotlib.pyplot as pltMUTATION_CHANCE
import numpy as np
from typing import Final
import csv
import random
import sys
import PolynomialHandler
from PolynomialHandler import Polynomial

POPULATION_SIZE: Final = 10
COEF_GEN_RANGE: Final = 100
MAX_ITERATIONS: Final = 100
MUTATION_CHANCE: Final = 0.5
MUTATION_MAX: Final = 10
MAX_POLYNOMIAL_DEGREE: Final = 20


def absoluteSum(numbers):
    result = 0
    for num in numbers:
        result += abs(num)
    return result


def rankPolynomialsByError(polynomials: list[Polynomial]):

    listSize = len(polynomials)

    for i in range(0,listSize-1):
        unrankedPoly = polynomials.pop(i)
        for j in range(0,listSize-2):
            if unrankedPoly.error < polynomials[j].error:
                polynomials.insert(j, unrankedPoly)
                break
        if len(polynomials) < listSize:
            polynomials.append(unrankedPoly)
    return polynomials


def mix(a: Polynomial, b: Polynomial, x, y):
    c = []
    for i in range(0, max(a.degree, b.degree) + 1):
        try:
            c.append((a.coefficients[i] + b.coefficients[i])/2)
        except:
            try:
                c.append(a.coefficients[i] / 2)
            except:
                c.append(b.coefficients[i] / 2)

    if(random.uniform(0,1) > MUTATION_CHANCE):
        c[random.randint(0,len(c)-1)] *= -MUTATION_MAX + 2*MUTATION_MAX*random.uniform(0,1)

    p = PolynomialHandler.Polynomial(c, x, y)
    
    return p


def generateRandomPolynomial(degree, xValues, yValues):
    coefficients = []
    for i in range(0, degree+1):
        coefficients.append(getRandomIntegerInRange(COEF_GEN_RANGE))
    return PolynomialHandler.Polynomial(coefficients, xValues, yValues)

def getRandomIntegerInRange(range):
    return random.randint(-range,range)

    
def fit(x, y, p: Polynomial):
    population = [PolynomialHandler.Polynomial(p.coefficients, x, y)]
    best = population[0]
    for i in range(1, MAX_POLYNOMIAL_DEGREE+1):
        for j in range(0,POPULATION_SIZE):
            population.append(generateRandomPolynomial(i, x, y))
        for k in range(1, MAX_ITERATIONS):
            population = rankPolynomialsByError(population)
            for l in range(1,6):
                population.pop(len(population)-1)

            population.append(generateRandomPolynomial(i, x, y))
            population.append(generateRandomPolynomial(i, x, y))
            population.append(generateRandomPolynomial(i, x, y))
            population.append(mix(population[0], population[1], x, y))
            population.append(mix(population[2], population[3], x, y))
            population.append(mix(population[4], population[5], x, y))
        if population[0].error < best.error:
            best = population[0]
        population.clear()
    return best
