import os
import time
import base64
import binascii
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.hmac import HMAC
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Documentation: https://cryptography.io/en/latest/
''' NOTE: COPIED CODE
The documentation gave very detailed instructions on how to write the code in most cases
Most of the code for setting up classes and using their methods are directly from the documentation
    IE: Cipher(algorithms.AES(self.encryption_key), modes.CBC(iv)).encryptor()
    IE: encryptor.update(padded_data) + encryptor.finalize()
The most detailed AES documentation already used 128bit keys, so most numbers did not need to be changed 
'''
class InvalidToken(Exception):
    pass

class Crypto_Cipher:
    def __init__(self, key):
        if len(key) != 32:
            print("Key must be 32 bytes to split into 2 16 byte keys")
            raise InvalidToken
        self._key = key
        self._integrity_key = self._key[:16]
        self._encryption_key = self._key[16:]

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        Encrypts plaintext of bytes format
        Encryption is 128bit AES in CBC mode
        Integrity achieved with HMAC using sha256
        Confidentiality and integrity keys are both 128bit
        :return: An encoded value containing the ciphertext, iv, time, and hmac
        """
        if not isinstance(plaintext, bytes):  # Check if the plaintext is of type bytes
            print("Plaintext must be bytes")
            raise InvalidToken

        current_time = int(time.time())  # Time of encryption
        iv = os.urandom(16)  # Initialization Vector

        pad = padding.PKCS7(algorithms.AES.block_size).padder()  # Makes PaddingContext obj to pad data to mult of 8
        padded_data = pad.update(plaintext) + pad.finalize()  # Padded plaintext

        # Encryptor that uses AES with a 128bit key and CBC mode with a 128bit IV
        encryptor = Cipher(algorithms.AES(self._encryption_key), modes.CBC(iv)).encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()  # Encrypted data

        basic_parts = (  # Taken from documentation; Matched needed data so code was left unchanged
            b"\x80"  # Starting byte
            + current_time.to_bytes(length=8, byteorder="big")  # Current time for time-based authentication
            + iv  # IV needed to decrypt the ciphertext
            + ciphertext)

        h = HMAC(self._integrity_key, hashes.SHA256())  # HMAC obj that uses the signing key and sha256
        h.update(basic_parts)
        hmac = h.finalize()  # HMAC for integrity
        return base64.urlsafe_b64encode(basic_parts + hmac)

    def decrypt(self, data: bytes, ttl: int = None) -> bytes:
        """
        Decrypts ciphertext sent from the encrypt() method
        Optionally takes a time to live (TTL) value to ensure recency of the message
        Uses HMACs to determine message integrity
        :return: plaintext in bytes format
        """
        # Ensure the data is the correct format and decode it
        try:
            decoded_data = base64.urlsafe_b64decode(data)
        except (TypeError, binascii.Error):
            raise InvalidToken

        # Unpack all data sent from encryption
        sent_time = int.from_bytes(decoded_data[1:9], byteorder="big")
        iv = decoded_data[9:25]
        ciphertext = decoded_data[25:-32]
        sent_hmac = decoded_data[-32:]
        basic_parts = decoded_data[:-32]

        if ttl is not None:  # Execute if a TTL value has been passed
            try:
                # Check if the data has been sent within the TTL period
                current_time = int(time.time())
                if sent_time + ttl < current_time:
                    print("Message is invalid: TTL has been passed")
                    raise InvalidToken
            except TypeError:  # Raise an error if the TTL is not a number
                print("TTL must be a number")
                raise InvalidToken

        try:  # Raise an error if the data hash does not match the sent hash
            h = HMAC(self._integrity_key, hashes.SHA256())
            h.update(basic_parts)  # Hash the data sent
            h.verify(sent_hmac)  # Verify the data hash using the HMAC sent
        except InvalidSignature:
            raise InvalidToken

        # Decryptor object using 128bit AES in CBC mode with the sent IV
        decryptor = Cipher(algorithms.AES(self._encryption_key), modes.CBC(iv)).decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()  # Decrypt the ciphertext
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()  # Unpad the plaintext
        return plaintext


# f = open("example.json", 'rb')
# data = f.read()
# f.close()
data = b"Demo"
key = b'A\x18\x86\xfd\xbf\x10\x802\xa4\xf3\xb9\x08\x12\x17!\x9crWc^\xa4\x1c\x1eoj\xc6\xefd1t\xa8w'
# key = os.urandom(32)
crypt = Crypto_Cipher(key)
ct = crypt.encrypt(data)
pt = crypt.decrypt(ct)
print(pt)
# print(ct)
# time.sleep(1)
# pt = crypt.decrypt(ct, 3)
# print(pt)

