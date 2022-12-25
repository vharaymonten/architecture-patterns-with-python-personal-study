import datetime
import domain
import pytest

@pytest.fixture
def fake_batches():

    new_batch1 = domain.Batch(
        reference="1",
        sku="23456",
        _purchased_quantity = 1000,
        eta=datetime.datetime.now(),
        _allocations={
            domain.OrderLine("1", "23456", 100),
            domain.OrderLine("2", "23456", 90),
            domain.OrderLine("3", "23456", 810)
        }
    )
    new_batch2 = domain.Batch(
        reference="10",
        sku="12345",
        _purchased_quantity = 1000,
        eta=datetime.datetime.now(),
        _allocations={
            domain.OrderLine("10", "12345", 100),
            domain.OrderLine("11", "12345", 90),
            domain.OrderLine("12", "12345", 810)
        }
    )
    new_batch3 = domain.Batch(
        reference="10",
        sku="34567",
        _purchased_quantity = 1000,
        eta=datetime.datetime.now(),
        _allocations={
            domain.OrderLine("30", "34567", 100),
            domain.OrderLine("31", "34567", 90),
            domain.OrderLine("32", "34567", 810)
        }
    )
    return [new_batch1, new_batch2, new_batch3]
from repository import FakeRepository
def test_repository_list(fake_batches):
    repo = FakeRepository(fake_batches)
    batches = repo.list()
    return len(batches) == 3

def test_repository_add(fake_batches):
    repo = FakeRepository(fake_batches)
    new_batch4 = domain.Batch(
        reference="30",
        sku="345678",
        _purchased_quantity = 1000,
        eta=datetime.datetime.now())

    repo.add(new_batch4)
    assert len(repo.list()) == 4