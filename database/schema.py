from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from database.connection import engine

Base = declarative_base()

class SalesRecord(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False)
    product = Column(String(100), nullable=False)
    category = Column(String(50))
    customer = Column(String(100))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    revenue = Column(Float, nullable=False)
    region = Column(String(50))
    created_at = Column(DateTime, default=func.now())

class InventoryRecord(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product = Column(String(100), nullable=False)
    category = Column(String(50))
    stock_level = Column(Integer, nullable=False)
    reorder_point = Column(Integer)
    unit_cost = Column(Float)
    last_updated = Column(DateTime, default=func.now())

class AgentLog(Base):
    __tablename__ = "agent_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    query = Column(Text, nullable=False)
    response = Column(Text)
    tool_used = Column(String(100))
    created_at = Column(DateTime, default=func.now())

def create_tables():
    Base.metadata.create_all(engine)
    print("✅ Tables created successfully")

if __name__ == "__main__":
    create_tables()