import random
from CurveFit import Polynomial, Point

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
    