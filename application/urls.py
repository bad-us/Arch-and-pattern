from datetime import date
from application.views import Index, Contacts, PageNotFound

# Front controllers


def today(request):
    request["data"] = date.today()


def user_name(request):
    request["user"] = "BAD"


fronts = [today, user_name]

routes = {
    "/": Index(),
    "/contacts/": Contacts(),
}

page_404 = PageNotFound()
