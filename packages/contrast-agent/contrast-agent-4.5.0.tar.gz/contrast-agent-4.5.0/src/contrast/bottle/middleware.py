# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.wsgi.middleware import WSGIMiddleware
from contrast.utils.decorators import fail_safely, fail_quietly
from contrast.extern import structlog as logging
from contrast.agent.middlewares.route_coverage.bottle_routes import (
    create_bottle_routes,
    build_bottle_route,
)

logger = logging.getLogger("contrast")


class BottleMiddleware(WSGIMiddleware):
    # Since Bottle is WSGI-based, there is no way to retrieve the app name.
    # Use common config to define an app name.
    def __init__(self, app):
        super(BottleMiddleware, self).__init__(app, app_name="Bottle Application")

    @fail_safely("Unable to get route coverage", return_value={})
    def get_route_coverage(self):
        return create_bottle_routes(self.wsgi_app)

    @fail_quietly("Unable to get Bottle view func")
    def get_view_func(self, request):
        path = request.path
        if not path:
            return None
        method = request.method
        route_info = self.wsgi_app.match({"PATH_INFO": path, "REQUEST_METHOD": method})
        if not route_info:
            return None
        view_func = route_info[0].callback
        return view_func

    @fail_safely("Unable to build route", return_value="")
    def build_route(self, view_func, url):
        return build_bottle_route(url, view_func)
