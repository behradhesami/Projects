from Base import *

class User(BaseClass):# here we builde seller information 

    def __init__(self,firstname,lastname,phonnumber,*args,**kwargs) -> None:
        self.firstname = firstname
        self.lastname = lastname
        self.phonnumber = phonnumber
        super().__init__(*args,**kwargs)


    @property
    def fullname(self):
        return f"{self.firstname} {self.lastname}"