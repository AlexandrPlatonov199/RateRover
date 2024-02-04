from pydantic import BaseModel, ConfigDict


class Course(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    exchanger: str
    direction: str
    value: float

