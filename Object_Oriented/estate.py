from abc import ABC,abstractclassmethod
from Base import BaseClass

class EstateAbstract (ABC):

    """this class make shared information between House,Apartment and store"""
    def __init__(self,user,area,room_count,build_year,region,address ,*args, **kwargs) -> None:
        self.user=user
        self.area = area
        self.room_count = room_count
        self.bulid_year = build_year
        self.region = region
        self.address = address

        super().__init__(*args, **kwargs)

    
    @abstractclassmethod
    #This line of code says that all objects must have this and it cannot be changed
    def show_description(self):
        pass


class Apartment(EstateAbstract):#here we builde the atrbiute of aprtment
    def __init__(self,has_elevetor,has_parking,floor, *args, **kwargs) -> None:
        self.has_elevetor = has_elevetor
        self.has_parking = has_parking
        self.floor = floor
        super().__init__(*args,**kwargs)

    
    

    def show_description(self):# Apartment Class must have  this
        print(f'Apartment {self._id}')


class House(EstateAbstract):#here we builde the atrbiute of House
    def __init__(self,has_yard,floors_count,*args,**kwargs):
        self.has_yard = has_yard
        self.floors_count = floors_count

        super().__init__(*args,**kwargs)


    def show_description(self):
        print(f'House: {self._id}')



class Store(EstateAbstract):
    def show_description(self):
        print(f'Store : {self._id}')

