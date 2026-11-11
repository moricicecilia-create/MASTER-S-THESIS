from __future__ import annotations
import threading
import time
import os


class PeakMemoryMonitor:
    """Poll process and child-process RSS; requires psutil."""
    def __init__(self, interval: float = 0.1):
        self.interval = interval
        self.peak_mb = 0.0
        self._stop = threading.Event()
        self._thread = None

    def _sample(self):
        try:
            import psutil
            proc = psutil.Process(os.getpid())
            while not self._stop.is_set():
                total = 0
                try:
                    total += proc.memory_info().rss
                    for child in proc.children(recursive=True):
                        try:
                            total += child.memory_info().rss
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            pass
                    self.peak_mb = max(self.peak_mb, total / (1024 ** 2))
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
                time.sleep(self.interval)
        except ImportError:
            return

    def __enter__(self):
        import psutil
        self.peak_mb = psutil.Process(os.getpid()).memory_info().rss / (1024 ** 2)
        self._thread = threading.Thread(target=self._sample, daemon=True)
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc, tb):
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=2)
        return False
