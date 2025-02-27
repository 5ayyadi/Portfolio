"""
This file contains the error schema for the application
which is used to handle errors in the application
"""
class BaseError(Exception):
    msg = "Base Exeption"
    reason = ""

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if request:
            self.request = request


    def __str__(self):
        return f'{self.__class__.__name__}-{self.msg}'


class UnauthorizedAccess(BaseError):
    msg = "Unauthorized Access"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    
class NoResultFound(BaseError):
    msg = "No Result Found"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
class WrongInput(BaseError):
    msg = "Wrong Input"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        