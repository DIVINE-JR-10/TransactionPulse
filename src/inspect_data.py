from pathlib import Path

import pandas as pd


# -------------------------------
# PROJECT PATHS
# -------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw"

# -------------------------------
# LOAD RAW DATA
# -------------------------------

customers = pd.read_csv(RAW_DATA_PATH / "customers.csv")
merchants = pd.read_csv(RAW_DATA_PATH / "merchants.csv")
transactions = pd.read_csv(RAW_DATA_PATH / "transactions.csv")

# -------------------------------
# BASIC DATA INSPECTION
# -------------------------------

print("\n--- CUSTOMERS ---")
print(f"Rows: {len(customers)}")
print(f"Columns: {list(customers.columns)}")
print(customers.head())

print("\n--- MERCHANTS ---")
print(f"Rows: {len(merchants)}")
print(f"Columns: {list(merchants.columns)}")
print(merchants.head())

print("\n--- TRANSACTIONS ---")
print(f"Rows: {len(transactions)}")
print(f"Columns: {list(transactions.columns)}")
print(transactions.head())

# -------------------------------
# REFERENTIAL INTEGRITY CHECK
# -------------------------------

customer_ids = set(customers["customer_id"])
merchant_ids = set(merchants["merchant_id"])

invalid_customer_references = transactions[
    ~transactions["customer_id"].isin(customer_ids)
]

invalid_merchant_references = transactions[
    ~transactions["merchant_id"].isin(merchant_ids)
]

print("\n--- REFERENTIAL INTEGRITY CHECK ---")
print(
    f"Invalid customer references: "
    f"{len(invalid_customer_references)}"
)
print(
    f"Invalid merchant references: "
    f"{len(invalid_merchant_references)}"
)