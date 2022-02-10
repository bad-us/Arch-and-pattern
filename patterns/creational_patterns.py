import copy
import quopri


# Пользователи
# Абстрактный пользователь
class User:
    pass


# Учитель
class Teacher(User):
    pass


# Студент
class Student(User):
    pass


# Наставник
class Mentor(User):
    pass


# порождающий паттерн Абстрактная фабрика - фабрика пользователей
class UserFactory:
    types = {"student": Student, "teacher": Teacher, "mentor": Mentor}

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


# порождающий паттерн Прототип
class CoursePrototype:
    # прототип курсов обучения

    def clone(self):
        return copy.deepcopy(self)


class Course(CoursePrototype):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


# Типы курсов
# Вебинарный формат
class WebinarCourse(Course):
    pass


# Курс в записи
class RecordCourse(Course):
    pass


# Курс проходит в аудиториях
class ClassroomCourse(Course):
    pass


class CourseFactory:
    types = {"webinar": WebinarCourse, "record": RecordCourse, "classroom": ClassroomCourse}

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


# Категория
class Category:
    id = 1

    def __init__(self, name):
        self.id = Category.id
        Category.id += 1
        self.name = name
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        return result


# Основной интерфейс проекта
class Engine:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    @staticmethod
    def create_category(name):
        return Category(name)

    def find_category_by_id(self, id):
        for item in self.categories:
            if item.id == id:
                return item
        # нет id - бросаем исключение
        raise KeyError

    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory.create(type_, name, category)

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace("%", "=").replace("+", " "), "UTF-8")
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode("UTF-8")


# порождающий паттерн Синглтон
class Singleton(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs["name"]

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=Singleton):
    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print("log file >>> ", text)
