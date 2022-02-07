from datetime import date
from application.views import (
    Index,
    Contacts,
    PageNotFound,
    Write_to_us,
    CategoryList,
    CreateCategory,
    CoursesList,
    CreateCourse,
    CopyCourse,
)

# Front controllers


def today(request):
    request["data"] = date.today()


def user_name(request):
    request["user"] = "BAD"


fronts = [today, user_name]

# routes = {
#     "/": Index(),
#     "/contacts/": Contacts(),
#     "/write/": Write_to_us(),
# }

routes = {
    "/": Index(),
    "/contacts/": Contacts(),
    "/write/": Write_to_us(),
    "/category_list/": CategoryList(),
    "/create_category/": CreateCategory(),
    "/courses_list/": CoursesList(),
    "/create_course/": CreateCourse(),
    "/copy_course/": CopyCourse(),
}

page_404 = PageNotFound()
