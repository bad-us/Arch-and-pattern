from time import time

# Декоратор похожий на flask

class AppRoute:
    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()


# Время выполнения модуля
class Debug:
    def __init__(self, name):

        self.name = name

    def __call__(self, cls):
        def timeit(func):
            def timed(*args, **kwargs):
                start = time()
                result = func(*args, **kwargs)
                finish = time()
                total_time = finish - start

                print(f"Модуль {self.name} выполнялся {total_time:2.2f} ms")
                return result

            return timed

        return timeit(cls)