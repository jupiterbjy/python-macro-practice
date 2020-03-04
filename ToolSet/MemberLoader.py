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


def ListTarget(name, target, prefix_mode, blacklist):
    if prefix_mode and blacklist is None:
        blacklist = {'_'}

    elif blacklist is None:
        blacklist = {}

    members = inspect.getmembers(modules[name], target)
    results = {a for a, _ in members}

    if not prefix_mode:
        results -= blacklist
        return sorted(results)
    
    else:
        exclude = ''.join([str(i) for i in blacklist])
        regex = '^[' + exclude + ']'

        return sorted(i for i in results if not bool(re.match(regex, i)))


def ListClass(name, prefix_mode=True, blacklist=None):
    return ListTarget(name, inspect.isclass, prefix_mode, blacklist)


def ListFunction(name, prefix_mode=True, blacklist=None):
    return ListTarget(name, inspect.isfunction, prefix_mode, blacklist)
