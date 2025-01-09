import threading


class Singleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                # Another thread could have created the instance
                # before we acquired the lock. So check that the
                # instance is still nonexistent.
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    print(f"loading {cls.__name__}")
                    cls.build(cls)
        return cls._instance

    def build(cls):
        raise NotImplementedError()
