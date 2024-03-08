#import matplotlib.pyplot as pltMUTATION_CHANCE
import numpy as np
from typing import Final
import random
import math
import csv
import sys

POPULATION_SIZE: Final = 10
COEF_GEN_RANGE: Final = 100
MAX_ITERATIONS: Final = 100
MUTATION_CHANCE: Final = 0.5
MUTATION_MAX: Final = 10
MAX_POLYNOMIAL_DEGREE: Final = 20

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Polynomial:
    def __init__(self, coefficients, points: list[Point]):
        #Coefficients start from lowest to highest degree starting from y intecrept
        self.coefficients = coefficients
        self.degree = len(coefficients) - 1
        self.error = math.inf
        if len(coefficients) > 0:
            self.calculateError(points)

    def yAt(self, x):
        result = 0
        for i in range(0, self.degree + 1):
            result += self.coefficients[i]*(x**(i))
        return result
    
    def mapToY(self, xValues):
        yValues = []
        for i in xValues:
            yValues.append(self.yAt(i))
        return yValues

    
    def calculateError(self, points: list[Point]):
        err: float = 0
        for i in range(0, len(points)):
            err += (points[i].y - self.yAt(points[i].x))**2
        self.error = err

    def mutate(self, MUTATION_CHANCE, MUTATION_MAX):
        if(random.uniform(0,1) > MUTATION_CHANCE):
            self.coefficients[random.randint(0,len(self.coefficients)-1)] *= -MUTATION_MAX + 2*MUTATION_MAX*random.uniform(0,1)

    def __str__(self):
        return str(self.coefficients) + " error: " + str(self.error)
    

class Fitter:
    def __init__(self):
        self.points = []
        self.bestPolynomial = Polynomial([0], self.points)

    def addPoint(self, x, y):
        self.points.append(Point(x, y))
        self.bestPolynomial.calculateError(self.points)

    def fit(self):
        population = [self.bestPolynomial]
        for i in range(0, MAX_POLYNOMIAL_DEGREE+1):
            for j in range(1,POPULATION_SIZE):
                population.append(generateRandomPolynomial(i, COEF_GEN_RANGE, self.points))
            for k in range(1, MAX_ITERATIONS):
                population = rankPolynomialsByError(population)
                for l in range(1,6):
                    population.pop(len(population)-1)

                population.append(generateRandomPolynomial(i, COEF_GEN_RANGE, self.points))
                population.append(generateRandomPolynomial(i, COEF_GEN_RANGE, self.points))
                population.append(generateRandomPolynomial(i, COEF_GEN_RANGE, self.points))
                population.append(createAveragePolynomial(population[0], population[1], self.points))
                population.append(createAveragePolynomial(population[2], population[3], self.points))
                population.append(createAveragePolynomial(population[4], population[5], self.points))
            if population[0].error < self.bestPolynomial.error:
                self.bestPolynomial = population[0]
            population.clear()
        return self.bestPolynomial

def rankPolynomialsByError(polynomials: list[Polynomial]):

        listSize = len(polynomials)

        for i in range(0,listSize-1):
            unrankedPoly = polynomials.pop(i)
            for j in range(0,listSize-1):
                if unrankedPoly.error < polynomials[j].error:
                    polynomials.insert(j, unrankedPoly)
                    break
            if len(polynomials) < listSize:
                polynomials.append(unrankedPoly)
        return polynomials


def absoluteSum(numbers):
    result = 0
    for num in numbers:
        result += abs(num)
    return result

def generateRandomPolynomial(degree, coefficentRange, points: list[Point]):
    coefficients = []
    for i in range(0, degree+1):
        coefficients.append(getRandomIntegerInRange(coefficentRange))
    return Polynomial(coefficients=coefficients, points=points)


def getRandomIntegerInRange(range):
    return random.randint(-range,range)


def createAveragePolynomial(a: Polynomial, b: Polynomial, points: list[Point]):
    coefficients = []
    for i in range(0, max(a.degree, b.degree) + 1):
        try:
            coefficients.append((a.coefficients[i] + b.coefficients[i])/2)
        except:
            try:
                coefficients.append(a.coefficients[i] / 2)
            except:
                coefficients.append(b.coefficients[i] / 2)

    return Polynomial(coefficients, points)
    