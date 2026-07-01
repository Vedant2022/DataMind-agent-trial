import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from anthropic import Anthropic
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.orm import Session
from database.connection import engine
from database.schema import AgentLog

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """
You are DataMind, an autonomous business intelligence agent.
You have access to a business database with sales and inventory data.
When asked a question, analyse the data and give clear, concise insights.
Always back your answers with numbers from the data provided.
Be direct and actionable — you are talking to business stakeholders.
"""

def log_interaction(query, response, tool_used=None):
    with Session(engine) as session:
        log = AgentLog(query=query, response=response, tool_used=tool_used)
        session.add(log)
        session.commit()

def query_database(sql):
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        rows = result.fetchall()
        columns = result.keys()
        return [dict(zip(columns, row)) for row in rows]

def get_sales_summary():
    return query_database("""
        SELECT 
            region,
            COUNT(*) as total_orders,
            ROUND(SUM(revenue), 2) as total_revenue,
            ROUND(AVG(revenue), 2) as avg_order_value
        FROM sales
        GROUP BY region
        ORDER BY total_revenue DESC
    """)

def get_top_products():
    return query_database("""
        SELECT 
            product,
            category,
            COUNT(*) as times_sold,
            ROUND(SUM(revenue), 2) as total_revenue
        FROM sales
        GROUP BY product
        ORDER BY total_revenue DESC
        LIMIT 5
    """)

def get_inventory_alerts():
    return query_database("""
        SELECT product, stock_level, reorder_point
        FROM inventory
        WHERE stock_level <= reorder_point
    """)

def ask_agent(user_query):
    sales_summary = get_sales_summary()
    top_products = get_top_products()
    inventory_alerts = get_inventory_alerts()

    context = f"""
Current business data:

SALES BY REGION:
{sales_summary}

TOP 5 PRODUCTS BY REVENUE:
{top_products}

INVENTORY ALERTS (low stock):
{inventory_alerts}

User question: {user_query}
"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": context}]
    )

    answer = response.content[0].text
    log_interaction(user_query, answer, tool_used="claude-sonnet-4-6")
    return answer

if __name__ == "__main__":
    print("🤖 DataMind Agent ready\n")
    question = input("Ask your question: ")
    # question = "Which region is performing best and which products should we restock?"
    print(f"Question: {question}\n")
    print("Answer:")
    print(ask_agent(question))