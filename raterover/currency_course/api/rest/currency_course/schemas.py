from pydantic import BaseModel
import enum


class BaseSymbol(str,enum.Enum):
    BTC = "btcusdt"
    ETH = "ethusdt"
    USDTTRC = "usdttrcusdt"
    USDTERC = "usdtercusdt"


class Course(BaseModel):
    direction: str
    value: float


class CourseResponseModel(BaseModel):
    exchanger: str
    courses: list[Course]


class CourseListFiltersRequest(BaseModel):
    exchanger: str
    direction: str
    value: float

