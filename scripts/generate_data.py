import os
import random
from datetime import datetime, timedelta

import numpy as np
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from faker import Faker


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing from .env")

NUM_CUSTOMERS = 10_000
NUM_PRODUCTS = 500
NUM_ORDERS = 100_000

SEED = 42

random.seed(SEED)
np.random.seed(SEED)

fake = Faker()
Faker.seed(SEED)


# ============================================================
# DATABASE
# ============================================================

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


# ============================================================
# DATA DEFINITIONS
# ============================================================

CITIES = [
    "Karachi",
    "Lahore",
    "Islamabad",
    "Rawalpindi",
    "Faisalabad",
    "Multan",
    "Peshawar",
    "Quetta",
]

COUNTRY = "Pakistan"

CATEGORIES = [
    "Electronics",
    "Clothing",
    "Home & Kitchen",
    "Beauty",
    "Sports",
    "Books",
    "Accessories",
    "Grocery",
]

STATUSES = [
    "completed",
    "shipped",
    "processing",
    "cancelled",
]

RETURN_REASONS = [
    "Damaged",
    "Wrong Product",
    "Poor Quality",
    "Not as Expected",
    "Size Issue",
    "Late Delivery",
]


# ============================================================
# HELPERS
# ============================================================

def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)


def generate_product_name(category, index):
    names = {
        "Electronics": [
            "Wireless Headphones",
            "Smart Watch",
            "Bluetooth Speaker",
            "USB-C Charger",
            "Power Bank",
            "Mechanical Keyboard",
            "Wireless Mouse",
            "Webcam",
        ],
        "Clothing": [
            "Premium T-Shirt",
            "Cotton Hoodie",
            "Denim Jacket",
            "Casual Shirt",
            "Sports Trousers",
            "Running Shoes",
        ],
        "Home & Kitchen": [
            "Coffee Maker",
            "Air Fryer",
            "Kitchen Organizer",
            "Water Bottle",
            "LED Lamp",
            "Storage Box",
        ],
        "Beauty": [
            "Face Wash",
            "Moisturizer",
            "Hair Serum",
            "Perfume",
            "Skin Care Kit",
        ],
        "Sports": [
            "Yoga Mat",
            "Running Gloves",
            "Football",
            "Fitness Band",
            "Gym Bag",
        ],
        "Books": [
            "Python Programming",
            "Machine Learning Guide",
            "Business Strategy",
            "Data Science Handbook",
            "AI Engineering",
        ],
        "Accessories": [
            "Phone Case",
            "Laptop Sleeve",
            "Wallet",
            "Backpack",
            "Sunglasses",
        ],
        "Grocery": [
            "Organic Coffee",
            "Green Tea",
            "Protein Snacks",
            "Breakfast Cereal",
            "Cooking Oil",
        ],
    }

    base_name = random.choice(names[category])
    return f"{base_name} {index}"


# ============================================================
# GENERATE CUSTOMERS
# ============================================================

def generate_customers():
    print("Generating customers...")

    customers = []

    start_date = datetime(2023, 1, 1).date()
    end_date = datetime(2025, 12, 31).date()

    for _ in range(NUM_CUSTOMERS):

        first_name = fake.first_name()
        last_name = fake.last_name()

        email = (
            f"{first_name.lower()}."
            f"{last_name.lower()}."
            f"{random.randint(1000, 999999)}"
            "@example.com"
        )

        customers.append(
            {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "city": random.choice(CITIES),
                "country": COUNTRY,
                "signup_date": random_date(start_date, end_date),
            }
        )

    return customers


# ============================================================
# GENERATE PRODUCTS
# ============================================================

def generate_products():
    print("Generating products...")

    products = []

    for i in range(1, NUM_PRODUCTS + 1):

        category = random.choice(CATEGORIES)

        cost_price = round(
            random.uniform(5, 500),
            2,
        )

        margin = random.uniform(1.15, 2.5)

        selling_price = round(
            cost_price * margin,
            2,
        )

        products.append(
            {
                "product_name": generate_product_name(category, i),
                "category": category,
                "selling_price": selling_price,
                "cost_price": cost_price,
            }
        )

    return products


# ============================================================
# INSERT CUSTOMERS
# ============================================================

def insert_customers(customers):

    print("Inserting customers...")

    query = text(
        """
        INSERT INTO customers
        (
            first_name,
            last_name,
            email,
            city,
            country,
            signup_date
        )
        VALUES
        (
            :first_name,
            :last_name,
            :email,
            :city,
            :country,
            :signup_date
        )
        """
    )

    with engine.begin() as connection:

        connection.execute(
            query,
            customers,
        )


# ============================================================
# INSERT PRODUCTS
# ============================================================

def insert_products(products):

    print("Inserting products...")

    query = text(
        """
        INSERT INTO products
        (
            product_name,
            category,
            selling_price,
            cost_price
        )
        VALUES
        (
            :product_name,
            :category,
            :selling_price,
            :cost_price
        )
        """
    )

    with engine.begin() as connection:

        connection.execute(
            query,
            products,
        )


# ============================================================
# GENERATE ORDERS
# ============================================================

def generate_orders():

    print("Generating orders...")

    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 12, 31)

    orders = []

    for _ in range(NUM_ORDERS):

        customer_id = random.randint(
            1,
            NUM_CUSTOMERS,
        )

        order_date = random_date(
            start_date,
            end_date,
        )

        status = random.choices(
            STATUSES,
            weights=[
                70,
                15,
                10,
                5,
            ],
        )[0]

        shipping_city = random.choice(
            CITIES
        )

        total_amount = round(
            random.uniform(20, 1500),
            2,
        )

        shipping_cost = round(
            random.uniform(2, 25),
            2,
        )

        orders.append(
            {
                "customer_id": customer_id,
                "order_date": order_date,
                "status": status,
                "shipping_city": shipping_city,
                "total_amount": total_amount,
                "shipping_cost": shipping_cost,
            }
        )

    return orders


