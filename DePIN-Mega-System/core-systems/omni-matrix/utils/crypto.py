#!/usr/bin/env python3
"""
Cryptographic utilities for Omni-Matrix
"""

import os
import hashlib
import hmac
from typing import Union, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64


def generate_key(password: Optional[str] = None) -> bytes:
    """Generate encryption key"""
    if password:
        # Derive key from password
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=os.urandom(16),
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))
    else:
        # Generate random key
        return Fernet.generate_key()


def encrypt_data(data: Union[str, bytes], key: bytes) -> bytes:
    """Encrypt data using Fernet"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    f = Fernet(key)
    return f.encrypt(data)


def decrypt_data(encrypted_data: bytes, key: bytes) -> bytes:
    """Decrypt data using Fernet"""
    f = Fernet(key)
    return f.decrypt(encrypted_data)


def encrypt_aes_gcm(
    data: Union[str, bytes],
    key: bytes,
    associated_data: Optional[bytes] = None
) -> tuple:
    """Encrypt data using AES-256-GCM"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, data, associated_data)
    
    return nonce, ciphertext


def decrypt_aes_gcm(
    nonce: bytes,
    ciphertext: bytes,
    key: bytes,
    associated_data: Optional[bytes] = None
) -> bytes:
    """Decrypt data using AES-256-GCM"""
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, associated_data)


def hash_data(data: Union[str, bytes], algorithm: str = 'sha256') -> str:
    """Hash data using specified algorithm"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    if algorithm == 'sha256':
        return hashlib.sha256(data).hexdigest()
    elif algorithm == 'sha512':
        return hashlib.sha512(data).hexdigest()
    elif algorithm == 'blake2b':
        return hashlib.blake2b(data).hexdigest()
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")


def verify_hmac(data: bytes, signature: bytes, key: bytes) -> bool:
    """Verify HMAC signature"""
    expected = hmac.new(key, data, hashlib.sha256).digest()
    return hmac.compare_digest(expected, signature)


def generate_hmac(data: bytes, key: bytes) -> bytes:
    """Generate HMAC signature"""
    return hmac.new(key, data, hashlib.sha256).digest()
