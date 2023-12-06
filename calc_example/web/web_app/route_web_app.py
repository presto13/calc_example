from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="calc_example/templates")
router = APIRouter(include_in_schema=False)


@router.get("/")
async def home(
    request: Request,
):
    """
    This method is used to handle the home page request.

    Parameters:
    - request (Request): The FastAPI Request object.
    Returns:
    - TemplateResponse: The rendered HTML template response using
    the Jinja2 template engine.
    """
    return templates.TemplateResponse(
        "calculator_page.html",
        {"request": request},
    )
