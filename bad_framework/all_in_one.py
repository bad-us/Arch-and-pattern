from wsgiref.simple_server import make_server
from jinja2 import Template
import os
from datetime import date


def render(template_name, folder="../templates", **kwargs):
    file_path = os.path.join(folder, template_name)
    with open(file_path, encoding="utf-8") as f:
        template = Template(f.read())
    return template.render(**kwargs)


class Index:
    def __call__(self, request):
        page = render("index.html", data=request.get("data", None), user_name=request.get("user", None))
        return "200 OK", [bytes(page, "UTF-8")]


class Contacts:
    def __call__(self, request):
        page = render("contacts.html", data=request.get("data", None), user_name=request.get("user", None))
        return "200 OK", [bytes(page, "UTF-8")]


class PageNotFound:
    def __call__(self, request):
        page = render("not_found.html", data=None)
        return "404 WHAT", [bytes(page, "UTF-8")]


routes = {
    "/": Index(),
    "/contacts/": Contacts(),
}

# Front controllers
def today(request):
    request["data"] = date.today()


def user_name(request):
    request["user"] = "BAD"


fronts = [today, user_name]


class Framework:
    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):

        path = environ["PATH_INFO"]

        if not path.endswith("/"):
            path = f"{path}/"

        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound()
        request = {}
        # front controller
        for front in self.fronts:
            front(request)
        code, body = view(request)
        start_response(code, [("Content-Type", "text/html")])
        return body


framework = Framework(routes, fronts)

with make_server("", 8000, framework) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()
