from datetime import date

from application.views import PageNotFound

# Front controllers


def today(request):
    request["data"] = date.today()


def user_name(request):
    request["user"] = "User_1"


fronts = [today, user_name]


page_404 = PageNotFound()
