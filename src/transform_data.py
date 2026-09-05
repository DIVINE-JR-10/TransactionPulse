from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEAN_DATA_PATH = PROJECT_ROOT / "data" / "clean"
OUTPUT_PATH = PROJECT_ROOT / "data" / "transformed"

customers = pd.read_csv(CLEAN_DATA_PATH / "customers.csv")
merchants = pd.read_csv(CLEAN_DATA_PATH / "merchants.csv")
transactions = pd.read_csv(CLEAN_DATA_PATH / "transactions.csv")

print("Loaded clean data.")
print(f"Customers: {len(customers)}, Merchants: {len(merchants)}, Transactions: {len(transactions)}")

transactions_full = transactions.merge(
    customers[["customer_id", "customer_name", "city", "customer_type"]],
    on="customer_id",
    how="left"
)

transactions_full = transactions_full.merge(
    merchants[["merchant_id", "merchant_name", "category"]],
    on="merchant_id",
    how="left"
)

print("\nJoined transactions with customer and merchant info.")
print("Columns now:", list(transactions_full.columns))
print("Total rows:", len(transactions_full))

missing_customer_info = transactions_full["customer_name"].isnull().sum()
missing_merchant_info = transactions_full["merchant_name"].isnull().sum()

print(f"\nRows missing customer info after join: {missing_customer_info}")
print(f"Rows missing merchant info after join: {missing_merchant_info}")

customer_summary = transactions_full.groupby("customer_id").agg(
    total_transactions=("transaction_id", "count"),
    total_spent=("amount", "sum"),
    avg_transaction_amount=("amount", "mean")
).reset_index()

customer_summary = customer_summary.merge(
    customers[["customer_id", "customer_name", "city", "customer_type"]],
    on="customer_id",
    how="left"
)

print("\nCustomer summary built.")
print(customer_summary.head())

merchant_summary = transactions_full.groupby("merchant_id").agg(
    total_transactions=("transaction_id", "count"),
    total_revenue=("amount", "sum"),
    avg_transaction_amount=("amount", "mean")
).reset_index()

merchant_summary = merchant_summary.merge(
    merchants[["merchant_id", "merchant_name", "category"]],
    on="merchant_id",
    how="left"
)

print("\nMerchant summary built.")
print(merchant_summary.head())

status_counts = transactions_full.groupby(["customer_id", "status"]).size().unstack(fill_value=0)

customer_summary = customer_summary.merge(status_counts, on="customer_id", how="left")

if "SUCCESS" in customer_summary.columns:
    customer_summary["success_rate"] = (
        customer_summary["SUCCESS"] / customer_summary["total_transactions"]
    ).round(3)

print("\nAdded success rate to customer summary.")
print(customer_summary[["customer_id", "total_transactions", "SUCCESS", "FAILED", "PENDING", "success_rate"]].head())

OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

transactions_full.to_csv(OUTPUT_PATH / "transactions_full.csv", index=False)
customer_summary.to_csv(OUTPUT_PATH / "customer_summary.csv", index=False)
merchant_summary.to_csv(OUTPUT_PATH / "merchant_summary.csv", index=False)

print("\n--- SAVED ---")
print(f"transactions_full: {len(transactions_full)} rows")
print(f"customer_summary: {len(customer_summary)} rows")
print(f"merchant_summary: {len(merchant_summary)} rows")
print(f"\nSaved to: {OUTPUT_PATH}")