#-------------------- Imports --------------------

#-------------------- CacheConfig Class --------------------

class CacheConfig():
    __slots__ = ("MAX_CACHE_SIZE", "DEFAULT_TTL")

    def __init__(self, MAX_CACHE_SIZE: int = 68, DEFAULT_TTL: float = 600):
        self.MAX_CACHE_SIZE = MAX_CACHE_SIZE
        self.DEFAULT_TTL = DEFAULT_TTL