import redis
import os
import json

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

def set_cache(artista, data, expire=604800):
    redis_client.set(artista, json.dumps(data), ex=expire)

def get_cache(artista):
    data = redis_client.get(artista)
    if data:
        return json.loads(data)
    return None

def clear_cache(artista):
    redis_client.delete(artista)