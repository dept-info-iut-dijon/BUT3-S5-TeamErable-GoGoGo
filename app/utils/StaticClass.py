#----------------------------------------------------------------------------------------------------

    # Class
class StaticClass(type):
    '''Metaclasse qui permet de créer des classes statiques.
    ```py
    class MyClass(metaclass = StaticClass):
        pass
    ```'''

    def __new__(cls, *args, **kwargs) -> None:
        return None
#----------------------------------------------------------------------------------------------------
