import datetime
import domain
def test_orderline_mapper_can_load_lines(session):
    session.execute(
        "INSERT INTO order_lines (orderid, sku, qty) VALUES "
        "('1', 'RED-CHAIR', 12),"
        "('2', 'RED-TABLE', 13),"
        "('3', 'GREEN-CHAIR', 14)"
    )

    expected = [
        domain.OrderLine(orderid="1", sku='RED-CHAIR', qty=12),
        domain.OrderLine(orderid="2", sku='RED-TABLE', qty=13),
        domain.OrderLine(orderid="3", sku='GREEN-CHAIR', qty=14)
    ]

    assert session.query(domain.OrderLine).all() == expected

def test_orderline_can_save_to_orm(session):
    newline = domain.OrderLine("1", 'DECORATIVE-WIDGET', 100)
    session.add(newline)
    session.commit()
    rows = list(session.execute("SELECT orderid, sku, qty FROM 'order_lines' "))
    assert rows == [("1", 'DECORATIVE-WIDGET', 100)]

def test_orm_can_save_batch(session):
    new_batch = domain.Batch(
        reference="10",
        sku="MAPPA",
        qty=1000,
        eta=datetime.datetime.now(),
    )

    session.add(new_batch)
    session.commit()
def test_orm_can_save_map_order_line(session):
    new_batch = domain.Batch(
        reference="10",
        sku="MAPPA",
        _purchased_quantity = 1000,
        eta=datetime.datetime.now(),
    )
    new_batch.allocate(domain.OrderLine("1", "HAPPA", 10))
    session.add(new_batch)
    session.commit()
    batch : domain.Batch = session.query(domain.Batch).filter_by(reference="10").one()
    assert batch.available_quantity == 990

def test_allocations(session):
    new_batch = domain.Batch(
        reference="10",
        sku="MAPPA",
        _purchased_quantity = 1000,
        eta=datetime.datetime.now(),
    )
    new_batch.allocate(domain.OrderLine("1", "HAPPA", 10))
    session.add(new_batch)
    session.commit()
    batch : domain.Batch = session.query(domain.Batch).filter_by(reference="10").one()
    orderline = batch._allocations.pop()
    assert orderline.orderid == "1"
    assert orderline.qty == 10