# TransactionPulse

A beginner-friendly **Data Engineering project** focused on generating, processing, and validating structured transaction data using Python and Pandas.

## 📌 Project Overview

**TransactionPulse** simulates a transaction data environment containing customers, merchants, and transactions.

The project focuses on basic data engineering concepts such as **data generation, data processing, data inspection, validation, and ETL workflows**.

## 🎯 Objectives

- Generate realistic customer, merchant, and transaction datasets.
- Process structured data using Python and Pandas.
- Perform data inspection and validation.
- Maintain consistency between related datasets.
- Apply basic data engineering and ETL concepts.
- Manage project development using Git and GitHub.

## 📊 Dataset

The project contains:

| Dataset | Records |
|---|---:|
| Customers | 500 |
| Merchants | 50 |
| Transactions | 10,000 |

### Customers

- `customer_id`
- `customer_name`
- `city`
- `customer_type`
- `created_at`

### Merchants

- `merchant_id`
- `merchant_name`
- `category`
- `city`
- `created_at`

### Transactions

The transaction dataset connects customers and merchants through their respective IDs.

## 🔄 Project Workflow

```text
Data Generation
      ↓
Data Processing
      ↓
Data Inspection
      ↓
Data Validation
      ↓
Data Quality Checks
      ↓
Validated Dataset
```

## ✅ Data Quality Validation

The project includes **referential integrity checks** to ensure that transaction records correctly reference existing customers and merchants.

### Validation Result

```text
Invalid customer references: 0
Invalid merchant references: 0
```

This confirms that all customer and merchant references in the generated transaction data are valid.

## 🛠️ Tech Stack

- **Python**
- **Pandas**
- **SQL**
- **ETL Concepts**
- **Git**
- **GitHub**
- **VS Code**

## 📁 Project Structure

```text
TransactionPulse/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── data generation
│   ├── data processing
│   └── data inspection
│
├── requirements.txt
├── README.md
└── PROJECT_STATUS.md
```

> The exact files may vary depending on the current repository structure.

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd TransactionPulse
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**macOS / Linux:**

```bash
source .venv/bin/activate
```

**Windows:**

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

Run the project scripts according to the workflow documented in the repository.

## 📈 Results

The project successfully generated and processed:

- **500 customers**
- **50 merchants**
- **10,000 transactions**

Data validation produced:

- **0 invalid customer references**
- **0 invalid merchant references**

## 📚 What I Learned

Through this project, I gained practical exposure to:

- Working with structured datasets.
- Using Python and Pandas for data processing.
- Understanding basic ETL workflows.
- Performing data inspection and validation.
- Maintaining relationships between datasets.
- Using Git and GitHub for collaborative project development.

## 🔮 Future Improvements

Possible future improvements include:

- Adding more advanced data quality checks.
- Connecting the pipeline to a SQL database.
- Automating the ETL workflow.
- Adding transaction-level analytics.
- Building a dashboard for transaction insights.
- Exploring cloud-based data engineering tools.

## 👥 Project

**TransactionPulse** was developed as a collaborative Data Engineering project using Git/GitHub for project management and version control.
