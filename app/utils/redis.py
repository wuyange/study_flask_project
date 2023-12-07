from app.exts import cache

def set(key,vaule,timeout=None):
    cache.set(key, vaule, timeout=timeout)

def get(key):
    return cache.get(key)

