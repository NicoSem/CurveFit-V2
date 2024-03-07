#import matplotlib.pyplot as pltMUTATION_CHANCE
import numpy as np
from typing import Final
import csv
import sys
import PolynomialHandler
from PolynomialHandler import Polynomial

POPULATION_SIZE: Final = 10
COEF_GEN_RANGE: Final = 100
MAX_ITERATIONS: Final = 100
MUTATION_CHANCE: Final = 0.5
MUTATION_MAX: Final = 10
MAX_POLYNOMIAL_DEGREE: Final = 20
points = []


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



    
def fit(x, y, p: Polynomial):
    population = [PolynomialHandler.Polynomial(p.coefficients, x, y)]
    best = population[0]
    for i in range(1, MAX_POLYNOMIAL_DEGREE+1):
        for j in range(0,POPULATION_SIZE):
            population.append(PolynomialHandler.generateRandomPolynomial(i, COEF_GEN_RANGE, x, y))
        for k in range(1, MAX_ITERATIONS):
            population = rankPolynomialsByError(population)
            for l in range(1,6):
                population.pop(len(population)-1)

            population.append(PolynomialHandler.generateRandomPolynomial(i, COEF_GEN_RANGE, x, y))
            population.append(PolynomialHandler.generateRandomPolynomial(i, COEF_GEN_RANGE, x, y))
            population.append(PolynomialHandler.generateRandomPolynomial(i, COEF_GEN_RANGE, x, y))
            population.append(PolynomialHandler.createAveragePolynomial(population[0], population[1], x, y))
            population.append(PolynomialHandler.createAveragePolynomial(population[2], population[3], x, y))
            population.append(PolynomialHandler.createAveragePolynomial(population[4], population[5], x, y))
        if population[0].error < best.error:
            best = population[0]
        population.clear()
    return best

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y