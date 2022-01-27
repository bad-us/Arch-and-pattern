from bad_framework.requests import parse_input_data, get_request_params
import quopri

class Framework:
    def __init__(self, routes, fronts, page_404):
        self.routes = routes
        self.fronts = fronts
        self.page_404 = page_404

    def __call__(self, environ, start_response):

        path = environ["PATH_INFO"]

        # Lesson_1
        # if not path.endswith("/"):
        #     path = f"{path}/"
        #
        # if path in self.routes:
        #     view = self.routes[path]
        # else:
        #     view = self.page_404
        # request = {}
        # # front controller
        # for front in self.fronts:
        #     front(request)
        # code, body = view(request)
        # start_response(code, [("Content-Type", "text/html")])
        # return body

        if not path.endswith("/"):
            path = f"{path}/"

        request = {}
        # Метод которым отправили запрос
        method = environ["REQUEST_METHOD"]
        request["method"] = method

        if method == "GET":
            query_string = environ["QUERY_STRING"]  # получаем содержимое запроса - строку
            get_request = parse_input_data(query_string)
            request["get_data"] = get_request
            print(f"Получен GET запрос: {get_request}")
        if method == "POST":
            data = get_request_params(environ)
            request["post_data"] = data
            print(f"Получен POST запрос: {Framework.decode_value(data)}")

        if path in self.routes:
            view = self.routes[path]
        else:
            view = self.page_404

        # front controller
        for front in self.fronts:
            front(request)

        code, body = view(request)
        start_response(code, [("Content-Type", "text/html")])
        return body


    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace("%", "=").replace("+", " "), "UTF-8")
            val_decode_str = quopri.decodestring(val).decode("UTF-8")
            new_data[k] = val_decode_str
        return new_data
