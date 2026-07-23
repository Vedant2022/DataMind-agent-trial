import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st
import pandas as pd
from sqlalchemy import text
from database.connection import engine

def show():
    st.title("📊 DataMind — Business Intelligence Dashboard")
    st.markdown("*Live insights from your business data*")
    st.divider()

    def get_kpis():
        with engine.connect() as conn:
            total_revenue = conn.execute(text("SELECT ROUND(SUM(revenue)::numeric,2) FROM sales")).scalar()
            total_orders = conn.execute(text("SELECT COUNT(*) FROM sales")).scalar()
            top_region = conn.execute(text("""
                SELECT region FROM sales 
                GROUP BY region 
                ORDER BY SUM(revenue) DESC 
                LIMIT 1
            """)).scalar()
            low_stock = conn.execute(text("""
                SELECT COUNT(*) FROM inventory 
                WHERE stock_level <= reorder_point
            """)).scalar()
        return total_revenue, total_orders, top_region, low_stock

    def get_revenue_by_region():
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT region, 
                       ROUND(SUM(revenue)::numeric,2) as total_revenue,
                       COUNT(*) as total_orders
                FROM sales
                GROUP BY region
                ORDER BY total_revenue DESC
            """))
            return pd.DataFrame(result.fetchall(), columns=result.keys())

    def get_top_products():
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT product, category,
                       COUNT(*) as times_sold,
                       ROUND(SUM(revenue)::numeric,2) as total_revenue
                FROM sales
                GROUP BY product, category
                ORDER BY total_revenue DESC
                LIMIT 5
            """))
            return pd.DataFrame(result.fetchall(), columns=result.keys())

    def get_inventory_alerts():
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT product, stock_level, reorder_point,
                       (reorder_point - stock_level) as units_needed
                FROM inventory
                WHERE stock_level <= reorder_point
                ORDER BY units_needed DESC
            """))
            return pd.DataFrame(result.fetchall(), columns=result.keys())

    def get_monthly_revenue():
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT to_char(date, 'YYYY-MM') as month,
                       ROUND(SUM(revenue)::numeric,2) as revenue
                FROM sales
                GROUP BY month
                ORDER BY month
            """))
            return pd.DataFrame(result.fetchall(), columns=result.keys())

    total_revenue, total_orders, top_region, low_stock = get_kpis()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Revenue", f"£{total_revenue:,.2f}")
    with col2:
        st.metric("Total Orders", f"{total_orders:,}")
    with col3:
        st.metric("Top Region", top_region)
    with col4:
        st.metric("Low Stock Alerts", low_stock, delta=f"{low_stock} items need restock", delta_color="inverse")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Revenue by Region")
        region_df = get_revenue_by_region()
        st.bar_chart(region_df.set_index("region")["total_revenue"])

    with col2:
        st.subheader("Monthly Revenue Trend")
        monthly_df = get_monthly_revenue()
        st.line_chart(monthly_df.set_index("month")["revenue"])

    st.divider()

    st.subheader("Top 5 Products by Revenue")
    products_df = get_top_products()
    st.dataframe(products_df, use_container_width=True, hide_index=True)

    st.divider()

    st.subheader("🔴 Inventory Alerts")
    alerts_df = get_inventory_alerts()
    if len(alerts_df) > 0:
        st.dataframe(alerts_df, use_container_width=True, hide_index=True)
    else:
        st.success("All inventory levels are healthy")
