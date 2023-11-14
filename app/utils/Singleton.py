#----------------------------------------------------------------------------------------------------

    # Class
class Singleton(type):
    '''Metaclasse qui permet de créer des Singleton.
    ```py
    class MyClass(metaclass = Singleton):
        pass
    ```'''

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
#----------------------------------------------------------------------------------------------------
