import sqlite3
from pathlib import Path

import pandas as pd

DATA_DIR = Path("data")
DB_PATH = Path("ecommerce.db")


def load_csv(name: str) -> pd.DataFrame:
    path = DATA_DIR / f"{name}.csv"
    if not path.exists():
        raise FileNotFoundError(f"Expected CSV at {path}")
    return pd.read_csv(path)


def main():
    if not DATA_DIR.exists():
        raise FileNotFoundError("Data directory not found. Generate CSVs first.")

    customers_df = load_csv("customers")
    products_df = load_csv("products")
    orders_df = load_csv("orders")
    order_items_df = load_csv("order_items")
    reviews_df = load_csv("reviews")

    with sqlite3.connect(DB_PATH) as conn:
        customers_df.to_sql("customers", conn, if_exists="replace", index=False)
        products_df.to_sql("products", conn, if_exists="replace", index=False)
        orders_df.to_sql("orders", conn, if_exists="replace", index=False)
        order_items_df.to_sql("order_items", conn, if_exists="replace", index=False)
        reviews_df.to_sql("reviews", conn, if_exists="replace", index=False)

        tables = {
            "customers": customers_df,
            "products": products_df,
            "orders": orders_df,
            "order_items": order_items_df,
            "reviews": reviews_df,
        }
        for table in tables:
            count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"{table}: {count} rows")


if __name__ == "__main__":
    main()


