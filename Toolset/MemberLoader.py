from sys import modules
import inspect
import re


def ListTarget(name, target, prefix_mode, blacklist, return_dict):
    """
    Return list of target, i.e. Class or Function in target module.
    Main usage is for generating __all__ upon function defining.

    i.e.
    __all__ = member_loader.ListFunction(__name__, name_only = True)

    Blacklist only supported for array return.

    On default will follow python's way, ignoring case starting with underscore.
    """

    if prefix_mode and blacklist is None:
        blacklist = {"_"}

    elif blacklist is None:
        blacklist = {}

    members = inspect.getmembers(modules[name], target)

    if prefix_mode:
        exclude = "".join([str(i) for i in blacklist])
        regex = "^[" + exclude + "]"

        filtered = [i for i in members if not bool(re.match(regex, i[0]))]
    else:
        filtered = [i for i in members if i[0] not in blacklist]

    sorted(filtered)

    if return_dict:
        return FunctionToDict([i for _, i in filtered])

    return [i for i, _ in filtered]


def ListClass(name, prefix_mode=True, blacklist=None, return_dict=False):
    return ListTarget(name, inspect.isclass, prefix_mode, blacklist, return_dict)


def ListFunction(name, prefix_mode=True, blacklist=None, return_dict=False):
    return ListTarget(name, inspect.isfunction, prefix_mode, blacklist, return_dict)


def FunctionToDict(func_list):
    return dict((i.__name__, i) for i in func_list)
