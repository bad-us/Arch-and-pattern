from bad_framework.templator import render


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