import pytest

from calc_example.services.calculator import (
    AddCalculator,
    CalculatorFactory,
    DivideCalculator,
    MultiplyCalculator,
    SubtractCalculator,
)


@pytest.fixture
def calculator_factory():
    return CalculatorFactory()


def test_calculator_factory_with_valid_arguments(calculator_factory) -> None:
    calculator = calculator_factory.from_string("2 + 2")
    assert isinstance(calculator, AddCalculator)
    assert calculator.calculate() == 4

    calculator = calculator_factory.from_string("2 - 2")
    assert isinstance(calculator, SubtractCalculator)
    assert calculator.calculate() == 0

    calculator = calculator_factory.from_string("2 * 2")
    assert isinstance(calculator, MultiplyCalculator)
    assert calculator.calculate() == 4

    calculator = calculator_factory.from_string("2 / 2")
    assert isinstance(calculator, DivideCalculator)
    assert calculator.calculate() == 1


@pytest.mark.parametrize(
    "expression",
    [
        "2.3",
        "2",
        "a+2",
        "2^2",
    ],
)
def test_calculator_factory_with_invalid_arguments(
    calculator_factory,
    expression,
) -> None:
    with pytest.raises(ValueError):
        calculator_factory.from_string(expression)


def test_divide_calculator_with_zero_division() -> None:
    with pytest.raises(ValueError):
        calculator = DivideCalculator(2, 0)
        calculator.calculate()
