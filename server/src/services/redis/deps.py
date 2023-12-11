from src.services.redis.service import RedisService

_connection = None


def redis_connection() -> RedisService:
    global _connection
    if _connection is None:
        client = RedisService()
        _connection = client
    return _connection
