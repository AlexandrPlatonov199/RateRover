import fastapi

from . import rest
from ...common.utils.package import get_version

router = fastapi.APIRouter()

version = get_version()
router.include_router(rest.router, prefix=f"/{version}")

