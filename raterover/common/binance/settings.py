from pydantic_settings import BaseSettings

class BaseBinanceSettings(BaseSettings):
    uri: str = ""