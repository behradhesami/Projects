from user import *
from random import choice
from estate import *
from region import Region
from advertisement import *
from deal import *


First_Name = ['Ali','Hosein','reza']
Last_Name = ['mohseni','rahimi', 'maleki']
Mobiles = ['09305544721','09327538134','09123113959','3203470013','09353427495']


def creat_sample():
    for mobile in Mobiles:
        User(choice(First_Name),choice(Last_Name),mobile)


    #for user in User.object_list:
        #print(f'{user._id}\t {user.fullname}')
reg1 = Region(name = 'Andishe City')
#_-------------------------------------------------------------
aprent = ApartmentRent(user = 'javad', area = 80, room_count = 2,build_year = 1393,
    has_elevetor=True, has_parking= True, floor=3,region = reg1,address = 'some address....',
    initial_price = 100,monthly_price =4.5 )


aprt = ApartmentSell(
    user = 'mohamad', area = 80, room_count = 2,build_year = 1393,
    has_elevetor=True, has_parking= True, floor=3,region = reg1,address = 'some address....',convertable = False,
     price_per_metr = 10, discountable =True             
    )


apartment = ApartmentSell(user = 'ali', area = 80, room_count = 2,build_year = 1393,
    has_elevetor=True, has_parking= True, floor=3,region = reg1,address = 'some address....', convertable = False,
     price_per_metr = 10, discountable =True)

#----------------------------HOUSE--------------------------

hosell = HouseSell('hasan', area = 80, room_count = 2,build_year = 1393,
    region = reg1,address = 'some address....',
    has_yard = True,floors_count = 3,price_per_metr = 36)

horent= HouseRent ('hadi', area = 80, room_count = 2,build_year = 1393,
    region = reg1,address = 'some address....',initial_price = 300, monthly_price = 8,
    has_yard = True,floors_count = 3)


search_result = ApartmentSell.manager.search(price_per_metr__min = 10)#این قسمت برای متود سرچ استفادخ میشه

#print(f'Result : {search_result}')
#print(apartment) , print(apartment.show_detail)