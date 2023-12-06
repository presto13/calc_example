import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("input_data", "expected_result"),
    [
        [{"expression": "3+3"}, {"result": 6}],
        [{"expression": "3*3"}, {"result": 9}],
        [{"expression": "3-3"}, {"result": 0}],
        [{"expression": "3/3"}, {"result": 1}],
        [{"expression": "3+3", "color": True}, {"result": 6, "color": "green"}],
        [{"expression": "3/7", "color": True}, {"result": 0.4286, "color": "red"}],
    ],
)
async def test_calculator_api(
    client: AsyncClient,
    fastapi_app: FastAPI,
    input_data: dict[str, str | bool],
    expected_result: float | int,
) -> None:
    """
    Checks the health endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    :param input_data: data to be sent as input to the server.
    :param expected_result: expected result.
    """
    url = fastapi_app.url_path_for("calculate")
    response = await client.post(url, json=input_data)

    assert response.status_code == status.HTTP_200_OK

    res_data = response.json()
    assert res_data == expected_result


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("expression", "expected_error_message"),
    [
        ["2++", "Value error, Expression should not start or end with an operator."],
        ["+2+", "Value error, Expression should not start or end with an operator."],
        ["2%2", "Value error, Invalid character '%'."],
        ["22=", "Value error, Invalid character '='."],
        ["2++2", "Value error, Invalid character '+'."],
        ["22", "String should have at least 3 characters"],
        [" 22  ", "Value error, Minimum length must be 3 except a spaces."],
        ["2/0", "Cannot divide by zero."],
    ],
)
async def test_calculator_api_raise_error_with_wrong_expression(
    client: AsyncClient,
    fastapi_app: FastAPI,
    expression: str,
    expected_error_message: str,
) -> None:
    """
    Checks the health endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    :expected_error_message: expected error message.
    """
    url = fastapi_app.url_path_for("calculate")
    data = {"expression": expression}
    response = await client.post(url, json=data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    res_data = response.json()
    assert res_data["detail"][0]["msg"] == expected_error_message
