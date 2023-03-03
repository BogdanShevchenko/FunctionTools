from collections.abc import Callable, Sequence

def get_args_dict(f: Callable, args: Sequence, kwargs: dict) -> dict:
    """
    By given function and passed args list and kwargs dict, return dictionary with names and values of all arguments,
    passed to the function, including defaults for those which wasn't passed
    :param f: any function
    :param args: all positional arguments, passed to function
    :param kwargs: all named arguments passed to function
    :return: dictionary with all parameters of the function
    """
    varnames = f.__code__.co_varnames
    pos_arg_count = min(f.__code__.co_argcount, len(args))
    flags = '{:04b}'.format(f.__code__.co_flags)
    has_args = int(flags[-3])
    has_kwargs = int(flags[-4])
    kwarg_name = [None, varnames[-1]][has_kwargs]
    arg_name = [None, varnames[-1 - has_kwargs]][has_args]
    kwargs.update(zip(varnames[:pos_arg_count], args[:pos_arg_count]))
    if has_args:
        kwargs[arg_name] = args[pos_arg_count:]
        defaults = f.__kwdefaults__
    else:
        args_from_named = varnames[pos_arg_count: len(args)]
        args_from_named_values = args[pos_arg_count:]
        kwargs.update(zip(args_from_named, args_from_named_values))

        defaults = f.__defaults__
        defaults = dict(zip(
            varnames[-len(defaults) - has_kwargs:(-1 if has_kwargs else None)],
            f.__defaults__
        ))
    if has_kwargs:
        kwargs[kwarg_name] = {i: kwargs[i] for i in kwargs if i not in varnames}
    defaults.update(kwargs)
    return defaults
