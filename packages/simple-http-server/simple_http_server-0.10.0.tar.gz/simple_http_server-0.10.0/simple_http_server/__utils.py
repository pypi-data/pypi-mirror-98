
from collections import OrderedDict
import inspect


def remove_url_first_slash(url: str):
    _url = url
    while _url.startswith("/"):
        _url = url[1:]
    return _url


def get_function_args(func, default_type=str):
    argspec = inspect.getfullargspec(func)
    # ignore first argument like `self` or `clz` in object methods or class methods
    start = 1 if inspect.ismethod(func) else 0
    if argspec.defaults is None:
        args = argspec.args[start:]
    else:
        args = argspec.args[start: len(argspec.args) - len(argspec.defaults)]
    arg_turples = []
    for arg in args:
        if arg in argspec.annotations:
            ty = argspec.annotations[arg]
        else:
            ty = default_type
        arg_turples.append((arg, ty))
    return arg_turples


def get_function_kwargs(func, default_type=str):
    argspec = inspect.getfullargspec(func)
    if argspec.defaults is None:
        return []

    kwargs = OrderedDict(zip(argspec.args[-len(argspec.defaults):], argspec.defaults))
    kwarg_turples = []
    for k, v in kwargs.items():
        if k in argspec.annotations:
            k_anno = argspec.annotations[k]
        else:
            k_anno = default_type
        kwarg_turples.append((k, v, k_anno))
    return kwarg_turples
