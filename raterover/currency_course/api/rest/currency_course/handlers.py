import asyncio
from loguru import logger
import fastapi
from fastapi.responses import RedirectResponse

from raterover.common.request_course import RequestService
from raterover.currency_course.api.rest.schemas import CurrencyCourseResponse
from raterover.currency_course.broker.producer_service import CourseBrokerProducerService

from raterover.currency_course.database.models import CurrencyCourse
from raterover.currency_course.database.service import CurrencyCourseDatabaseService





from .schemas import CourseResponseModel, BaseSymbol, Course, CurrencyPair

router = fastapi.APIRouter()


@router.get("/corse", name="corse")
async def get_course(
        request: fastapi.Request,
        base_symbol: BaseSymbol,
        currency_pair: CurrencyPair,
) -> CourseResponseModel:
    base_symbol = base_symbol.value
    currency_pair = currency_pair.value
    print(base_symbol)

    request_service:  RequestService = request.app.service.request_service
    database_service: CurrencyCourseDatabaseService = request.app.service.database
    broker_producer: CourseBrokerProducerService = request.app.service.broker_producer

    coros = await request_service.get_price_feed(base_symbol, currency_pair)

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


