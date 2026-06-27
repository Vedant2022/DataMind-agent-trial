import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import engine
from database.schema import SalesRecord, InventoryRecord, Base
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random

products = [
    ("Laptop Pro", "Electronics", 999.99),
    ("Wireless Mouse", "Accessories", 29.99),
    ("USB Hub", "Accessories", 49.99),
    ("Monitor 27inch", "Electronics", 349.99),
    ("Mechanical Keyboard", "Accessories", 89.99),
    ("Webcam HD", "Electronics", 79.99),
    ("Desk Lamp", "Office", 39.99),
    ("Notebook Pack", "Stationery", 12.99),
]

customers = ["Acme Corp", "TechStart Ltd", "Green Solutions", "BrightMind Co", "NextWave Inc"]
regions = ["North", "South", "East", "West", "Central"]

def seed_sales(session, n=200):
    records = []
    for _ in range(n):
        product, category, price = random.choice(products)
        quantity = random.randint(1, 20)
        date = datetime.now() - timedelta(days=random.randint(0, 365))
        records.append(SalesRecord(
            date=date,
            product=product,
            category=category,
            customer=random.choice(customers),
            quantity=quantity,
            unit_price=price,
            revenue=round(quantity * price, 2),
            region=random.choice(regions)
        ))
    session.add_all(records)
    print(f"✅ {n} sales records seeded")

def seed_inventory(session):
    records = []
    for product, category, cost in products:
        records.append(InventoryRecord(
            product=product,
            category=category,
            stock_level=random.randint(10, 200),
            reorder_point=20,
            unit_cost=cost * 0.6
        ))
    session.add_all(records)
    print(f"✅ {len(products)} inventory records seeded")

if __name__ == "__main__":
    with Session(engine) as session:
        seed_sales(session)
        seed_inventory(session)
        session.commit()
        print("✅ Database seeded successfully")