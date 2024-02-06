from locust import HttpUser, task, between, constant_pacing
import random
from config import cfg

class PriceFeedUser(HttpUser):
    wait_time = constant_pacing(cfg.pacing_sec)
    host = cfg.api_host

    @task
    def get_price_feed_request(self):
        transaction = self.get_price_feed_request.__name__
        course = ["BTC-USD",
                  "BTC-RUB",
                  "ETH-USD",
                  "ETH-RUB"]

        course = random.choice(course)


        with self.client.get(f'/api/v1/course/?course={course}',
                              name=transaction, catch_response=True) as response:
            if response.status_code == 200:
                response.success()


