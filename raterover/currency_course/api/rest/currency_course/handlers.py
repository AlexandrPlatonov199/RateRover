import fastapi

from raterover.common.request_course import RequestService
from raterover.currency_course.database.service import CourseDatabaseService

from .schemas import CourseResponseModel, BaseSymbol, Course, CurrencyPair

router = fastapi.APIRouter()


@router.get("/")
async def get_course(
        request: fastapi.Request,
        base_symbol: BaseSymbol,
        currency_pair: CurrencyPair,
) -> CourseResponseModel:
    base_symbol = base_symbol.value
    currency_pair = currency_pair.value
    print(base_symbol)

    request_service:  RequestService = request.app.service.request_service
    database_service: CourseDatabaseService = request.app.service.database

    coros = await request_service.get_price_feed(base_symbol, currency_pair)

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


