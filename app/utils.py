import threading


class Singleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    print(f"loading {cls.__name__}")
                    cls.build(cls)
        return cls._instance

    def build(cls):
        raise NotImplementedError()
