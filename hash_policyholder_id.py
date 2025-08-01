import hashlib

def hash_policyholder_id(policyholder_id):
    """
    Hashes the given Policyholder_ID using SHA-256.
    Parameters:
        policyholder_id (str): The Policyholder_ID to hash.
    Returns:
        str: SHA-256 hash of the Policyholder_ID in hexadecimal format.
    """
    try:
        # Handle None or empty strings
        if not policyholder_id or not isinstance(policyholder_id, str):
            return "INVALID_INPUT"

        # Encode the string to bytes
        encoded_id = policyholder_id.encode('utf-8')

        # Compute SHA-256 hash
        hashed_value = hashlib.sha256(encoded_id).hexdigest()

        return hashed_value

    except Exception as e:
        return f"ERROR: {str(e)}"


# For standalone testing
if __name__ == "__main__":
    sample_id = "MMW254"
    print(f"Original ID: {sample_id}")
    print(f"Hashed ID: {hash_policyholder_id(sample_id)}")