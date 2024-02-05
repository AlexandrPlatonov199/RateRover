from raterover.common.api.schemas.health import HealthResponse
from raterover.common.utils.package import get_version


async def health() -> HealthResponse:
    return HealthResponse(
        version="0.0.0",
        name="Course",
    )