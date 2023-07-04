from estate import *


class Sell(ABC):
    def __init__(self,price_per_metr,discountable= False,convertable = True, *args, **kwargs) -> None:

        self.price_per_metr = price_per_metr
        self.discountable = discountable
        self.convertable = convertable

        super().__init__(*args, **kwargs)
    
    def show_price(self):
        print(f'price: {self.price_per_metr}\t discount: {self.discountable}\t convert: {self.convertable}')


class Rent(ABC):
    def __init__(self,initial_price,monthly_price,convertable = False,discountable = True, *args, **kwargs) -> None:

        self.initial_price = initial_price
        self.monthly_price = monthly_price
        self.convertable = convertable
        self.discountable = discountable

        super().__init__(*args, **kwargs)
