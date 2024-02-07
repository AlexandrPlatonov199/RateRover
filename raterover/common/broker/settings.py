from pydantic_settings import BaseSettings


class BaseBrokerConsumerSettings(BaseSettings):
    consumer_servers: str = ""
    queues: list[str] = []


class BaseBrokerProducerSettings(BaseSettings):
    producer_servers: str = ""