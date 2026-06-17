import json

from redis import Redis


class RedisCacheBackend:
    
    def __init__(self, redis_url: str, cache_ttl: int | None = None):
        self.redis = Redis.from_url(redis_url, decoded_responses=True)
        self.cache_ttl =  cache_ttl
        
    def set(self,  key: str, value: dict) -> None:
        self.redis.set(key, json.dumps(value), ex=self.cache_ttl)
        
    def get(self, key: str) -> dict:
        return self.redis.get(key)
        
    def delete(self, key: str) -> None:
        self.redis.delete(key)