from fastapi.routing import APIRouter

from calc_example.web.api.calculator import router as calculator_router

api_router = APIRouter()
api_router.include_router(calculator_router)
