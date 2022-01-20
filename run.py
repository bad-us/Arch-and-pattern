from bad_framework.main import Framework
from application.urls import routes, fronts, page_404
from wsgiref.simple_server import make_server

application = Framework(routes, fronts, page_404)

with make_server("", 8000, application) as httpd:
    print("Сервер работает на порту 8000...")
    httpd.serve_forever()
