#import matplotlib.pyplot as pltMUTATION_CHANCE
import numpy as np
from typing import Final
import random
import math
import csv
import sys

POPULATION_SIZE: Final = 200
COEF_GEN_RANGE: Final = 100
MAX_ITERATIONS: Final = 1000
MUTATION_CHANCE: Final = 1.0
MUTATION_MAX: Final = 5
MAX_POLYNOMIAL_DEGREE: Final = 20

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Polynomial:
    def __init__(self, coefficients, points: list[Point]):
        #Coefficients start from lowest to highest degree starting from y intecrept
        self.coefficients: list = coefficients
        self.degree = len(coefficients) - 1
        self.error = math.inf
        if len(coefficients) > 0:
            self.calculateError(points)

    def clone(self, points: list[Point]):
        coefficients = []
        for c in self.coefficients:
            coefficients.append(c)
        p = Polynomial(coefficients, points)
        return p

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
        err = 0
        for i in range(0, len(points)):
            err += (points[i].y - self.yAt(points[i].x))**2
        self.error = err

    def mutate(self, points: list[Point]):
        if random.uniform(0,1) > 0.5:
            self.coefficients[random.randint(0,len(self.coefficients)-1)] += -MUTATION_MAX + 2*MUTATION_MAX*random.uniform(0,1)
        else:
            if random.uniform(0,1) > 0.5:
                if self.degree > 0:
                    self.coefficients.pop()
                    self.degree -= 1
                else:
                    self.coefficients[random.randint(0,len(self.coefficients)-1)] += -MUTATION_MAX + 2*MUTATION_MAX*random.uniform(0,1)
            else:
                self.coefficients.append(getRandomIntegerInRange(COEF_GEN_RANGE))
                self.degree += 1

        self.calculateError(points)

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
        for i in range(0, MAX_ITERATIONS):

            for j in range(0, POPULATION_SIZE):
                population.append(cloneAndMutate(self.bestPolynomial, self.points))   

            rankPolynomialsByError(population)

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
    return Polynomial(coefficients, points)


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
    
def cloneAndMutate(parent: Polynomial, points: list[Point]) -> Polynomial:
    child = parent.clone(points)
    child.mutate(points)
    return child