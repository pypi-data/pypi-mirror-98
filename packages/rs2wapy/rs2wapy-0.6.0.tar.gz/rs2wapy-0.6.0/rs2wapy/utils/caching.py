import functools
import os
import sys
from typing import Callable
from typing import Optional

import orjson
import redis
from cachetools.func import ttl_cache as cachetools_ttl_cache
from logbook import Logger
from logbook import StreamHandler

StreamHandler(sys.stdout, level="WARNING").push_application()
logger = Logger(__name__)

_REDIS_POOL = None


class RedisCached:
    def __init__(self,
                 pool: Optional[redis.ConnectionPool],
                 ttl_seconds: int,
                 function: Callable,
                 is_method: bool = False,
                 cache_falsy: bool = True,
                 serializer: Callable = orjson.dumps,
                 deserializer: Callable = orjson.loads):

        self._redis = redis.Redis(connection_pool=pool)
        self.function = function
        self.serializer = serializer
        self.deserializer = deserializer
        self.ttl_seconds = ttl_seconds
        self.is_method = is_method
        self.cache_falsy = cache_falsy

    @property
    def key_prefix(self):
        return self.function.__name__

    def key(self, *args, **kwargs):
        if self.is_method:
            args = args[1:]
        params = self.serializer({'args': args, "kwargs": kwargs})
        return f"{self.key_prefix}__{params}"

    @property
    def __name__(self):
        return self.function.__name__

    @property
    def __wrapped__(self):
        return self.function

    def __call__(self, *args, **kwargs):
        val = None
        key = self.key(*args, **kwargs)
        try:
            val = self._redis.get(key)
        except redis.exceptions.RedisError:
            logger.exception("Unable to use cache")

        if val is not None:
            logger.debug("Cache HIT for %s", self.key(*args, **kwargs))
            return self.deserializer(val)

        logger.debug("Cache MISS for %s", self.key(*args, **kwargs))
        val = self.function(*args, **kwargs)

        if not val and not self.cache_falsy:
            logger.debug("Caching falsy result is disabled for %s", self.__name__)
            return val

        try:
            self._redis.setex(key, self.ttl_seconds, self.serializer(val))
            logger.debug("Cache SET for %s", self.key(*args, **kwargs))
        except redis.exceptions.RedisError:
            logger.exception("Unable to set cache")

        return val

    def clear_all(self):
        try:
            keys = list(self._redis.scan_iter(match=f"{self.key_prefix}*"))
            if keys:
                self._redis.delete(*keys)
        except redis.exceptions.RedisError:
            logger.exception("Unable to clear cache")
        else:
            logger.debug("Cache CLEARED for %s", keys)


def ttl_cache(ttl: int, *args, is_method: bool = True,
              cache_falsy: bool = True, **kwargs):
    global _REDIS_POOL
    redis_url = os.getenv('REDIS_URL')
    if not redis_url:
        logger.warning("REDIS_URL is not set falling back to memory cache")
        return cachetools_ttl_cache(*args, ttl=ttl, **kwargs)
    if _REDIS_POOL is None:
        logger.warning("Redis pool initializing")
        _REDIS_POOL = redis.ConnectionPool.from_url(
            redis_url, max_connections=10, socket_connect_timeout=5,
            socket_timeout=5, decode_responses=True
        )

    def decorator(func: Callable):
        cached_func = RedisCached(
            _REDIS_POOL,
            ttl,
            function=func,
            is_method=is_method,
            cache_falsy=cache_falsy
        )

        def wrapper(*wargs, **wkwargs):
            # Re-wrapping to preserve function signature
            return cached_func(*wargs, **wkwargs)

        wrapper = functools.update_wrapper(wrapper, func)
        wrapper.cache_clear = cached_func.clear_all
        return wrapper

    return decorator
