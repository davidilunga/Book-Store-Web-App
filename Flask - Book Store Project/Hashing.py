import random
import string
import hashlib
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def hash_password(password, salt):
    iterations = 10000
    key_length = 64  # 64 bytes for SHA-512
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        iterations=iterations,
        length=key_length,
        salt=salt.encode(),
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def generate_secure_password(password, salt):
    # Hashing the password with PBKDF2-HMAC-SHA512
    secure_password = hash_password(password, salt)
    
    # Base64 encode the hashed password
    encoded_secure_password = base64.b64encode(secure_password).decode()
    
    return encoded_secure_password

class PasswordHash:

    global_salt = ""

    def get_salt(length):
        alphabet = string.ascii_letters + string.digits
        return ''.join(random.choice(alphabet) for _ in range(length))
    # Example usage:
    def run(password, generated_salt):

        secure_password = generate_secure_password(password, generated_salt)
        return secure_password
    
    def checkPassword(salt, saved_password, password):
        secure_password = generate_secure_password(password, salt)
        if secure_password == saved_password:
            return True
        else:
            return False