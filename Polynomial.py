class Poly:
    def __init__(self, coefficients):
        self.coefficients = coefficients
        self.degree = len(coefficients) - 1
        self.error = 0

    def __str__(self):
        return str(self.coefficients)
