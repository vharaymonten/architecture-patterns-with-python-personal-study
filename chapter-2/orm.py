from sqlalchemy import String, Integer, String, Column, MetaData, Table, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapper, relationship
from sqlalchemy import create_engine

metadata = MetaData()

order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("qty", Integer, nullable=False),
    Column("orderid", String(255))
)

batches = Table(
    "batches",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(255)),
    Column("sku", String(255)),
    Column("_purchased_quantity", Integer, nullable=False),
    Column("eta", Date, nullable=True),
)

allocations = Table(
    "allocation",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("orderline_id", ForeignKey("order_lines.id")),
    Column("batch_id", ForeignKey("batches.id"))
)

import domain

def start_mappers():
    lines_mapper = mapper(domain.OrderLine, order_lines)
    mapper(
        domain.Batch,
        batches,
        properties = {
            "_allocations" : relationship(
                lines_mapper, secondary=allocations, collection_class=set
            )
        }
    )

#engine = create_engine('sqlite:///database.db')
#metadata.create_all(bind=engine, tables=[order_lines, batches, allocations])
