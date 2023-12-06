import re
from enum import Enum

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from starlette import status

from calc_example.services.calculator import CalculatorFactory

router = APIRouter()

ALLOWED_OPERATORS = "+-*/"


class CalculatorInput(BaseModel):
    """
    A class to represent the input of a calculator.

    Attributes:
        expression (str): mathematical operation to execute.
        color (bool): whether to determine a color based on the result.
    """

    expression: str = Field(
        min_length=3,
        description="Math expression a+b. Allowed integers and operators '+ - * / ",
    )
    color: bool = False

    @field_validator("expression")
    @classmethod
    def validate_length(cls, expression: str) -> str:
        """
        Validate the length of the mathematical operation.

        Parameters:
            expression (str): mathematical operation.

        Returns:
            The validated mathematical operation.

        Raises:
            ValueError: If the mathematical operation has less than 3 characters,
            excluding spaces.
        """
        expression = expression.replace(" ", "")
        if len(expression) < 3:
            raise ValueError("Minimum length must be 3 except a spaces.")
        return expression

    @field_validator("expression")
    @classmethod
    def validate_allowed_chars(cls, expression: str) -> str:
        """
        Validate the character of the mathematical operation.

        Parameters:
            expression (str): mathematical operation.

        Returns:
            The validated mathematical operation.

        Raises:
            ValueError: If the mathematical operation includes a character that
            is not an integer or operator.
        """
        for char in expression:
            if char.isdigit() or char in ALLOWED_OPERATORS:
                continue
            raise ValueError(f"Invalid character '{char}'.")
        return expression

    @field_validator("expression")
    @classmethod
    def validate_operators(cls, expression: str) -> str:
        """
        Validate the operator of the mathematical operation.

        Parameters:
            expression (str): mathematical operation.

        Returns:
            The validated mathematical operation.

        Raises:
            ValueError: If the mathematical operation starts or ends with an operator or includes an invalid character in operation.
        """
        if expression[0] in ALLOWED_OPERATORS or expression[-1] in ALLOWED_OPERATORS:
            raise ValueError("Expression should not start or end with an operator.")
        parts = re.split("([+\-*/^])", expression)
        for index, part in enumerate(parts):
            if part.isdigit():
                continue
            if part in ALLOWED_OPERATORS and parts[index + 1] in ALLOWED_OPERATORS:
                raise ValueError(f"Invalid character '{part}'.")
        return expression


class CalculatorResult(BaseModel):
    """
    A class to represent the result of a calculator.

    Attributes:
        result (float): the result of a mathematical operation.
    """

    result: float


class CalculatorResultWithColor(CalculatorResult):
    """
    A class to represent the result of a calculator with a color.
    Inherits from CalculatorResult.

    Attributes:
        color (str): a color determined based on the parity of the result.
    """

    color: str


class Color(Enum):
    """
    An enumeration to represent colors.
    """

    RED = "red"
    GREEN = "green"


def get_result_color(result: float) -> Color:
    """
    Determines the color based on the parity of the result.
    Returns "red" for odd results and "green" for even results.
    """
    return Color.RED if result % 2 else Color.GREEN


def evaluate_expression(
    expression: str,
    color: bool = False,
) -> CalculatorResult | CalculatorResultWithColor:
    """
    Evaluates a mathematical operation, and optionally determine a color based on the result.

    Parameters:
        expression (str): mathematical operation to execute.
        color (bool, optional): whether to determine a color based on the result. Defaults to False.

    Returns:
        The result of the mathematical operation, optionally with a color.
    """
    factory = CalculatorFactory()
    calculator = factory.from_string(expression)
    result = calculator.calculate()
    if color:
        result_color = get_result_color(result)
        return CalculatorResultWithColor(result=result, color=result_color.value)
    return CalculatorResult(result=result)


@router.post("/calculate", response_model=CalculatorResult | CalculatorResultWithColor)
async def calculate(
    data: CalculatorInput,
) -> CalculatorResult | CalculatorResultWithColor:
    """
    Calculates the result of an expression and returns it.
    """
    try:
        return evaluate_expression(data.expression, data.color)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{"msg": str(e)}],
        )
