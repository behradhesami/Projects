from estate import *
from deal import *
from Base import BaseClass

class ApartmentSell(BaseClass,Apartment,Sell):    
    def show_detail(self):
        self.show_description()
        self.show_price()
        print("\n")
        
    def __str__(self) -> str:
        return f'Name : {self.user}, {self.area}' 


class ApartmentRent(BaseClass,Apartment,Rent):
    pass



class HouseSell(BaseClass,House,Sell):
    pass


class HouseRent(BaseClass,House,Rent):
    pass

