from Base import BaseClass

class Region (BaseClass):#برای ایجاد محله ازش استفادخ میکنیم و تیاز به چیز خاصی نداره 
    def __init__(self,name, *args, **kwargs) -> None:
        
        self.name = name
        
        super().__init__(*args, **kwargs)
