import time


class Timer:
    def __enter__(self):
        self._start = time.perf_counter()
        self.elapsed = None
        return self

    def __exit__(self, exc_type, exc, tb):
        self.elapsed = time.perf_counter() - self._start
        return False
