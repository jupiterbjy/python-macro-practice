"""
Mimics Singledispatch, but for objects.
"""


class dispatchObject:
    def __init__(self, func=None):
        self.function_map = {}
        self.default = self.template if func is None else func

    def __call__(self, *args, **kwargs):
        return self.dispatch(*args, **kwargs)

    def template(self, *args, **kwargs):
        raise RuntimeError('Default function is not assigned to function_map.')

    def dispatch(self, obj, *args, **kwargs):
        print(self.function_map)

        return self.function_map.get(type(obj), self.default)


# https://stackoverflow.com/questions/5929107/decorators-with-parameters
# Referred this.
def register(dispatch_obj, type_obj):
    def decorator(func):
        dispatch_obj.function_map[type_obj] = func

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator
