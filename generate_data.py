import random
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd


random.seed(42)
np.random.seed(42)

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

NUM_CUSTOMERS = 500
NUM_PRODUCTS = 200
NUM_ORDERS = 1000
NUM_ORDER_ITEMS = 2000
NUM_REVIEWS = 300


def random_date(start: datetime, end: datetime) -> datetime:
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))


def build_customers():
    first_names = [
        "Alex",
        "Jordan",
        "Taylor",
        "Casey",
        "Morgan",
        "Riley",
        "Jamie",
        "Robin",
        "Avery",
        "Cameron",
    ]
    last_names = [
        "Smith",
        "Johnson",
        "Williams",
        "Brown",
        "Jones",
        "Miller",
        "Davis",
        "Garcia",
        "Rodriguez",
        "Martinez",
    ]
    genders = ["Female", "Male", "Non-binary", "Prefer not to say"]
    locations = [
        "New York",
        "Los Angeles",
        "Chicago",
        "Houston",
        "Phoenix",
        "Seattle",
        "Miami",
        "Denver",
        "Boston",
        "San Francisco",
    ]

    signup_start = datetime(2020, 1, 1)
    signup_end = datetime(2024, 12, 31)

    customers = []
    for cid in range(1, NUM_CUSTOMERS + 1):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        customers.append(
            {
                "customer_id": cid,
                "name": name,
                "age": random.randint(18, 70),
                "gender": random.choice(genders),
                "location": random.choice(locations),
                "signup_date": random_date(signup_start, signup_end).date(),
            }
        )
    return pd.DataFrame(customers)


def build_products():
    categories = [
        "Electronics",
        "Home",
        "Fashion",
        "Beauty",
        "Sports",
        "Outdoors",
        "Toys",
        "Books",
    ]
    brands = [
        "Acme",
        "Northwind",
        "Globex",
        "Innotech",
        "Umbrella",
        "Soylent",
        "Stark",
        "Wayne",
        "Wonka",
    ]

    products = []
    for pid in range(1, NUM_PRODUCTS + 1):
        category = random.choice(categories)
        products.append(
            {
                "product_id": pid,
                "name": f"{category} Item {pid}",
                "category": category,
                "price": round(random.uniform(5, 500), 2),
                "brand": random.choice(brands),
            }
        )
    return pd.DataFrame(products)


def build_orders(customers_df):
    payment_methods = ["Credit Card", "PayPal", "Bank Transfer", "Apple Pay", "Google Pay"]
    order_start = datetime(2021, 1, 1)
    order_end = datetime(2025, 11, 14)

    orders = []
    for oid in range(1, NUM_ORDERS + 1):
        cust = customers_df.sample(1).iloc[0]
        customer_signup = datetime.fromisoformat(str(cust["signup_date"]))
        start_date = max(order_start, customer_signup)
        order_date = random_date(start_date, order_end)
        orders.append(
            {
                "order_id": oid,
                "customer_id": int(cust["customer_id"]),
                "order_date": order_date.date(),
                "total_amount": 0.0,  # placeholder, updated after items built
                "payment_method": random.choice(payment_methods),
            }
        )
    return pd.DataFrame(orders)


def build_order_items(orders_df, products_df):
    order_totals = {oid: 0.0 for oid in orders_df["order_id"]}
    order_items = []

    def create_item(order_id, item_id):
        product = products_df.sample(1).iloc[0]
        quantity = random.randint(1, 5)
        base_price = float(product["price"])
        item_price = round(base_price * random.uniform(0.9, 1.1), 2)
        order_totals[order_id] += quantity * item_price
        return {
            "item_id": item_id,
            "order_id": order_id,
            "product_id": int(product["product_id"]),
            "quantity": quantity,
            "item_price": item_price,
        }

    current_item_id = 1
    # Ensure every order has at least one item
    for order_id in orders_df["order_id"]:
        order_items.append(create_item(int(order_id), current_item_id))
        current_item_id += 1

    # Add remaining items
    remaining = NUM_ORDER_ITEMS - len(order_items)
    order_id_choices = orders_df["order_id"].tolist()
    for _ in range(remaining):
        oid = int(random.choice(order_id_choices))
        order_items.append(create_item(oid, current_item_id))
        current_item_id += 1

    order_items_df = pd.DataFrame(order_items)
    orders_df = orders_df.copy()
    orders_df["total_amount"] = orders_df["order_id"].map(order_totals).round(2)
    return order_items_df, orders_df


def build_reviews(customers_df, products_df):
    review_text_templates = [
        "Loved the quality and fast shipping!",
        "Product met my expectations.",
        "Decent value for the price.",
        "Would definitely recommend to friends.",
        "Not what I expected, but customer service helped.",
        "Five stars! Will buy again.",
        "Solid performance so far.",
        "Packaging could be improved, but product is great.",
        "Exactly as described.",
        "Great deal and excellent brand.",
    ]
    review_start = datetime(2021, 1, 1)
    review_end = datetime(2025, 11, 14)

    reviews = []
    for rid in range(1, NUM_REVIEWS + 1):
        customer = customers_df.sample(1).iloc[0]
        product = products_df.sample(1).iloc[0]
        reviews.append(
            {
                "review_id": rid,
                "customer_id": int(customer["customer_id"]),
                "product_id": int(product["product_id"]),
                "rating": random.randint(1, 5),
                "review_text": random.choice(review_text_templates),
                "review_date": random_date(review_start, review_end).date(),
            }
        )
    return pd.DataFrame(reviews)


def main():
    customers_df = build_customers()
    products_df = build_products()
    orders_df = build_orders(customers_df)
    order_items_df, orders_df = build_order_items(orders_df, products_df)
    reviews_df = build_reviews(customers_df, products_df)

    customers_df.to_csv(DATA_DIR / "customers.csv", index=False)
    products_df.to_csv(DATA_DIR / "products.csv", index=False)
    orders_df.to_csv(DATA_DIR / "orders.csv", index=False)
    order_items_df.to_csv(DATA_DIR / "order_items.csv", index=False)
    reviews_df.to_csv(DATA_DIR / "reviews.csv", index=False)


if __name__ == "__main__":
    main()


