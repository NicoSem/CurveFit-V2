import random
from CurveFit import Point

class Polynomial:
    def __init__(self, coefficients, points: list[Point]):
        #Coefficients start from lowest to highest degree starting from y intecrept
        self.coefficients = coefficients
        self.degree = len(coefficients) - 1
        int: self.error = self.calculateError(points)

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

    def mutate(self, MUTATION_CHANCE, MUTATION_MAX):
        if(random.uniform(0,1) > MUTATION_CHANCE):
            self.coefficients[random.randint(0,len(self.coefficients)-1)] *= -MUTATION_MAX + 2*MUTATION_MAX*random.uniform(0,1)

    def __str__(self):
        return str(self.coefficients)
        
    

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
    