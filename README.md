# Claims Automation Framework

This project automates the end-to-end process of validating and processing insurance claims. It uses **UiPath REFramework (C#)** for transaction handling, integrates **Python** for encryption and data processing, **SQLite** for structured storage, and **Excel** for reporting.

---

## ✅ Key Features
- Reads claims data from Excel.
- Applies validation rules for policy IDs, claim amounts, dates, branches, and claim types.
- Encrypts sensitive data (Policyholder_ID) using SHA-256 in Python.
- Stores valid and invalid claims in an SQLite database.
- Generates a compliance summary report in Excel.
- Handles error scenarios such as missing files, invalid data, and database errors.

---

## 🛠 Tech Stack
- **UiPath Studio** (REFramework in C#)
- **Python 3.12.x** with:
  - `pandas`
  - `openpyxl`
- **SQLite**
- **Excel**

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/claims-automation-framework.git
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
````

### 3. Install UiPath Packages
- `UiPath.Excel.Activities`
- `UiPath.Database.Activities`
- `UiPath.Python.Activities`

### 4. Configure Paths
Update Config.xlsx in the Data folder with:
 - `Input and output file paths`
 - `Database path`
 - `Python script locations`


## ▶️ How to Run
1. Open the UiPath project in UiPath Studio.
2. Run Main.xaml.
3. The process will:
    - Read the input claims Excel file
    - Validate and encrypt data
    - Insert records into SQLite
    - Generate a summary report

## 🧪 Testing
Use the Testing folder for:
 - Empty or missing input file
 - Corrupted Excel file
 - Database connection failure
