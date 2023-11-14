#----------------------------------------------------------------------

    # Libraries
import functools
import inspect
import warnings
#----------------------------------------------------------------------

    # Setup
string_types = (type(b''), type(u''))
#----------------------------------------------------------------------
    # Class
def deprecated(reason: str):
    '''Décorateur qui permet de marquer une fonction comme dépréciée. Cela émettra un avertissement lors de l'utilisation de la fonction.

    Si le `@deprecated` est utilisé avec une 'reason':
    ```py
    @deprecated('please, use another function')
    def old_function(x, y):
        pass
    ```

    Si le `@deprecated` est utilisé sans 'reason':
    ```py
    @deprecated
    def old_function(x, y):
        pass
    ```'''

    if isinstance(reason, string_types):
        # Le `@deprecated` est utilisé avec une 'reason'.
        # ```py
        # @deprecated('please, use another function')
        # def old_function(x, y):
        #     pass
        # ```

        def decorator(func1):

            if inspect.isclass(func1):
                fmt1 = 'Call to deprecated class <{name}> -> {reason}'
            else:
                fmt1 = 'Call to deprecated function <{name}> -> {reason}'

            @functools.wraps(func1)
            def new_func1(*args, **kwargs):
                warnings.simplefilter('always', DeprecationWarning)
                warnings.warn(
                    fmt1.format(name = func1.__name__, reason = reason),
                    category = DeprecationWarning,
                    stacklevel = 2
                )
                warnings.simplefilter('default', DeprecationWarning)
                return func1(*args, **kwargs)

            return new_func1

        return decorator

    elif inspect.isclass(reason) or inspect.isfunction(reason):

        # Le `@deprecated` est utilisé sans 'reason'.
        # ```py
        # @deprecated
        # def old_function(x, y):
        #     pass
        # ```

        func2 = reason

        if inspect.isclass(func2):
            fmt2 = 'Call to deprecated class <{name}>'
        else:
            fmt2 = 'Call to deprecated function <{name}>'

        @functools.wraps(func2)
        def new_func2(*args, **kwargs):
            warnings.simplefilter('always', DeprecationWarning)
            warnings.warn(
                fmt2.format(name = func2.__name__),
                category = DeprecationWarning,
                stacklevel = 2
            )
            warnings.simplefilter('default', DeprecationWarning)
            return func2(*args, **kwargs)

        return new_func2

    else:
        raise TypeError(repr(type(reason)))
#----------------------------------------------------------------------
