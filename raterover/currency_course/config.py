from typing import Literal

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv(".env"))


class Settings(BaseSettings):
    BTC_URI: str
    URL_EXCHANGE: str
    ETH_URI: str
    API_KEY_EXCHANGE: str

    @property
    def BTC_URI(self):
        return self.BTC_URI

    @property
    def URL_EXCHANGE(self):
        return self.URL_EXCHANGE

    @property
    def ETH_URI(self):
        return self.ETH_URI

    @property
    def API_KEY_EXCHANGE(self):
        return self.API_KEY_EXCHANGE



    model_config = SettingsConfigDict(case_sensitive=True)


settings = Settings()