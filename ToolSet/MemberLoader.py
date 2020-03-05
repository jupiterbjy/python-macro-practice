import inspect
import re
from sys import modules

'''
Return list of target, i.e. Class or Function in target module.
Main usage is for generating __all__ upon function defining.

i.e.
__all__ = member_loader.ListFunction(__name__, name_only = True)

Blacklist only supported for array return.

On default will follow python's way, ignoring case starting with underscore.
'''
# TODO: add dict key remove for blacklist


def ListTarget(name, target, prefix_mode, blacklist, return_target):

    if prefix_mode and blacklist is None:
        blacklist = {'_'}

    elif blacklist is None:
        blacklist = {}

    members = inspect.getmembers(modules[name], target)

    if prefix_mode:
        exclude = ''.join([str(i) for i in blacklist])
        regex = '^[' + exclude + ']'

        filtered = [i for i in members if not bool(re.match(regex, i[0]))]
    else:
        filtered = [i for i in members if i[0] not in blacklist]

    sorted(filtered)

    if return_target:
        return filtered

    else:
        return [i for i, _ in filtered]


def ListClass(name, prefix_mode=True, blacklist=None, return_target=False):
    return ListTarget(name, inspect.isclass, prefix_mode, blacklist, return_target)


def ListFunction(name, prefix_mode=True, blacklist=None, return_target=False):
    return ListTarget(name, inspect.isfunction, prefix_mode, blacklist, return_target)
