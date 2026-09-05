# TransactionPulse — Project Status & Handoff Document

> **Purpose of this file:** If you are a teammate (or an AI assistant helping a
> teammate) picking up this project, read this document FIRST. It explains
> what has been built, why key decisions were made, and exactly what's left
> to do. Do not re-do or re-decide anything described as "DONE" below without
> checking with the team first — some decisions (especially in cleaning) were
> made deliberately and affect downstream phases.

---

## 1. What is TransactionPulse?

A data engineering project that takes raw customer, merchant, and
transaction data, validates it, cleans it, transforms it, and eventually
produces analytics-ready output — a mini real-world data pipeline (not just
a Python/SQL script exercise).

## 2. Project structure

```
TransactionPulse/
├── data/
│   ├── raw/                 # Original, clean, synthetically generated data (untouched)
│   ├── raw_dirty/           # Deliberately "messed up" copy — see Phase 5 notes below
│   ├── clean/                # Output of cleaning step (Phase 6) — analytics-ready-ish
│   │   └── transactions_needs_review.csv   # Judgment-call rows, NOT deleted (see below)
│   └── transformed/          # Output of transformation step (Phase 7) — final joined/summarized data
├── src/
│   ├── generate_data.py       # Generates the original synthetic data (Faker-based)
│   ├── inspect_data.py        # Phase 3/4: basic inspection + referential integrity check
│   ├── inject_dirty_data.py   # Phase 5 prep: deliberately injects realistic data issues
│   ├── data_quality_checks.py # Phase 5: full quality audit (nulls, dupes, invalid values, dates, types)
│   ├── clean_data.py          # Phase 6: applies fix/drop/quarantine rules
│   └── transform_data.py      # Phase 7: joins tables + builds customer/merchant summaries
├── requirements.txt
└── README.md
```

## 3. Phase-by-phase status

| Phase | Description | Status |
|---|---|---|
| 1 | Project setup (venv, folder structure) | ✅ Done |
| 2 | Understand raw data (schemas, row counts) | ✅ Done |
| 3 | Data inspection script | ✅ Done — `inspect_data.py` |
| 4 | Referential integrity check | ✅ Done — folded into `inspect_data.py` and re-verified in `data_quality_checks.py` |
| 5 | Full data quality checks (nulls, dupes, invalid values, dates, types) | ✅ Done — `data_quality_checks.py` |
| 6 | Data cleaning (fix / drop / quarantine) | ✅ Done — `clean_data.py` |
| 7 | Data transformation (joins + summaries) | ✅ Done — `transform_data.py` |
| 8 | SQL / database layer | 🔲 Not started |
| 9 | Full ETL pipeline (tie everything into one runnable pipeline) | 🔲 Not started |
| 10 | Automation (scheduling, logging) | 🔲 Not started |
| 11 | Analytics / dashboard (Streamlit, Power BI, etc.) | 🔲 Not started |
| 12 | Final documentation / project report | 🔲 Not started (this file is a working draft toward it) |

## 4. Key decisions made so far (IMPORTANT — read before continuing)

### Why there's both `data/raw/` and `data/raw_dirty/`
The original generated data (`generate_data.py`, using Faker) was too clean —
zero nulls, zero duplicates, no invalid values. That's unrealistic for a data
quality project, so `inject_dirty_data.py` was built to create a deliberately
messy COPY of the data at `data/raw_dirty/`, leaving `data/raw/` untouched.
All Phase 5/6 work is designed to run against `data/raw_dirty/`.

### Exactly what was injected (for reference)
- **Customers**: 5 blank cities, 4 duplicate rows, 3 invalid `customer_type`
  values ("UNKNOWN_TYPE"), 3 broken `created_at` dates
- **Merchants**: 2 blank categories, 1 duplicate `merchant_id` with a
  conflicting name (same ID, different merchant_name — a nastier kind of
  duplicate)
- **Transactions**: 10 blank amounts, 10 blank payment methods, 6 duplicate
  rows, 7 negative amounts, 4 invalid status values ("UNKNOWN"), 5 invalid
  customer_id references, 5 invalid merchant_id references, 5 unparseable
  timestamps

