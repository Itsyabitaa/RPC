class CalculatorService:
    """
    Actual implementation of the Calculator service methods.
    """
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        return a // b  # We use integer division to stick to our 'int' IDL definition
