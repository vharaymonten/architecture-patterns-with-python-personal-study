import datetime
from typing import List, Optional
from pydantic import BaseModel

class Product(BaseModel):
    sku : str 
    name : str

class OrderLine(BaseModel):
    orderid : str 
    sku : str 
    qty : int

class Order(BaseModel):
    orders : List[OrderLine]

class Batch(BaseModel):
    sku : str 
    qty : int
    eta : Optional[datetime.datetime] = None
    order_lines : List[OrderLine] = []

    @property
    def available_quantity(self):
        return self.qty - sum([order_line.qty for order_line in self.order_lines])
    
    @property
    def allocated_quantity(self):
        return sum([order_line.qty for order_line in self.order_lines])
    
    def can_allocate(self, order_line : OrderLine):
        return self.available_quantity >= order_line.qty
    
    def allocate(self, order_line : OrderLine) -> bool:
        if self.can_allocate(order_line):
            self.order_lines.append(order_line)
            return True
        return False 

def test_available_quantity():
    batch = Batch(
        sku="BAJU", 
        qty=1000,
        eta=datetime.datetime.now())
    order_line_1 = OrderLine(
        orderid="1", 
        sku="BAJU", 
        qty=100
        
        )
    order_line_2 = OrderLine(
        orderid="2", 
        sku="BAJU", 
        qty=800
        )

    batch.allocate(order_line_1)
    batch.allocate(order_line_2)

    assert batch.available_quantity == 100