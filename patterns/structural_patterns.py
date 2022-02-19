from time import time

# Декоратор url по типу flask

# Тк декораторы срабатывают в момент импорта, то мы получаем словарь routes (который у нас был на 4 уроке в urls.py),
# в таком виде - {'/': <views.Index object at 0x0000014B223C5BE0>, '/about/': <views.About object at 0x0000014B223C5F10>}
# Получили путь (ключ) и подставили задекорированную функцию (в виде ссылки на объект в памяти)


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
