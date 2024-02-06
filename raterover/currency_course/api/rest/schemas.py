from pydantic import BaseModel, ConfigDict

from raterover.currency_course.database.models import Course


class CourseModel(BaseModel):
    direction: str
    value: float


class CourseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    exchanger: str
    courses: list[CourseModel]

