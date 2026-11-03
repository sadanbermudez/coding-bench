import time
from collections import OrderedDict


class TTLCache:
    def __init__(self, capacity, ttl, clock=time.monotonic):
        if capacity < 1:
            raise ValueError(capacity)
        self.capacity, self.ttl, self.clock, self.d = capacity, ttl, clock, OrderedDict()

    def _expired(self, k):
        return self.clock() - self.d[k][1] >= self.ttl

    def get(self, key, default=None):
        if key not in self.d:
            return default
        if self._expired(key):
            del self.d[key]
            return default
        self.d.move_to_end(key)
        return self.d[key][0]

    def put(self, key, value):
        if key not in self.d and len(self.d) >= self.capacity:
            for k in [k for k in self.d if self._expired(k)]:
                del self.d[k]
            if len(self.d) >= self.capacity:
                self.d.popitem(last=False)
        self.d[key] = (value, self.clock())
        self.d.move_to_end(key)

    def __len__(self):
        return sum(not self._expired(k) for k in self.d)
