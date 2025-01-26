from base import BaseClass
from estate import Apartment, House, Store
from deal import Rent, Sell


class ApartmentSell(BaseClass, Apartment, Sell):

    def show_detail(self):
        self.show_description()
        self.show_price()
    def show(self) :
        return"Apartment for Sell: " 


class ApartmentRent(BaseClass, Apartment, Rent):
    def show_detail(self):
        self.show_description()
        # self.show_price()
    def show(self) :
        return"Apartment for Rent: " 
         

class HouseSell(BaseClass, House, Sell):
    def show_detail(self):
        self.show_description()
        self.show_price()
    def show(self) :
        return"House for Sell: " 
         

class HouseRent(BaseClass, House, Rent):
    def show_detail(self):
        self.show_description()
        self.show_price()
    def show(self) :
        return"House for Rent: " 
 
    
class StoreSell(BaseClass, Store, Sell):
    def show_detail(self):
        self.show_description()
        self.show_price()
    def __str__(self):
        return"Apartment for Sell: " 


class StoreRent(BaseClass, Store, Rent):
    def show_detail(self):
        self.show_description()
        self.show_price()
    def __str__(self) -> str:
        print( "ApartMent For Sell :")