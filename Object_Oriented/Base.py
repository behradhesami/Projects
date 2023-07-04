from abc import ABC
from manager import Manager 

class BaseClass(ABC): #no instanse
    _id =0
    object_list = None
    manager = None

    def __init__(self,*args,**kwargs) -> None:
        self._id = self.generator_id()
        self.store (self)
        self.set_manager()
        super().__init__(*args,**kwargs)

    @classmethod # هر بار که کلاس اجرا میشه ۱ دونه ب آی دی ها اعضافه میشه
    def generator_id(cls):
        cls._id +=1
        return cls._id
    

    @classmethod
    def set_manager(cls):
        if cls.manager is  None:
            cls.manager = Manager(cls)


    @classmethod #اینجا چون دیتا بیس نداریم برای ذحیره ازش استفاده میکنیم برای تست 
    def store(cls,obj):
        if cls.object_list is None:
            cls.object_list = list()
        cls.object_list.append(obj)
        

    