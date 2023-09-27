from abc import ABC, abstractmethod
from ..models import Laptop


class ConcreteComponent(Laptop):
    def get_price(self):
        # Calculate the base price of the laptop
        return self.price


class BaseDecorator(Laptop):
   

    """The base Decorator class follows the same interface as the other components.
    The primary purpose of this class is to define the wrapping interface for all
    concrete decorators.
    """
    _component:Laptop=None
    def __init__(self, component:Laptop):
        self._component = component   # Aggregation 
        
    @property 
    def component(self):
        return self._component

    def get_price(self):
        return self._component.get_price()
    

class ConcreteDecoratorRam(BaseDecorator):
   
    """Concrete Decorator class for adding RAM specification to the laptop.
    """
    def __init__(self, component: Laptop, ram_capacity: int):
        super().__init__(component)
        self.ram_capacity = ram_capacity
    def get_price(self):
        base_price = super().get_price()
        ram_price_adjustment= (self.ram_capacity -self.component.get_ram_capacity())*10
        return base_price +  ram_price_adjustment
    
    def __str__(self):
        return f"upgrade Ram {self.ram_capacity}"

class ConcreteDecoratorSSD(BaseDecorator):
   
    """Concrete Decorator class for adding SSD specification to the laptop.
    """
    def __init__(self, component, ssd_capacity: int):
        super().__init__(component)
        self.ssd_capacity = ssd_capacity
    

    def get_price(self):
        base_price = super().get_price()
       
        ssd_price_adjustment=(self.ssd_capacity-self.component.component.ssd.capacity)*5
        return base_price + ssd_price_adjustment
    def __str__(self):
        return f"upgrade SSD {self.ssd_capacity}"
