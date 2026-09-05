from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw"
DIRTY_DATA_PATH = PROJECT_ROOT / "data" / "raw_dirty"

customers = pd.read_csv(RAW_DATA_PATH / "customers.csv")
merchants = pd.read_csv(RAW_DATA_PATH / "merchants.csv")
transactions = pd.read_csv(RAW_DATA_PATH / "transactions.csv")

print("Loaded clean data.")
print(f"Customers: {len(customers)}, Merchants: {len(merchants)}, Transactions: {len(transactions)}")

customers_dirty = customers.copy()

null_city_rows = customers_dirty.sample(5, random_state=1).index
customers_dirty.loc[null_city_rows, "city"] = None

print("\nInjected 5 blank city values.")
print("Null city count now:", customers_dirty["city"].isnull().sum())

duplicate_rows = customers_dirty.sample(4, random_state=2)
customers_dirty = pd.concat([customers_dirty, duplicate_rows], ignore_index=True)

print("\nInjected 4 duplicate rows.")
print("Total customers now:", len(customers_dirty))
print("Duplicate customer_id count:", customers_dirty["customer_id"].duplicated().sum())

bad_type_rows = customers_dirty.sample(3, random_state=3).index
customers_dirty.loc[bad_type_rows, "customer_type"] = "UNKNOWN_TYPE"

print("\nInjected 3 invalid customer_type values.")
print(customers_dirty["customer_type"].unique())

bad_date_rows = customers_dirty.sample(3, random_state=4).index
customers_dirty.loc[bad_date_rows, "created_at"] = "31-13-2025"

print("\nInjected 3 broken dates.")
print(customers_dirty.loc[bad_date_rows, "created_at"])

merchants_dirty = merchants.copy()

null_category_rows = merchants_dirty.sample(2, random_state=5).index
merchants_dirty.loc[null_category_rows, "category"] = None

print("\nInjected 2 blank category values.")
print("Null category count:", merchants_dirty["category"].isnull().sum())

dup_merchant = merchants_dirty.sample(1, random_state=6).copy()
dup_merchant["merchant_name"] = dup_merchant["merchant_name"] + " (DUPLICATE)"
merchants_dirty = pd.concat([merchants_dirty, dup_merchant], ignore_index=True)

print("\nInjected 1 duplicate merchant_id with conflicting name.")
print("Duplicate merchant_id count:", merchants_dirty["merchant_id"].duplicated().sum())

transactions_dirty = transactions.copy()

null_amount_rows = transactions_dirty.sample(10, random_state=7).index
transactions_dirty.loc[null_amount_rows, "amount"] = None

null_payment_rows = transactions_dirty.sample(10, random_state=8).index
transactions_dirty.loc[null_payment_rows, "payment_method"] = None

print("\nInjected 10 blank amounts and 10 blank payment methods.")
print("Null amount count:", transactions_dirty["amount"].isnull().sum())
print("Null payment_method count:", transactions_dirty["payment_method"].isnull().sum())

dup_transactions = transactions_dirty.sample(6, random_state=9)
transactions_dirty = pd.concat([transactions_dirty, dup_transactions], ignore_index=True)

print("\nInjected 6 duplicate transaction rows.")
print("Total transactions now:", len(transactions_dirty))
print("Duplicate transaction_id count:", transactions_dirty["transaction_id"].duplicated().sum())

negative_rows = transactions_dirty.sample(7, random_state=10).index
transactions_dirty.loc[negative_rows, "amount"] = -transactions_dirty.loc[negative_rows, "amount"]

print("\nInjected 7 negative amounts.")
print("Negative amount count:", (transactions_dirty["amount"] < 0).sum())

bad_status_rows = transactions_dirty.sample(4, random_state=11).index
transactions_dirty.loc[bad_status_rows, "status"] = "UNKNOWN"

print("\nInjected 4 invalid status values.")
print(transactions_dirty["status"].unique())

bad_customer_rows = transactions_dirty.sample(5, random_state=12).index
transactions_dirty.loc[bad_customer_rows, "customer_id"] = "C9999"

bad_merchant_rows = transactions_dirty.sample(5, random_state=13).index
transactions_dirty.loc[bad_merchant_rows, "merchant_id"] = "M9999"

print("\nInjected 5 invalid customer_id and 5 invalid merchant_id references.")

bad_timestamp_rows = transactions_dirty.sample(5, random_state=14).index
transactions_dirty.loc[bad_timestamp_rows, "timestamp"] = "not_a_date"

print("\nInjected 5 broken timestamps.")

DIRTY_DATA_PATH.mkdir(parents=True, exist_ok=True)

customers_dirty.to_csv(DIRTY_DATA_PATH / "customers.csv", index=False)
merchants_dirty.to_csv(DIRTY_DATA_PATH / "merchants.csv", index=False)
transactions_dirty.to_csv(DIRTY_DATA_PATH / "transactions.csv", index=False)

print("\nDirty data saved to:", DIRTY_DATA_PATH)
print(f"Customers: {len(customers_dirty)}, Merchants: {len(merchants_dirty)}, Transactions: {len(transactions_dirty)}")