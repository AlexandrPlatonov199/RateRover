from pydantic import BaseModel, ConfigDict, NaiveDatetime


class CurrencyCourseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    exchanger: str
    direction: str
    value: float
    updated_at: NaiveDatetime
