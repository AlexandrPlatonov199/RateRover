import fastapi

from . import currency_course

router = fastapi.APIRouter()


router.include_router(currency_course.router, prefix="/course", tags=["Course"])

