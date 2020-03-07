"""
Mimics Singledispatch, but only for objects.
"""


# def objectdispatch(func):
#
#     func_dic = None
#
#     def dispatch(cls):
#         nonlocal func_dic
#         if func_dic is not None:
#
#     def register(cls, func):
#         # TODO: add error handling
#
#         nonlocal func_dic
#         func_dic[cls] = func
#         return func
#
#     def wrapper(*args, **kwargs):
#         nonlocal func_dic
#         if not args:
#             raise TypeError('no argument is given.')
#
#         return func_dic[type(args[0])](*args, **kwargs)
#
#         wrapper.register


# class ObjectDispatch:
#     def __init__(self, object_list, default):
#         self.object_list = object_list
#         self.function_map = {}
#         self.default_behavior = default
#
#     def register(self, func, obj_type):
#         self.function_map['obj_type'] = func
#         return func
#
#     @staticmethod
#     def deco(source, obj):
#         if type(obj) in source.object_list:
#             return source.function_map[type(obj)]
#
#         else:
#             return source.default_behavior
#
#     def __call__(self, *args, **kwargs):
#         return self.register(self, *args, **kwargs)

def singledispatch(func):
    """
    Copy of code from functools.
    """
    # There are many programs that use functools without singledispatch, so we
    # trade-off making singledispatch marginally slower for the benefit of
    # making start-up of such applications slightly faster.
    import types, weakref

    registry = {}
    dispatch_cache = weakref.WeakKeyDictionary()
    cache_token = None

    def dispatch(cls):
        """generic_func.dispatch(cls) -> <function implementation>

        Runs the dispatch algorithm to return the best available implementation
        for the given *cls* registered on *generic_func*.

        """
        nonlocal cache_token
        if cache_token is not None:
            current_token = get_cache_token()
            if cache_token != current_token:
                dispatch_cache.clear()
                cache_token = current_token
        try:
            impl = dispatch_cache[cls]
        except KeyError:
            try:
                impl = registry[cls]
            except KeyError:
                impl = _find_impl(cls, registry)
            dispatch_cache[cls] = impl
        return impl

    def register(cls, func=None):
        """generic_func.register(cls, func) -> func

        Registers a new implementation for the given *cls* on a *generic_func*.

        """
        nonlocal cache_token
        if func is None:
            if isinstance(cls, type):
                return lambda f: register(cls, f)
            ann = getattr(cls, '__annotations__', {})
            if not ann:
                raise TypeError(
                    f"Invalid first argument to `register()`: {cls!r}. "
                    f"Use either `@register(some_class)` or plain `@register` "
                    f"on an annotated function."
                )
            func = cls

            # only import typing if annotation parsing is necessary
            from typing import get_type_hints
            argname, cls = next(iter(get_type_hints(func).items()))
            if not isinstance(cls, type):
                raise TypeError(
                    f"Invalid annotation for {argname!r}. "
                    f"{cls!r} is not a class."
                )
        registry[cls] = func
        if cache_token is None and hasattr(cls, '__abstractmethods__'):
            cache_token = get_cache_token()
        dispatch_cache.clear()
        return func

    def wrapper(*args, **kw):
        if not args:
            raise TypeError(f'{funcname} requires at least '
                            '1 positional argument')

        return dispatch(args[0].__class__)(*args, **kw)

    funcname = getattr(func, '__name__', 'singledispatch function')
    registry[object] = func
    wrapper.register = register
    wrapper.dispatch = dispatch
    wrapper.registry = types.MappingProxyType(registry)
    wrapper._clear_cache = dispatch_cache.clear
    update_wrapper(wrapper, func)
    return wrapper


if __name__ == '__main__':

    class a:
        def aa(self):
            print('bla!')

    def c():
        print('default!')

    b = ObjectDispatch(obj_list, c)

    @b(a)
    def d():
        print('Fla!')




