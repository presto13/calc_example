import re
from collections import deque
from typing import Callable, Dict, List, Tuple


class RPNCalculator:
    """A class for performing calculations using Reverse Polish Notation (RPN)."""

    operators: Dict[str, Tuple[int, Callable[[float, float], float]]] = {
        "+": (1, lambda x, y: x + y),  # Addition operation
        "-": (1, lambda x, y: x - y),  # Subtraction operation
        "*": (2, lambda x, y: x * y),  # Multiplication operation
        "/": (2, lambda x, y: x / y if y != 0 else float("inf")),
        # Division operation with check for division by zero
    }

    def _parse(self, expression: str) -> List[str]:
        """
        Parses the expression into a list of tokens.

        :param expression: A string of the mathematical expression
        :return: A list of tokens
        """
        tokens = re.split("([+\-*/()])", expression)
        return [token for token in tokens if token != " "]

    def _infix_to_rpn(self, parsed_formula: List[str]) -> List[str]:
        """
        Converts the parsed formula into Reverse Polish Notation.

        :param parsed_formula: A list of tokens representing the formula
        :return: A list of tokens in Reverse Polish Notation
        """
        stack, queue = [], deque()

        for token in parsed_formula:
            if token not in self.operators:
                queue.append(token)
            elif token in self.operators:
                while (
                    stack and self.operators[token][0] <= self.operators[stack[-1]][0]
                ):
                    queue.append(stack.pop())
                stack.append(token)

        while stack:
            queue.append(stack.pop())

        return list(queue)

    def calculate(self, expression: str) -> float:
        """
        Calculates the result of the expression using Reverse Polish Notation.

        :param expression: A string of the mathematical expression
        :return: The result of the calculation
        """
        parsed_exp = self._parse(expression)
        rpn_queue = self._infix_to_rpn(parsed_exp)

        stack = []

        for token in rpn_queue:
            if token in self.operators:
                if len(stack) < 2:
                    raise ValueError("Invalid expression")

                y, x = stack.pop(), stack.pop()
                result = self.operators[token][1](x, y)

                if result is float("inf"):
                    raise ValueError("Division by zero")

                stack.append(result)
            else:
                if not token.isnumeric():
                    raise ValueError(f"Invalid character: {token}")

                stack.append(float(token))

        if len(stack) != 1:
            raise ValueError("Invalid expression")

        return stack[0]
