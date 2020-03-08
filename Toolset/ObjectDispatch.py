"""
Mimics Singledispatch, but for objects.
"""


class dispatchObject:
    def __init__(self, func=None):
        self.function_map = {}
        self.default = self.template if func is None else func

    def __call__(self, obj, *args, **kwargs):
        return self.dispatch(obj, *args, **kwargs)

    def template(self, *args, **kwargs):
        raise RuntimeError('Default function is not assigned to function_map.')

    def dispatch(self, obj, *args, **kwargs):
        return self.function_map.get(str(type(obj)), self.default)(obj)


# https://stackoverflow.com/questions/5929107/decorators-with-parameters
# Referred this.
def register(dispatch_obj, type_obj):
    def decorator(func):
        dispatch_obj.function_map[str(type_obj)] = func

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


def mainDispatch():
    # TODO: change decorator so wrapper 'CreateDispatcher' is not required.
    pass