# ============================================================
# INSERT ORDERS
# ============================================================

def insert_orders(orders):

    print("Inserting orders...")

    query = text(
        """
        INSERT INTO orders
        (
            customer_id,
            order_date,
            status,
            shipping_city,
            total_amount,
            shipping_cost
        )
        VALUES
        (
            :customer_id,
            :order_date,
            :status,
            :shipping_city,
            :total_amount,
            :shipping_cost
        )
        """
    )

    with engine.begin() as connection:

        connection.execute(
            query,
            orders,
        )


# ============================================================
# GENERATE ORDER ITEMS
# ============================================================

def generate_order_items():

    print("Generating order items...")

    items = []

    for order_id in range(1, NUM_ORDERS + 1):

        number_of_items = random.randint(1, 4)

        product_ids = random.sample(
            range(1, NUM_PRODUCTS + 1),
            number_of_items,
        )

        for product_id in product_ids:

            quantity = random.randint(1, 4)

            items.append(
                {
                    "order_id": order_id,
                    "product_id": product_id,
                    "quantity": quantity,
                    "unit_price": round(
                        random.uniform(10, 500),
                        2,
                    ),
                    "unit_cost": round(
                        random.uniform(5, 300),
                        2,
                    ),
                }
            )

    return items


# ============================================================
# INSERT ORDER ITEMS
# ============================================================

def insert_order_items(items):

    print(
        f"Inserting {len(items):,} order items..."
    )

    query = text(
        """
        INSERT INTO order_items
        (
            order_id,
            product_id,
            quantity,
            unit_price,
            unit_cost
        )
        VALUES
        (
            :order_id,
            :product_id,
            :quantity,
            :unit_price,
            :unit_cost
        )
        """
    )

    with engine.begin() as connection:

        batch_size = 10_000

        for i in range(
            0,
            len(items),
            batch_size,
        ):

            batch = items[
                i:i + batch_size
            ]

            connection.execute(
                query,
                batch,
            )

            print(
                f"Inserted {min(i + batch_size, len(items)):,}"
                f"/{len(items):,}"
            )


# ============================================================
# GENERATE INVENTORY
# ============================================================

def generate_inventory():

    print("Generating inventory...")

    inventory = []

    for product_id in range(
        1,
        NUM_PRODUCTS + 1,
    ):

        inventory.append(
            {
                "product_id": product_id,
                "current_stock": random.randint(
                    0,
                    500,
                ),
                "reorder_level": random.randint(
                    10,
                    100,
                ),
                "last_restock_date": datetime(
                    2025,
                    random.randint(1, 12),
                    random.randint(1, 28),
                ).date(),
            }
        )

    return inventory


# ============================================================
# INSERT INVENTORY
# ============================================================

def insert_inventory(inventory):

    print("Inserting inventory...")

    query = text(
        """
        INSERT INTO inventory
        (
            product_id,
            current_stock,
            reorder_level,
            last_restock_date
        )
        VALUES
        (
            :product_id,
            :current_stock,
            :reorder_level,
            :last_restock_date
        )
        """
    )

    with engine.begin() as connection:

        connection.execute(
            query,
            inventory,
        )


# ============================================================
# GENERATE RETURNS
# ============================================================

def generate_returns():

    print("Generating returns...")

    returns = []

    number_of_returns = 10_000

    for _ in range(
        number_of_returns
    ):

        order_id = random.randint(
            1,
            NUM_ORDERS,
        )

        product_id = random.randint(
            1,
            NUM_PRODUCTS,
        )

        customer_id = random.randint(
            1,
            NUM_CUSTOMERS,
        )

        return_date = datetime(
            2025,
            random.randint(1, 12),
            random.randint(1, 28),
        ).date()

        returns.append(
            {
                "order_id": order_id,
                "product_id": product_id,
                "customer_id": customer_id,
                "return_date": return_date,
                "quantity": random.randint(1, 3),
                "reason": random.choice(
                    RETURN_REASONS
                ),
                "refund_amount": round(
                    random.uniform(10, 500),
                    2,
                ),
            }
        )

    return returns


# ============================================================
# INSERT RETURNS
# ============================================================

def insert_returns(returns):

    print("Inserting returns...")

    query = text(
        """
        INSERT INTO returns
        (
            order_id,
            product_id,
            customer_id,
            return_date,
            quantity,
            reason,
            refund_amount
        )
        VALUES
        (
            :order_id,
            :product_id,
            :customer_id,
            :return_date,
            :quantity,
            :reason,
            :refund_amount
        )
        """
    )

    with engine.begin() as connection:

        connection.execute(
            query,
            returns,
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("OPSPILOT AI - DATA GENERATOR")
    print("=" * 60)

    customers = generate_customers()
    insert_customers(customers)

    products = generate_products()
    insert_products(products)

    orders = generate_orders()
    insert_orders(orders)

    order_items = generate_order_items()
    insert_order_items(order_items)

    inventory = generate_inventory()
    insert_inventory(inventory)

    returns = generate_returns()
    insert_returns(returns)

    print("=" * 60)
    print("DATA GENERATION COMPLETE")
    print("=" * 60)

    print(
        f"Customers: {len(customers):,}"
    )

    print(
        f"Products: {len(products):,}"
    )

    print(
        f"Orders: {len(orders):,}"
    )

    print(
        f"Order Items: {len(order_items):,}"
    )

    print(
        f"Inventory: {len(inventory):,}"
    )

    print(
        f"Returns: {len(returns):,}"
    )


if __name__ == "__main__":
    main()