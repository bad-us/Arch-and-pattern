from jinja2 import Template
import os
from jinja2 import FileSystemLoader
from jinja2.environment import Environment



def render(template_name, folder="templates", **kwargs):
    # file_path = os.path.join(folder, template_name)
    # with open(file_path, encoding="utf-8") as f:
    #     template = Template(f.read())
    # return template.render(**kwargs) Lesson 2
    env = Environment()
    # указываем папку для поиска шаблонов
    env.loader = FileSystemLoader(folder)
    # находим шаблон в окружении
    template = env.get_template(template_name)
    return template.render(**kwargs)
