from pydantic_settings import BaseSettings
from pydantic import AnyUrl


class BaseDatabaseSettings(BaseSettings):
    dns_base: AnyUrl
