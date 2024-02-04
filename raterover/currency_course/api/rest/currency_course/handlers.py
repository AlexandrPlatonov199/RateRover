import asyncio
from loguru import logger
import fastapi
from fastapi.responses import RedirectResponse

from raterover.common.binance import BinanceService
from raterover.currency_course.api.rest.schemas import CurrencyCourseResponse
from raterover.currency_course.broker.producer_service import CourseBrokerProducerService

from raterover.currency_course.database.models import CurrencyCourse
from raterover.currency_course.database.service import CurrencyCourseDatabaseService





from .schemas import CourseResponseModel, BaseSymbol, CourseListFiltersRequest, Course

router = fastapi.APIRouter()


@router.get("/corse", name="corse")
async def get_course(
        request: fastapi.Request,
        base_symbol: BaseSymbol,
) -> CourseResponseModel:
    base_symbol = base_symbol.value.lower()
    print(base_symbol)


    binance_service:  BinanceService = request.app.service.binance
    database_service: CurrencyCourseDatabaseService = request.app.service.database
    broker_producer: CourseBrokerProducerService = request.app.service.broker_producer

    coros = await asyncio.create_task(binance_service.get_price_feed(base_symbol))

    await broker_producer.send_create_course(coros)

    async with database_service.transaction() as session:
        db_course = await database_service.create_course(
            session=session,
            exchanger=coros["exchanger"],
            direction=coros["direction"],
            value=coros["value"]
        )


    return CourseResponseModel(
        exchanger=db_course.exchanger,
        courses=[Course(direction=db_course.direction, value=db_course.value)]
    )


