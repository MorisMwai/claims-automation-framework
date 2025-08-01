import re
import json
from datetime import datetime

def validate_claim(policy_id, amount, claim_date_raw, branch, claim_type):
    """
    Validate insurance claim data and return structured dictionary.
    All inputs are expected as strings.
    """
    errors = []
    normalized_date = None
    parsed_amount = None
    is_valid = True

    # Clean input
    policy_id = policy_id.strip()
    amount = amount.strip()
    claim_date_raw = claim_date_raw.strip()
    branch = branch.strip()
    claim_type = claim_type.strip()

    # Validate Policyholder_ID
    if not re.fullmatch(r"[A-Za-z0-9]{6}", policy_id):
        errors.append("Invalid Policyholder_ID: Must be 6-character alphanumeric")

    # Validate Claim_Amount
    try:
        amount_val = float(amount)
        parsed_amount = amount_val
        if amount_val <= 0:
            errors.append("Invalid Claim_Amount: Must be positive")
        elif amount_val > 1_000_000:
            errors.append("Invalid Claim_Amount: Exceeds KES 1,000,000")
    except:
        errors.append("Invalid Claim_Amount: Not a valid number")

    # Validate and normalize Claim_Date
    valid_formats = ["%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y"]
    parsed = None
    for fmt in valid_formats:
        try:
            parsed = datetime.strptime(claim_date_raw, fmt)
            break
        except ValueError:
            continue
    if parsed:
        if parsed < datetime(2024, 7, 23):
            errors.append("Invalid Claim_Date: Earlier than 2024-07-23")
        elif parsed > datetime(2025, 7, 23):
            errors.append("Invalid Claim_Date: Later than 2025-07-23")
        else:
            normalized_date = parsed.strftime("%Y-%m-%d")
    else:
        errors.append("Invalid Claim_Date: Invalid format")

    # Validate Branch
    if branch not in ["Kenya", "Uganda", "South Sudan", "Malawi"]:
        errors.append(f"Invalid Branch: {branch}")

    # Validate Claim_Type
    if claim_type not in ["Health", "Motor", "Property", "Education"]:
        errors.append(f"Invalid Claim_Type: {claim_type}")

    if errors:
        is_valid = False

    result ={
        "IsValid": is_valid,
        "ErrorDescription": "; ".join(errors),
        "NormalizedDate": normalized_date,
        "ParsedAmount": parsed_amount,
        "RawDate": claim_date_raw,
        "Policyholder_ID": policy_id,
        "Branch": branch,
        "Claim_Type": claim_type
    }
    
    return json.dumps(result)

# 🧪 Standalone test
if __name__ == "__main__":
    print(validate_claim(
        policy_id="ABC123",
        amount="35245.6",
        claim_date_raw="10-10-2026",  # invalid format + out of range
        branch="Kenya",
        claim_type="Health"
    ))