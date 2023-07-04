
class Manager:#این کلاس برای درست کردن سرچ در برنامه است
    def __init__(self,_class = None) -> None:
        self._class =_class

    def __str__(self) -> str:
        return f'Manager :{self._class}'
    
        

    def search (self,**kwargs):#تمام سرچ هارو ما اون موجودی بهمون تشون میده 
        results = list()
        for key, value in kwargs.items():
            if key.endswith('__min'):#با انجام این کار این قابلیت دادیم ک کاربر 
                key =key[:-5]#بتونه بازه قیمتیو مشخص کنه
                compare_key ='min'
            elif key.endswith ('__max'):#مثلا خونه های بالای 10 میلوین
                key = key[:-5]
                compare_key = 'max'
            else:
                compare_key = 'equal'



            for obj in self._class.object_list:
                if hasattr(obj,key):
                    
                    if compare_key == 'min':
                        resul = bool(getattr(obj, key) >= value)
                    elif compare_key == 'max':
                        resul =bool(getattr (obj,key) <=value) 
                    else:
                        compare_key == 'equal'
                        resul =bool(getattr(obj, key) == value)
                    if resul:
                        results.append(obj)
                        

                    
        return results
        
       
    
    
    
    
    # def get (self,**kwargs):#فقط اولین سرچ بان اون موجودی به ما نمایش میده
    #     results = list()
    #     for key, value in kwargs.items():
    #         for obj in self._class.object_list:
    #             if hasattr(obj,key) and getattr(obj, key) == value:
    #                 return obj
    #     return None