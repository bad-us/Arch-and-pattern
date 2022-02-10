from bad_framework.main import Framework, FakeFramework, LogFramework
from application.urls import fronts, page_404
from application.views import routes  # импорт из view тк применяем декоратор AppRoute
from wsgiref.simple_server import make_server

application = Framework(routes, fronts, page_404)
fake_wsgi = FakeFramework()
log_wsgi = LogFramework(routes, fronts, page_404)


def create_wsgi_server():
    server_type = input("Выберите сервер для запуска: 1 - Основной сервер, 2 - ЛОГ_сервер, 3 - Второй сервер ")
    if server_type == "2":
        with make_server("", 8080, log_wsgi) as httpd:
            print("ЛОГ_сервер работает на порту 8080...")
            httpd.serve_forever()
    elif server_type == "3":
        with make_server("", 8888, fake_wsgi) as httpd:
            print("Второй сервер работает на порту 8888...")
            httpd.serve_forever()
    else:
        with make_server("", 8000, application) as httpd:
            print("Сервер работает на порту 8000...")
            httpd.serve_forever()


if __name__ == "__main__":
    create_wsgi_server()