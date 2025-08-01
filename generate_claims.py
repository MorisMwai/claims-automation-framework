import pandas as pd
import random
import string
from datetime import datetime, timedelta
import os

# -------------------------
# CONFIGURATION
# -------------------------

OUTPUT_FILE = r"C:\Users\MorisMwaiWachira\Desktop\MorisMwai_RPA_Assignment\CIC_Claims_Automation_Assessment\Data\Input\claims_data.xlsx" # Change this path as needed
NUM_RECORDS = 100                         
TARGET_INVALID_MIN = 25                  
TARGET_INVALID_MAX = 35                  

BRANCHES = ["Kenya", "Uganda", "South Sudan", "Malawi"]
CLAIM_TYPES = ["Health", "Motor", "Property", "Education"]
VALID_START_DATE = datetime(2024, 7, 23)
VALID_END_DATE = datetime(2025, 7, 23)

# -------------------------
# VALID & INVALID GENERATORS
# -------------------------

# Policyholder ID must be 3 uppercase letters + 3 digits (e.g., ABC123)
def generate_valid_policyholder_id():
    """Generate a valid 6-character alphanumeric Policyholder_ID."""
    return ''.join(random.choices(string.ascii_uppercase, k=3)) + ''.join(random.choices(string.digits, k=3))

def generate_invalid_policyholder_id():
    """Return an invalid Policyholder_ID based on length or format."""
    return random.choice([
        ''.join(random.choices(string.ascii_uppercase + string.digits, k=4)),  # Too short
        ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)),  # Too long
        "AB12!@",  # Invalid characters
        "12345!"   # Mixed formatting
    ])

# Claim Amount must be between 1,000 and 1,000,000
def generate_valid_claim_amount():
    """Generate a valid Claim_Amount (1000 - 1,000,000)."""
    return round(random.uniform(1000, 1000000), 2)

def generate_invalid_claim_amount():
    """Return an invalid Claim_Amount based on business rules."""
    return random.choice([-1000, 0, 1500000])  # Negative, zero, or over-limit

# Dates between July 23, 2024 and July 23, 2025 are valid
def generate_valid_claim_date():
    days_range = (VALID_END_DATE - VALID_START_DATE).days
    date = VALID_START_DATE + timedelta(days=random.randint(0, days_range))
    return date.strftime("%Y-%m-%d")

def generate_invalid_claim_date(branch=None):
    # Malawi bias: tends to use DD-MM-YYYY format
    if branch == "Malawi" and random.random() < 0.7:
        return datetime.now().strftime("%d-%m-%Y") # Accepted format in validator
    
    return random.choice([
        "2024-07-22",  # Too early
        "2025-07-24",  # Too late
        "22-07-2025",  # Wrong format
        "2026-01-01"   # Way too late
    ])

def generate_valid_branch():
    return random.choice(BRANCHES)

def generate_invalid_branch():
    return random.choice(["Tanzania", "Rwanda", "Nairobi"])

def generate_valid_claim_type():
    return random.choice(CLAIM_TYPES)

def generate_invalid_claim_type():
    return random.choice(["Life", "Marine", "Auto"])

# Generate document path based on Claim_ID
def generate_valid_supporting_document(claim_id):
    return os.path.join("C:\\docs", f"{claim_id}.pdf")

def generate_invalid_supporting_document():
    return random.choice([None, "", "invalid_path"])

# -------------------------
# FIELD CORRUPTION LOGIC
# -------------------------

def corrupt_field(row, field, branch=None):
    """Apply appropriate corruption to a single field of the row."""
    if field == "Policyholder_ID":
        row[field] = generate_invalid_policyholder_id()
    elif field == "Claim_Amount":
        row[field] = generate_invalid_claim_amount()
    elif field == "Claim_Date":
        row[field] = generate_invalid_claim_date(branch)
    elif field == "Branch":
        row[field] = generate_invalid_branch()
    elif field == "Claim_Type":
        row[field] = generate_invalid_claim_type()
    elif field == "Supporting_Document":
        row[field] = generate_invalid_supporting_document()

# -------------------------
# MAIN GENERATION LOGIC
# -------------------------

def generate_claims():
    """Generate synthetic claims with realistic bias and track validation stats."""
    data = []
    target_invalid = random.randint(TARGET_INVALID_MIN, TARGET_INVALID_MAX)
    injected_invalid = 0
    regional_bias_count = 0

    print(f" Target: {target_invalid} invalid records from {NUM_RECORDS} total")

    for i in range(NUM_RECORDS):
        # Precompute remaining counts
        remaining = NUM_RECORDS - i
        remaining_needed = target_invalid - injected_invalid
        
        # Decide if this record should be globally invalid
        should_be_invalid = (
            remaining_needed >= remaining or
            random.random() < (remaining_needed / remaining)
        )
        
        # Generate base row with valid data
        branch = generate_valid_branch()
        claim_id = f"CLM{str(i+1).zfill(3)}"

        # Start with a clean, valid row
        row = {
            "Policyholder_ID": generate_valid_policyholder_id(),
            "Claim_ID": claim_id,
            "Claim_Amount": generate_valid_claim_amount(),
            "Claim_Date": generate_valid_claim_date(),
            "Branch": branch,
            "Claim_Type": generate_valid_claim_type(),
            "Supporting_Document": generate_valid_supporting_document(claim_id)
        }
        
        # -----------------------------
        # Apply Regional Biases (Not always invalid)
        # -----------------------------

        if branch == "Malawi" and random.random() < 0.6:
            row["Claim_Date"] = generate_invalid_claim_date(branch)
            regional_bias_count += 1

        if branch == "South Sudan" and random.random() < 0.6:
            row["Supporting_Document"] = generate_invalid_supporting_document()
            regional_bias_count += 1

        if branch in ["Kenya", "Uganda"] and random.random() < 0.4 and injected_invalid < target_invalid:
            row["Policyholder_ID"] = generate_invalid_policyholder_id()
            regional_bias_count += 1
            injected_invalid += 1  # Kenya/Uganda ID corruption should be treated as invalid

        # ---------------------------------
        # Apply General Corruptions
        # ---------------------------------

        if should_be_invalid and injected_invalid < target_invalid:
            corrupt_fields = random.sample(
                ["Policyholder_ID", "Claim_Amount", "Claim_Date", "Branch", "Claim_Type"],
                random.randint(1, 2)
            )

            for field in corrupt_fields:
                corrupt_field(row, field, branch)
            injected_invalid += 1

        # Add finalized row to dataset
        data.append(row)

    # Save the generated data to Excel
    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df.to_excel(OUTPUT_FILE, index=False, sheet_name="ClaimsData")

    # Display summary
    print(f" Generated {NUM_RECORDS} records")
    print(f" Injected {injected_invalid} invalid rows")
    print(f" Rows with regional bias: {regional_bias_count}")
    print(f" Output saved to: {OUTPUT_FILE}")

    return df

# -------------------------
# SCRIPT ENTRY POINT
# -------------------------

if __name__ == "__main__":
    generate_claims()