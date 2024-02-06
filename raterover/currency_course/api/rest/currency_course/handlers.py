import fastapi

from .dependencies import get_path_course

from .schemas import BaseCourse
from ..schemas import CourseResponse, CourseModel

router = fastapi.APIRouter()


@router.get("/")
async def get_course(
        request: fastapi.Request,
        course: BaseCourse,
) -> CourseResponse:

    result = await get_path_course(request, course.value)

    course_model = CourseModel(direction=result.direction, value=result.value)

    return CourseResponse(
        exchanger=result.exchanger,
        courses=[course_model.dict()]
    )