### Cleaning rules applied in `clean_data.py` (and WHY)
| Issue | Rule | Reasoning |
|---|---|---|
| Blank city / customer_name / category | Fill with `"Unknown"` | Not fatal — record is still usable |
| Blank payment_method | Fill with `"UNKNOWN"` | Record still usable for amount/status analysis |
| Blank amount | **Drop row** | Can't safely guess a money value |
| Duplicate rows (exact) | Keep first, drop rest | Standard dedup |
| Duplicate merchant_id (conflicting data) | Keep first occurrence only | Can't have two truths for one ID |
| Invalid customer_type / status | **Drop row** | No defined meaning for these values |
| Unparseable dates | **Drop row** | Can't safely guess a date |
| Invalid customer_id / merchant_id reference | **Drop row** | Orphaned transaction, can't be attributed to anyone |
| **Negative amounts** | **NOT dropped** — moved to `transactions_needs_review.csv` | Could be a legitimate refund/chargeback; needs human judgment, not deletion |
| **Future-dated transactions** | **NOT dropped** — same review file | Could be a legitimate scheduled/pending transaction |

**Do not silently change these rules** without team discussion — Phase 7+
work assumes `data/clean/` follows these exact rules.

### A subtlety worth knowing: cleaning order causes cascading drops
When customers with invalid `customer_type` or broken dates were dropped
from the customers table, this ALSO orphaned many transactions that
legitimately referenced those (now-removed) customers — far more than the
5 transactions we deliberately broke on purpose. Final count: 113
transactions dropped for invalid customer_id references (not just 5). This
is CORRECT behavior, not a bug: cleaning a parent table ripples into child
tables. Worth mentioning explicitly in the final Phase 12 report.

### A pandas gotcha worth knowing
`pd.to_datetime()` infers a date format from the first value in a column and
applies it to the WHOLE column. A future date injected in a slightly
different format (no microseconds) was silently marked "unparseable"
instead of being caught as a future date. Fixed using `format="mixed"`,
which lets pandas infer format per-value instead of column-wide. If you're
doing further date work, be aware of this.

## 5. Final row counts (after Phase 6 cleaning)

| Table | Original (raw) | Dirty (raw_dirty) | Clean (final) |
|---|---|---|---|
| Customers | 500 | 504 | 494 |
| Merchants | 50 | 51 | 50 |
| Transactions | 10,000 | 10,006 | 9,856 (+7 in needs_review) |

## 6. What Phase 7 (`transform_data.py`) produces

- `data/transformed/transactions_full.csv` — every clean transaction, joined
  with customer name/city/type and merchant name/category
- `data/transformed/customer_summary.csv` — per customer: total
  transactions, total spent, avg transaction amount, success/failed/pending
  counts, success rate
- `data/transformed/merchant_summary.csv` — per merchant: total
  transactions, total revenue, avg transaction amount

## 7. How to run everything (in order)

```bash
# 1. Set up environment (first time only)
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2. Generate the original synthetic data (only if data/raw/ is missing)
python src/generate_data.py

# 3. Inspect the raw data
python src/inspect_data.py

# 4. Create the deliberately-dirty dataset (only needs to be run once)
python src/inject_dirty_data.py

# 5. Run data quality checks (point at raw_dirty, raw, or clean — see --data-dir flag if added)
python src/data_quality_checks.py

# 6. Clean the data
python src/clean_data.py

# 7. Transform into analytics-ready output
python src/transform_data.py
```

## 8. What's left — suggested next owners

- **Phase 8 (SQL/database layer)**: load `data/clean/` or `data/transformed/`
  into SQLite/Postgres, write analytical SQL queries (top merchants, monthly
  trends, customer segmentation)
- **Phase 9 (Pipeline orchestration)**: one script that runs steps 3-7 above
  in sequence automatically
- **Phase 10 (Automation)**: proper logging (not just print statements),
  maybe scheduling
- **Phase 11 (Dashboard)**: a simple Streamlit (or similar) dashboard reading
  from `data/transformed/` or the Phase 8 database
- **Phase 12 (Documentation)**: the final project report — this file is a
  head start on that

## 9. For AI assistants continuing this project

If you are Claude, ChatGPT, or another AI assistant helping a teammate
continue this project: please read this entire document before writing any
code. The team has made specific, documented decisions (Section 4) that
should be preserved unless the team explicitly decides to change them.
Prefer extending the existing scripts/patterns shown above over rewriting
from scratch, so the codebase stays consistent across team members.
