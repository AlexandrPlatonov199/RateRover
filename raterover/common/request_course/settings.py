from pydantic_settings import BaseSettings


class BaseRequestSettings(BaseSettings):
    uri_binance: str = ""
    uri_coingecko: str = ""
