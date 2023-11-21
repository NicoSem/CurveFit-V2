class Poly:
    def __init__(self, coefficients, x, y):
        #Coefficients start from lowest to highest degree starting from y intecrept
        self.coefficients = coefficients
        self.degree = len(coefficients) - 1
        int: self.error = self.calculateError(x, y)

    def yAt(self, x):
        result = 0
        for i in range(0, self.degree + 1):
            result += self.coefficients[i]*(x**(i))
        return result
    
    def mapToY(self, x):
        y = []
        for i in x:
            y.append(self.yAt(i))
        return y

    
    def calculateError(self, x, y):
        err = 0
        for i in range(0, len(x)):
            err += (y[i] - self.yAt(x[i]))**2
        self.error = err

    def __str__(self):
        return str(self.coefficients)
