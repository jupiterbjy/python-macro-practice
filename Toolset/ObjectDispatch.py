"""
Mimics singledispatch, but for objects.
use decorator function 'register' to do what that name implies.
"""


class dispatcher:
    def __init__(self, default=None):
        self.function_map = {}
        self.registerNotice = True
        self.default = self.template if default is None else default

    def __call__(self, obj, *args, **kwargs):
        return self.dispatch(obj, *args, **kwargs)

    def template(self, *args, **kwargs):
        raise RuntimeError('Default function is not assigned to function_map.')

    def dispatch(self, obj, *args, **kwargs):
        return self.function_map.get(str(type(obj)), self.default)(obj)

    def register(self, type_obj):

        def decorator(func):

            self.function_map[str(type_obj)] = func

            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper
        return decorator


def obj_dispatch():
    def deco(func):
        function_map = {}
        default = func

        def wrapper(obj, *args, **kwargs):
            nonlocal function_map, default

            def register(_obj, _func):
                function_map[type(_obj)] = _func

            if t := type(obj) in function_map:
                out = function_map[t]
            else:
                out = default

            out(obj, *args, **kwargs)

        return wrapper
    return deco
