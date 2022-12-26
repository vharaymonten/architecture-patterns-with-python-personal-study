import abc
from typing import List

import domain
class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch : domain.Batch):
        pass 

    @abc.abstractmethod
    def get(self, reference) -> domain.Batch:
        pass 

class SQLAlchmeyRepository(AbstractRepository):
    def __init__(self, session) -> None:
        self.session = session 

    def add(self, batch: domain.Batch):
        self.session.add(batch)
    
    def get(self, reference) -> domain.Batch:
        return self.session.query(domain.Batch).filter_by(reference=reference).one()

    def list(self):
        return self.session.query(domain.Batch).all()

class FakeRepository(AbstractRepository):
    def __init__(self, batches :List[domain.Batch]) -> None:
        self.batches = batches
    def add(self, batch: domain.Batch):
        self.batches.append(batch)
    def get(self, reference : str):
        for batch in self.batches:
            if batch.reference == reference:
                return batch
        return None
    def list(self):
        return self.batches.copy()
