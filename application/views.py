from patterns.architectural_system_pattern_mappers import MapperRegistry
from patterns.architectural_system_pattern_unit_of_work import UnitOfWork
from patterns.behavioral_patterns import (BaseSerializer, CreateView,
                                          EmailNotifier, SmsNotifier)
from patterns.structural_patterns import AppRoute, Debug
from patterns.сreational_patterns import Course, Engine, Logger
from trinity_framework.templator import render

site = Engine()
logger = Logger("main")

email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()

UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)

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
        # получаем данные категорий из БД и из engine
        categories_list = MapperRegistry.get_current_mapper("category").all()
        categories_list_from_engine = site.categories

        engine_category_list = [j.name for j in categories_list_from_engine]

        # сравниваем, если категории нет в движке, то добавляем ее туда из БД
        for i in categories_list:
            if i.name not in engine_category_list:
                site.categories.append(i)

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

            # категории уникальны, ловим исключение в architectural_system_pattern_mappers стр 85 (insert)
            new_category.mark_new()
            UnitOfWork.get_current().commit()

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
                # Добавляем наблюдателей на курс
                course.observers.append(email_notifier)
                course.observers.append(sms_notifier)
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


# Блок работы со студентами


@AppRoute(routes=routes, url="/student_create/")
class StudentCreate:
    @Debug("Создание студента")
    def __call__(self, request):
        logger.log("Создание студента")
        if request["method"] == "POST":
            student_name = request["post_data"]["name"]
            student_lastname = request["post_data"]["lastname"]
            student_email = request["post_data"]["email"]
            student_name = site.decode_value(student_name)
            student_lastname = site.decode_value(student_lastname)
            student_email = site.decode_value(student_email)
            # передаем категорию юзера и его имя
            # остальные поля (фамилия, почта) пока не используем
            new_student = site.create_user("student", student_name)
            site.students.append(new_student)
            # помечаем запись как новую и коммитим
            new_student.mark_new()
            UnitOfWork.get_current().commit()

        page = render("student_create.html", data=request.get("data", None), user_name=request.get("user", None))
        return "200 OK", [bytes(page, "UTF-8")]


@AppRoute(routes=routes, url="/student_list/")
class StudentList:
    def __call__(self, request):
        student_list = MapperRegistry.get_current_mapper("student").all()
        # проходимся по БД и выгружаем всех студентов в engine
        site.students = []  # предварительно очищаем список
        for student in student_list:
            site.students.append(student)

        page = render(
            "student_list.html",
            student_list=site.students,
            data=request.get("data", None),
            user_name=request.get("user", None),
        )
        return "200 OK", [bytes(page, "UTF-8")]


@AppRoute(routes=routes, url="/student_add_course/")
class StudentAddCourse(CreateView):
    template_name = "student_add_course.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["courses_list"] = site.courses
        context["student_list"] = site.students
        return context

    def create_obj(self, data: dict):
        try:
            course_name = data["course_name"]
            course_name = site.decode_value(course_name)
            course = site.get_course(course_name)
            student_name = data["student_name"]
            student_name = site.decode_value(student_name)
            student = site.get_student(student_name)
            course.add_student(student)
        except KeyError as er:
            logger.log(f"KeyError: {er}")


@AppRoute(routes=routes, url="/json_file/")
class JsonFile:
    def __call__(self, request):
        return "200 OK", [bytes(BaseSerializer(site.courses).save(), "UTF-8")]


class PageNotFound:
    @Debug("Страница не найдена")
    def __call__(self, request):
        page = render("not_found.html", data=None)
        return "404 WHAT", [bytes(page, "UTF-8")]
