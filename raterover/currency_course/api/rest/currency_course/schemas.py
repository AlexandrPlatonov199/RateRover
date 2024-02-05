from pydantic import BaseModel
import enum


class BaseSymbol(str, enum.Enum):
    BTC = "BTC"
    ETH = "ETH"


class CurrencyPair(str, enum.Enum):
    RUB = "RUB"
    USD = "USD"


class Course(BaseModel):
    direction: str
    value: float


class CourseResponseModel(BaseModel):
    exchanger: str
    courses: list[Course]



