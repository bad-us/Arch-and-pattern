from bad_framework.templator import render
from patterns.creational_patterns import Engine, Logger, Course
from patterns.structural_patterns import AppRoute, Debug

site = Engine()
logger = Logger("main")

routes = {}


@AppRoute(routes=routes, url="/")
class Index:
    @Debug("Главная")
    def __call__(self, request):
        page = render("index.html", data=request.get("data", None), user_name=request.get("user", None))
        return "200 OK", [bytes(page, "UTF-8")]


@AppRoute(routes=routes, url="/contacts/")
class Contacts:
    @Debug("Контакты")
    def __call__(self, request):
        page = render("contacts.html", data=request.get("data", None), user_name=request.get("user", None))
        return "200 OK", [bytes(page, "UTF-8")]


@AppRoute(routes=routes, url="/write/")
class Write_to_us:
    @Debug("Обратная связь")
    def __call__(self, request):
        page = render("write_to_us.html", data=request.get("data", None), user_name=request.get("user", None))
        return "200 OK", [bytes(page, "UTF-8")]


@AppRoute(routes=routes, url="/category_list/")
class CategoryList:
    @Debug("Список курсов")
    def __call__(self, request):
        # передаем список категорий
        page = render(
            "category_list.html",
            categories_list=site.categories,
            data=request.get("data", None),
            user_name=request.get("user", None),
        )
        return "200 OK", [bytes(page, "UTF-8")]


@AppRoute(routes=routes, url="/create_category/")
class CreateCategory:
    @Debug("Создание категории")
    def __call__(self, request):
        logger.log("Создание категории")
        if request["method"] == "POST":
            category_name = request["post_data"]["name"]
            category_name = site.decode_value(category_name)

            new_category = site.create_category(category_name)
            site.categories.append(new_category)

        # можно добавлять несколько категорий по очереди, поэтому возвращаем эту же страницу
        page = render("create_category.html", data=request.get("data", None), user_name=request.get("user", None))
        return "200 OK", [bytes(page, "UTF-8")]


@AppRoute(routes=routes, url="/create_course/")
class CreateCourse:
    category_id = -1

    @Debug("Создание курса")
    def __call__(self, request):
        logger.log("Создание курса")
        if request["method"] == "POST":
            course_name = request["post_data"]["name"]
            lesson_type = request["post_data"]["type"]
            course_name = site.decode_value(course_name)
            lesson_type = site.decode_value(lesson_type)

            category = None

            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))
                course = site.create_course(lesson_type, course_name, category)
                site.courses.append(course)
            page = render(
                "courses_list.html",
                courses_list=category.courses,
                category_name=category.name,
                id=category.id,
                data=request.get("data", None),
                user_name=request.get("user", None),
            )
            return "200 OK", [bytes(page, "UTF-8")]

        else:
            try:
                self.category_id = int(request["get_data"]["id"])
                category = site.find_category_by_id(int(self.category_id))
                page = render("create_course.html", category_name=category.name, id=category.id)
                return "200 OK", [bytes(page, "UTF-8")]
            except KeyError:
                page = render("not_found.html", data=None)
                return "404 WHAT", [bytes(page, "UTF-8")]


@AppRoute(routes=routes, url="/courses_list/")
class CoursesList:
    @Debug("Список уроков")
    def __call__(self, request):
        try:
            category = site.find_category_by_id(int(request["get_data"]["id"]))
            page = render(
                "courses_list.html",
                category_name=category.name,
                courses_list=category.courses,
                id=category.id,
                data=request.get("data", None),
                user_name=request.get("user", None),
            )
            return "200 OK", [bytes(page, "UTF-8")]
        # при исключении - выводим 404
        except KeyError:
            page = render("not_found.html", data=None)
            return "404 WHAT", [bytes(page, "UTF-8")]


# контроллер - копировать курс
@AppRoute(routes=routes, url="/copy_course/")
class CopyCourse:
    @Debug("Копирование урока")
    def __call__(self, request):
        request_params = request["get_data"]

        try:
            name = request_params["name"]
            name = site.decode_value(name)  # декодируем латиницу
            old_course = site.get_course(name)
            if old_course:
                new_name = f"{name}_new"
                new_course = Course.clone(old_course)
                # new_course = old_course.clone()
                new_course.name = new_name
                print(777, new_course)
                print(888, site.courses)
                site.courses.append(new_course)

            page = render(
                "courses_list.html",
                courses_list=site.courses,
                data=request.get("data", None),
                user_name=request.get("user", None),
            )
            return "200 OK", [bytes(page, "UTF-8")]
        except KeyError:
            page = render("not_found.html", data=request.get("data", None), user_name=request.get("user", None))
            return "404 WHAT", [bytes(page, "UTF-8")]


class PageNotFound:
    @Debug("Страница не найдена")
    def __call__(self, request):
        page = render("not_found.html", data=None)
        return "404 WHAT", [bytes(page, "UTF-8")]
