from locust import HttpUser, task, between, constant_pacing
import random
from config import cfg

class PriceFeedUser(HttpUser):
    wait_time = constant_pacing(cfg.pacing_sec)
    host = cfg.api_host

    @task
    def get_price_feed_request(self):
        transaction = self.get_price_feed_request.__name__
        base_symbols = ["BTC", "ETH"]
        currency_pairs = ["USD", "RUB"]

        base_symbol = random.choice(base_symbols)
        currency_pair = random.choice(currency_pairs)

        with self.client.get(f'/api/v1/course/?base_symbol={base_symbol}&currency_pair={currency_pair}',
                              name=transaction, catch_response=True) as response:
            if response.status_code == 200:
                response.success()

        if response.status_code == 200:
            response.success()
        else:
            response.failure(f"Не удалось получить данные о цене. Код состояния: {response.status_code}")

        if response.status_code == 200:
            response.success()
        else:
            response.failure(f"Не удалось получить данные о цене. Код состояния: {response.status_code}")