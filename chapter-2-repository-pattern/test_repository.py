import datetime
import domain
import pytest

@pytest.fixture
def session_with_data(session):

    new_batch1 = domain.Batch(
        reference="1",
        sku="23456",
        _purchased_quantity = 1000,
        eta=datetime.datetime.now(),
    )
    new_batch2 = domain.Batch(
        reference="10",
        sku="12345",
        _purchased_quantity = 1000,
        eta=datetime.datetime.now(),
    )
    session.add(new_batch1)
    session.add(new_batch2)
    session.commit()
    return session

from repository import SQLAlchmeyRepository
def test_repository_list(session_with_data):
    repo = SQLAlchmeyRepository(session=session_with_data)
    
    models = repo.list()
    assert len(models) == 2

def test_add_to_repo(session_with_data):
    repo = SQLAlchmeyRepository(session_with_data)
    batch = domain.Batch(
        reference="1",
        sku="45678",
        _purchased_quantity = 10,
        eta=datetime.datetime.now(),
        )
    order1 = domain.OrderLine(
        "1",
        "45678",
        4
    )
    order2 = domain.OrderLine(
        "1",
        "45678",
        4
    )
    if batch.can_allocate(order1):
        batch.allocate(order1)
    
    if batch.can_allocate(order2):
        batch.allocate(order2)

    repo.add(
        batch
    )
    session_with_data.commit()

    batches = repo.list()
    assert len(batches) == 3

def test_find_to_repo(session_with_data):
    repo = SQLAlchmeyRepository(session_with_data)
    batch = domain.Batch(
        reference="1",
        sku="45678",
        _purchased_quantity = 10,
        eta=datetime.datetime.now(),
        )
    order1 = domain.OrderLine(
        "1",
        "45678",
        4
    )
    order2 = domain.OrderLine(
        "1",
        "45678",
        4
    )
    if batch.can_allocate(order1):
        batch.allocate(order1)
    
    if batch.can_allocate(order2):
        batch.allocate(order2)

    repo.add(
        batch
    )
    session_with_data.commit()

    batches = repo.list()
    assert len(batches) == 3