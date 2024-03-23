from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode
from os import urandom
from dotenv import load_dotenv
import os

class Security:
    def __init__(self, key):
        if isinstance(key, str):
            # If key is a string, encode it
            self.key = key.encode()
        elif isinstance(key, bytes):
            # If key is already bytes, just assign it
            self.key = key
        else:
            raise TypeError("Key must be a string or bytes.")
        
        if len(self.key) != 32:
            raise ValueError("Key must be 32 bytes long.")

    def encryption(self, plaintext):
        iv = urandom(16)  # Randomly generate an IV
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padded_plaintext = self._pad(plaintext).encode()  # Padding to ensure block size alignment and encode to bytes
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

        # Return the IV and the ciphertext, both encoded in base64 to ensure safe string representation
        return b64encode(iv + ciphertext).decode()

    def decryption(self, encoded_ciphertext):
        raw_ciphertext = b64decode(encoded_ciphertext)
        iv = raw_ciphertext[:16]  # Extract the first 16 bytes as the IV
        actual_ciphertext = raw_ciphertext[16:]  # The rest is the actual ciphertext
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()

        # Unpad the plaintext after decryption and decode to a string
        return self._unpad(padded_plaintext).decode()

    @staticmethod
    def _pad(s):
        # Padding to block size (16 bytes for AES)
        block_size = 16
        number_of_padding_bytes = block_size - len(s) % block_size
        padding = chr(number_of_padding_bytes) * number_of_padding_bytes
        return s + padding

    @staticmethod
    def _unpad(s):
        # Remove padding from decrypted plaintext
        return s[:-ord(s[len(s) - 1:])]
