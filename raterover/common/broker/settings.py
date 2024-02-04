from pydantic_settings import BaseSettings


class BaseBrokerConsumerSettings(BaseSettings):
    consumer_servers: str = ""
    queues_name: str = ""


class BaseBrokerProducerSettings(BaseSettings):
    producer_servers: str = ""
    exchange_name: str = ""
