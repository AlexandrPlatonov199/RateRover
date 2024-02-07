from pydantic import BaseModel


class CourseMessageModel(BaseModel):
    exchanger: str
    direction: str
    value: float