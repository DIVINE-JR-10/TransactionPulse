from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_PATH = PROJECT_ROOT / "data" / "raw_dirty"
OUTPUT_PATH = PROJECT_ROOT / "data" / "clean"

customers = pd.read_csv(INPUT_PATH / "customers.csv")
merchants = pd.read_csv(INPUT_PATH / "merchants.csv")
transactions = pd.read_csv(INPUT_PATH / "transactions.csv")

print("Loaded dirty data.")
print(f"Customers: {len(customers)}, Merchants: {len(merchants)}, Transactions: {len(transactions)}")

customers_clean = customers.copy()

before = len(customers_clean)
customers_clean = customers_clean.drop_duplicates()
after = len(customers_clean)

print(f"\nDropped {before - after} duplicate customer rows.")
print("Total customers now:", len(customers_clean))

null_city_count = customers_clean["city"].isnull().sum()
customers_clean["city"] = customers_clean["city"].fillna("Unknown")

null_name_count = customers_clean["customer_name"].isnull().sum()
customers_clean["customer_name"] = customers_clean["customer_name"].fillna("Unknown")

print(f"\nFilled {null_city_count} blank city values with 'Unknown'.")
print(f"Filled {null_name_count} blank customer_name values with 'Unknown'.")
print("Remaining nulls in city:", customers_clean["city"].isnull().sum())

valid_types = {"Regular", "Premium"}

before = len(customers_clean)
customers_clean = customers_clean[customers_clean["customer_type"].isin(valid_types)]
after = len(customers_clean)
print(f"\nDropped {before - after} rows with invalid customer_type.")

before = len(customers_clean)
parsed_dates = pd.to_datetime(customers_clean["created_at"], errors="coerce")
customers_clean = customers_clean[parsed_dates.notna()]
after = len(customers_clean)
print(f"Dropped {before - after} rows with unparseable created_at.")

print("Final customers count:", len(customers_clean))

merchants_clean = merchants.copy()

before = len(merchants_clean)
merchants_clean = merchants_clean.drop_duplicates(subset=["merchant_id"], keep="first")
after = len(merchants_clean)

print(f"\nDropped {before - after} duplicate merchant_id rows.")
print("Total merchants now:", len(merchants_clean))

null_category_count = merchants_clean["category"].isnull().sum()
merchants_clean["category"] = merchants_clean["category"].fillna("Unknown")

print(f"\nFilled {null_category_count} blank category values with 'Unknown'.")
print("Final merchants count:", len(merchants_clean))

transactions_clean = transactions.copy()

before = len(transactions_clean)
transactions_clean = transactions_clean.drop_duplicates()
after = len(transactions_clean)
print(f"\nDropped {before - after} duplicate transaction rows.")

before = len(transactions_clean)
transactions_clean = transactions_clean[transactions_clean["amount"].notna()]
after = len(transactions_clean)
print(f"Dropped {before - after} rows with missing amount.")

print("Transactions count so far:", len(transactions_clean))

null_payment_count = transactions_clean["payment_method"].isnull().sum()
transactions_clean["payment_method"] = transactions_clean["payment_method"].fillna("UNKNOWN")
print(f"\nFilled {null_payment_count} blank payment_method values with 'UNKNOWN'.")

valid_statuses = {"SUCCESS", "FAILED", "PENDING"}
before = len(transactions_clean)
transactions_clean = transactions_clean[transactions_clean["status"].isin(valid_statuses)]
after = len(transactions_clean)
print(f"Dropped {before - after} rows with invalid status.")

print("Transactions count so far:", len(transactions_clean))

customer_ids = set(customers_clean["customer_id"])
merchant_ids = set(merchants_clean["merchant_id"])

before = len(transactions_clean)
transactions_clean = transactions_clean[transactions_clean["customer_id"].isin(customer_ids)]
after = len(transactions_clean)
print(f"\nDropped {before - after} rows with invalid customer_id reference.")

before = len(transactions_clean)
transactions_clean = transactions_clean[transactions_clean["merchant_id"].isin(merchant_ids)]
after = len(transactions_clean)
print(f"Dropped {before - after} rows with invalid merchant_id reference.")

print("Transactions count so far:", len(transactions_clean))

before = len(transactions_clean)
parsed_dates = pd.to_datetime(transactions_clean["timestamp"], errors="coerce")
transactions_clean = transactions_clean[parsed_dates.notna()]
after = len(transactions_clean)
print(f"\nDropped {before - after} rows with unparseable timestamp.")

negative_mask = transactions_clean["amount"] < 0
needs_review = transactions_clean[negative_mask].copy()
transactions_clean = transactions_clean[~negative_mask]

print(f"Moved {len(needs_review)} negative-amount rows to needs_review.")
print("Final clean transactions count:", len(transactions_clean))
print("Needs-review count:", len(needs_review))

OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

customers_clean.to_csv(OUTPUT_PATH / "customers.csv", index=False)
merchants_clean.to_csv(OUTPUT_PATH / "merchants.csv", index=False)
transactions_clean.to_csv(OUTPUT_PATH / "transactions.csv", index=False)
needs_review.to_csv(OUTPUT_PATH / "transactions_needs_review.csv", index=False)

print("\n--- FINAL SUMMARY ---")
print(f"Clean customers:    {len(customers_clean)}")
print(f"Clean merchants:    {len(merchants_clean)}")
print(f"Clean transactions: {len(transactions_clean)}")
print(f"Needs review:       {len(needs_review)}")
print(f"\nSaved to: {OUTPUT_PATH}")