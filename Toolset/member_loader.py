import inspect
from sys import modules

'''
Return list of target, i.e. Class or Function in target module.
Main usage is for generating __all__ upon function defining.

i.e.
__all__ = member_loader.ListFunction(__name__, name_only = True)

Blacklist only supported for array return, I have no time.
'''
# TODO: add dict key remove for blacklist


def ListTarget(name, target, name_only, blacklist):
    if blacklist is None:
        blacklist = {}

    members = inspect.getmembers(modules[name], target)

    if name_only:
        results = {a for a, _ in members}
        results -= blacklist
        return results
    
    else:
        return members
    
    
def ListClass(name, name_only=True, blacklist=None):
    return ListTarget(name, inspect.isclass, name_only, blacklist)


def ListFunction(name, name_only=True, blacklist=None):
    return ListTarget(name, inspect.isfunction, name_only, blacklist)