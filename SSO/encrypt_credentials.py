from cryptography.fernet import Fernet

def load_key():
    """Loads the secret key from a secure location (e.g., environment variable)."""
    key = os.environ.get("SECRET_KEY")
    if not key:
        raise ValueError("SECRET_KEY environment variable not set!")
    return key.encode()  # Ensure key is a byte string for Fernet

def encrypt_data(data):
    key = load_key()
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data.decode()

# correct_email = "saravanakumar.a@signatech.com"
# correct_password = "Cristiano7$S"
# wrong_email = "invalid_email"
# wrong_password = "invalid_password"

# encrypted_correct_email = encrypt_data(correct_email)
# encrypted_correct_password = encrypt_data(correct_password)
# encrypted_wrong_email = encrypt_data(wrong_email)
# encrypted_wrong_password = encrypt_data(wrong_password)

# print(f"Encrypted Correct Email: {encrypted_correct_email}")
# print(f"Encrypted Correct Password: {encrypted_correct_password}")
# print(f"Encrypted Wrong Email: {encrypted_wrong_email}")
# print(f"Encrypted Wrong Password: {encrypted_wrong_password}")