import re
from abc import ABC, abstractmethod


class Calculator(ABC):
    """Abstract base class for calculator classes."""

    def __init__(self, a, b, expression=None):
        self.a = a
        self.b = b
        self.expression = expression

    @abstractmethod
    def calculate(self):
        """Abstract method for performing calculations."""


class AddCalculator(Calculator):
    """Class for performing addition."""

    def calculate(self):
        return self.a + self.b


class SubtractCalculator(Calculator):
    """Class for performing subtraction."""

    def calculate(self):
        return self.a - self.b


class MultiplyCalculator(Calculator):
    """Class for performing multiplication."""

    def calculate(self):
        return self.a * self.b


class DivideCalculator(Calculator):
    """Class for performing division."""

    DEFAULT_DECIMAL_PLACES = 4

    def calculate(self):
        self._validate_input()
        return round(self.a / self.b, self.DEFAULT_DECIMAL_PLACES)

    def _validate_input(self):
        """Validate if the divisor is non-zero."""
        if self.b == 0:
            raise ValueError("Cannot divide by zero.")


class CalculatorFactory:
    """
    Factory class for creating calculator instances based on operation.
    """

    operation_dict = {
        "+": AddCalculator,
        "-": SubtractCalculator,
        "*": MultiplyCalculator,
        "/": DivideCalculator,
    }

    def from_string(self, expression):
        """
        Create a Calculator instance from a string expression.
        """
        parts = re.split(r"([+\-*/])", expression)
        if len(parts) != 3:
            raise ValueError("Invalid expression.")
        a, operation, b = parts
        calculator_class = self.operation_dict.get(operation)
        if not calculator_class:
            raise ValueError(f"Invalid operation {operation}.")
        return calculator_class(float(a), float(b))
