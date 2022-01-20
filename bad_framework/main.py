class Framework:
    def __init__(self, routes, fronts, page_404):
        self.routes = routes
        self.fronts = fronts
        self.page_404 = page_404

    def __call__(self, environ, start_response):

        path = environ["PATH_INFO"]

        if not path.endswith("/"):
            path = f"{path}/"

        if path in self.routes:
            view = self.routes[path]
        else:
            view = self.page_404
        request = {}
        # front controller
        for front in self.fronts:
            front(request)
        code, body = view(request)
        start_response(code, [("Content-Type", "text/html")])
        return body
