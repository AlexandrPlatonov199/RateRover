import fastapi

from . import handlers

router = fastapi.APIRouter()

router.include_router(handlers.router, prefix="/course")


