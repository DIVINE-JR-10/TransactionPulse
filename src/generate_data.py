import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from faker import Faker


# -------------------------------
# CONFIGURATION
# -------------------------------

NUM_CUSTOMERS = 500
NUM_MERCHANTS = 50
NUM_TRANSACTIONS = 10_000


# -------------------------------
# PROJECT PATHS
# -------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw"


# -------------------------------
# FAKE DATA SETUP
# -------------------------------

fake = Faker("en_IN")

# -------------------------------
# GENERATE CUSTOMERS
# -------------------------------

def generate_customers():
    customers = []

    customer_types = ["Regular", "Premium"]

    for i in range(1, NUM_CUSTOMERS + 1):

        customer = {
            "customer_id": f"C{i:04d}",
            "customer_name": fake.name(),
            "city": fake.city(),
            "customer_type": random.choice(customer_types),
            "created_at": fake.date_between(
                start_date="-2y",
                end_date="today"
            )
        }

        customers.append(customer)

    return pd.DataFrame(customers)

# -------------------------------
# GENERATE MERCHANTS
# -------------------------------

def generate_merchants():
    merchants = []

    merchant_types = {
        "QuickCart": "E-commerce",
        "FoodExpress": "Food & Dining",
        "MediCare": "Healthcare",
        "TechMart": "Electronics",
        "FunZone": "Entertainment",
        "TravelEase": "Travel"
    }

    merchant_names = list(merchant_types.keys())

    for i in range(1, NUM_MERCHANTS + 1):

        merchant_name = random.choice(merchant_names)

        merchant = {
            "merchant_id": f"M{i:04d}",
            "merchant_name": f"{merchant_name} {i}",
            "category": merchant_types[merchant_name],
            "city": fake.city(),
            "created_at": fake.date_between(
                start_date="-3y",
                end_date="today"
            )
        }

        merchants.append(merchant)

    return pd.DataFrame(merchants)

# -------------------------------
# GENERATE TRANSACTIONS
# -------------------------------

def generate_transactions(customers, merchants):
    transactions = []

    customer_ids = customers["customer_id"].tolist()
    merchant_ids = merchants["merchant_id"].tolist()

    payment_methods = ["UPI", "CARD", "NET_BANKING", "WALLET"]
    statuses = ["SUCCESS", "FAILED", "PENDING"]

    for i in range(1, NUM_TRANSACTIONS + 1):

        transaction = {
            "transaction_id": f"T{i:06d}",
            "customer_id": random.choice(customer_ids),
            "merchant_id": random.choice(merchant_ids),
            "amount": round(random.uniform(50, 50000), 2),
            "payment_method": random.choice(payment_methods),
            "status": random.choices(
                statuses,
                weights=[85, 10, 5],
                k=1
            )[0],
            "timestamp": fake.date_time_between(
                start_date="-90d",
                end_date="now"
            )
        }

        transactions.append(transaction)

    return pd.DataFrame(transactions)

# -------------------------------
# MAIN
# -------------------------------

def main():
    # Create the raw data folder if it doesn't exist
    RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)

    # Generate datasets
    print("Generating customers...")
    customers = generate_customers()

    print("Generating merchants...")
    merchants = generate_merchants()

    print("Generating transactions...")
    transactions = generate_transactions(customers, merchants)

    # Save datasets
    customers.to_csv(
        RAW_DATA_PATH / "customers.csv",
        index=False
    )

    merchants.to_csv(
        RAW_DATA_PATH / "merchants.csv",
        index=False
    )

    transactions.to_csv(
        RAW_DATA_PATH / "transactions.csv",
        index=False
    )

    print("\nData generation completed successfully!")
    print(f"Customers generated: {len(customers)}")
    print(f"Merchants generated: {len(merchants)}")
    print(f"Transactions generated: {len(transactions)}")


if __name__ == "__main__":
    main()