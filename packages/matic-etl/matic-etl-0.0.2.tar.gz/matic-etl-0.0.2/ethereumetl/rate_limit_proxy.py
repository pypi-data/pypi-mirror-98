import logging
import threading
import time


class RateLimitingProxy:
    def __init__(self, delegate, max_per_second=5):
        self._lock = threading.Lock()
        self._delegate = delegate
        self._min_interval = 1.0 / max_per_second
        self._last_time_called = time.perf_counter()
        self._wait_buffer = 0.001

    def __getattr__(self, name):
        self._lock.acquire()
        try:
            elapsed = time.perf_counter() - self._last_time_called
            left_to_wait = self._min_interval - elapsed + self._wait_buffer
            if left_to_wait > 0:
                logging.debug(f'Waiting {left_to_wait} seconds because of rate limiting')
                time.sleep(left_to_wait)

            return getattr(self._delegate, name)
        finally:
            self._last_time_called = time.perf_counter()
            self._lock.release()