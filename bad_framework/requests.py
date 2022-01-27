def parse_input_data(data):
    result = {}
    if data:
        # делим параметры через &
        params = data.split("&")
        for item in params:
            # делим ключ и значение через =
            k, v = item.split("=")
            result[k] = v
    return result


def get_wsgi_input_data(env) -> bytes:
    # получаем длину тела
    content_length_data = env.get("CONTENT_LENGTH")
    # приводим к int
    content_length = int(content_length_data) if content_length_data else 0
    # считываем данные если они есть
    data = env["wsgi.input"].read(content_length) if content_length > 0 else b""
    return data


def parse_wsgi_input_data(data: bytes) -> dict:
    result = {}
    if data:
        # декодируем данные
        data_str = data.decode(encoding="utf-8")
        # собираем их в словарь
        result = parse_input_data(data_str)
    return result


def get_request_params(environ):
    # получаем данные
    data = get_wsgi_input_data(environ)
    # превращаем данные в словарь
    dict_data = parse_wsgi_input_data(data)
    return dict_data