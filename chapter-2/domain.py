from dataclasses import dataclass
import datetime
from typing import List, Optional, Set
from pydantic import BaseModel, dataclasses

# class Product(BaseModel):
#     sku : str 
#     name : str

@dataclasses.dataclass(unsafe_hash=True)
class OrderLine:
    orderid : str 
    sku : str 
    qty : int
    
class Order(BaseModel):
    orders : List[OrderLine]

from dataclasses import field
@dataclasses.dataclass(unsafe_hash=True)
class Batch:
    reference : str
    sku : str
    _purchased_quantity : int = field(default_factory= lambda : 0)
    eta  : Optional[datetime.date] = None
    _allocations : Set[OrderLine]= field(default_factory= set)

    @property
    def available_quantity(self):
        return self._purchased_quantity - sum([order_line.qty for order_line in self._allocations])
    
    @property
    def allocated_quantity(self):
        return sum([order_line.qty for order_line in self._allocations])
    
    def can_allocate(self, order_line : OrderLine):
        return self.available_quantity >= order_line.qty
    
    def allocate(self, order_line : OrderLine) -> bool:
        if self.can_allocate(order_line):
            self._allocations.add(order_line)
            return True
        return False 
    # def __hash__(self):
    #     return self.reference

# def test_available_quantity():
#     batch = Batch(
#         sku="BAJU", 
#         qty=1000,
#         eta=datetime.datetime.now())
#     order_line_1 = OrderLine(
#         orderid="1", 
#         sku="BAJU", 
#         qty=100
        
#         )
#     order_line_2 = OrderLine(
#         orderid="2", 
#         sku="BAJU", 
#         qty=800
#         )

#     batch.allocate(order_line_1)
#     batch.allocate(order_line_2)

#     assert batch.available_quantity == 100

# # from __future__ import annotations
# from dataclasses import dataclass
# from datetime import date
# from typing import Optional, List, Set


# class OutOfStock(Exception):
#     pass




# @dataclass(unsafe_hash=True)
# class OrderLine:
#     orderid: str
#     sku: str
#     qty: int


# class Batch:
#     def __init__(self, ref: str, sku: str, qty: int, eta: Optional[datetime.date]):
#         self.reference = ref
#         self.sku = sku
#         self.eta = eta
#         self._purchased_quantity = qty
#         self._allocations = set()  # type: Set[OrderLine]

#     def __repr__(self):
#         return f"<Batch {self.reference}>"

#     def __eq__(self, other):
#         if not isinstance(other, Batch):
#             return False
#         return other.reference == self.reference

#     def __hash__(self):
#         return hash(self.reference)

#     def __gt__(self, other):
#         if self.eta is None:
#             return False
#         if other.eta is None:
#             return True
#         return self.eta > other.eta

#     def allocate(self, line: OrderLine):
#         if self.can_allocate(line):
#             self._allocations.add(line)

#     def deallocate(self, line: OrderLine):
#         if line in self._allocations:
#             self._allocations.remove(line)

#     @property
#     def allocated_quantity(self) -> int:
#         return sum(line.qty for line in self._allocations)

#     @property
#     def available_quantity(self) -> int:
#         return self._purchased_quantity - self.allocated_quantity

#     def can_allocate(self, line: OrderLine) -> bool:
#         return self.sku == line.sku and self.available_quantity >= line.qty


def allocate(line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f"Out of stock for sku {line.sku}")