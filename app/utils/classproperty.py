#----------------------------------------------------------------------

    # Class
class classproperty(property):
    '''Décorateur qui permet de créer des propriétés de classe.

    ```py
    @classproperty
    def function(cls):
        return 'something'
    ```'''
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()
#----------------------------------------------------------------------
