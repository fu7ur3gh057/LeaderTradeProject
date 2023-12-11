import os

from redis import StrictRedis

REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = os.environ["REDIS_PORT"]
REDIS_DB = os.environ["REDIS_DB"]


class RedisService:
    def __init__(self) -> None:
        self.client = StrictRedis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            charset="utf-8",
            decode_responses=True,
        )

    def cache_product(self, user_id: int, product_id: int) -> None:
        user_id = str(user_id)
        product_id = str(product_id)
        if product_id not in self.client.lrange(user_id, 0, -1):
            self.client.lpush(user_id, product_id)

    def get_cached_products(self, user_id: int) -> list[int]:
        cached = self.client.lrange(str(user_id), 0, -1)
        return [int(i) for i in cached]
