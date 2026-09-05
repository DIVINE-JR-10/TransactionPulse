from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "clean"

customers = pd.read_csv(DATA_PATH / "customers.csv")
merchants = pd.read_csv(DATA_PATH / "merchants.csv")
transactions = pd.read_csv(DATA_PATH / "transactions.csv")

print("Data loaded successfully!")
print(f"Customers: {len(customers)} rows")
print(f"Merchants: {len(merchants)} rows")
print(f"Transactions: {len(transactions)} rows")

print("\n--- NULL CHECK: CUSTOMERS ---")
print(customers.isnull().sum())

print("\n--- NULL CHECK: MERCHANTS ---")
print(merchants.isnull().sum())

print("\n--- NULL CHECK: TRANSACTIONS ---")
print(transactions.isnull().sum())

print("\n--- DUPLICATE CHECK: CUSTOMERS ---")
print("Duplicate customer_id count:", customers["customer_id"].duplicated().sum())

print("\n--- DUPLICATE CHECK: MERCHANTS ---")
print("Duplicate merchant_id count:", merchants["merchant_id"].duplicated().sum())

print("\n--- DUPLICATE CHECK: TRANSACTIONS ---")
print("Duplicate transaction_id count:", transactions["transaction_id"].duplicated().sum())

print("\n--- INVALID VALUE CHECK: TRANSACTIONS ---")
negative_amounts = transactions[transactions["amount"] < 0]
print("Negative amount count:", len(negative_amounts))

print("\nUnique status values:", transactions["status"].unique())
print("Unique payment_method values:", transactions["payment_method"].unique())

valid_statuses = {"SUCCESS", "FAILED", "PENDING"}
valid_payment_methods = {"CARD", "WALLET", "UPI", "NET_BANKING"}

invalid_status = transactions[~transactions["status"].isin(valid_statuses)]
invalid_payment = transactions[~transactions["payment_method"].isin(valid_payment_methods)]

print("\nInvalid status count:", len(invalid_status))
print("Invalid payment_method count:", len(invalid_payment))

print("\n--- DATE VALIDATION: TRANSACTIONS ---")
parsed_dates = pd.to_datetime(transactions["timestamp"], errors="coerce")
unparseable = transactions[parsed_dates.isna()]
print("Unparseable timestamp count:", len(unparseable))

print("\n--- DATA TYPE VALIDATION: TRANSACTIONS ---")
non_numeric_amount = transactions[pd.to_numeric(transactions["amount"], errors="coerce").isna()]
print("Non-numeric amount count:", len(non_numeric_amount))