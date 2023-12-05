from fastapi.routing import APIRouter

from calc_example.web.api import monitoring

api_router = APIRouter()
api_router.include_router(monitoring.router)
