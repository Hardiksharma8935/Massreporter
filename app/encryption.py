from cryptography.fernet import Fernet
import os
from app.config import ENCRYPTION_KEY
import logging

if not ENCRYPTION_KEY:
    logging.warning("No ENCRYPTION_KEY provided. Using a temporary key for startup. THIS IS NOT FOR PRODUCTION.")
    key = Fernet.generate_key()
else:
    key = ENCRYPTION_KEY.encode()

cipher_suite = Fernet(key)

def encrypt_session(session_string: str) -> bytes:
    return cipher_suite.encrypt(session_string.encode())

def decrypt_session(encrypted_session: bytes) -> str:
    return cipher_suite.decrypt(encrypted_session).decode()
  
