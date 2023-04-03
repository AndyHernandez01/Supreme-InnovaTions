import os
import time
import base64
import binascii
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.hmac import HMAC
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class InvalidToken(Exception):  # Raised when integrity has been compromised
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class KeyLengthError(Exception):  # Indicates issues with the key provided to the Crypto_Cipher class
    def __init__(self, key_length, key_type):
        self.key_length = key_length
        self.key_type = key_type
        super().__init__(f"Key must be a bytes object of length 32, A {self.key_type} object of length {self.key_length} was provided")

class Crypto_Cipher_Test:
    def __init__(self, key):
        if len(key) != 32 or not isinstance(key, bytes):  # Make sure the key is a bytes object of length 32
            raise KeyLengthError(len(key), type(key))
        self._key = key
        self._integrity_key = self._key[:16]
        self._confidentiality_key = self._key[16:]

    def encrypt_test(self, plaintext: bytes) -> bytes:
        """ Works the same as encrypt() from Crypto_Cipher() """

        if not isinstance(plaintext, bytes):  # Check if the plaintext is of type bytes
            raise TypeError(f"Plaintext must be bytes, {type(plaintext)} was provided instead")

        current_time = int(time.time())  # Time of encryption
        iv = os.urandom(16)  # 128-bit Initialization Vector

        pad = padding.PKCS7(algorithms.AES.block_size).padder()  # Makes PaddingContext obj to pad data to mult of 8
        padded_data = pad.update(plaintext) + pad.finalize()  # Padded plaintext

        # Encryptor that uses AES with a 128-bit key and CBC mode with a 128-bit IV
        encryptor = Cipher(algorithms.AES(self._confidentiality_key), modes.CBC(iv)).encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()  # Encrypted data

        ciphertext_package = (
            current_time.to_bytes(length=8, byteorder="big")  # Current time for time-based authentication
            + iv  # IV needed to decrypt the ciphertext
            + ciphertext)

        hasher = HMAC(self._integrity_key, hashes.SHA256())  # HMAC obj that uses the signing key and sha256
        hasher.update(ciphertext_package)
        hmac = hasher.finalize()  # HMAC for integrity
        return base64.urlsafe_b64encode(ciphertext_package + hmac)

    def decrypt_test(self, data: bytes, ttl: int = None, mode: int = None) -> bytes:
        """
        Tests the integrity of the encrypted data
        mode 1: Tests an expired TTL
        mode 2: Tests a modified HMAC from encryption
        mode 3: Tests modification of the package created during encryption
        """

        try:  # Ensure the data is the correct format and decode it
            decoded_data = base64.urlsafe_b64decode(data)
        except (TypeError, binascii.Error):
            raise InvalidToken("Ciphertext must be encoded with url safe base64 encoding")

        # Unpack all data sent from encryption
        time_of_encryption = int.from_bytes(decoded_data[0:8], byteorder="big")
        iv = decoded_data[8:24]
        ciphertext = decoded_data[24:-32]
        encryption_hmac = decoded_data[-32:]
        ciphertext_package = decoded_data[:-32]  # Used to confirm integrity

        if mode == 1:  # TTL passed
            ttl = 1
            time.sleep(2)
        elif mode == 2:  # HMAC changed
            encryption_hmac = encryption_hmac[:-1]
        elif mode == 3:  # ciphertext package changed (time + iv + ciphertext)
            ciphertext_package = ciphertext_package[:-1]

        if ttl is not None:  # Execute if a TTL value has been passed
            try:
                # Check if the data has been sent within the TTL period
                current_time = int(time.time())
                if time_of_encryption + ttl < current_time:
                    raise InvalidToken("Message is invalid: TTL has been passed")
            except TypeError:  # Raise an error if the TTL is not a number
                raise TypeError(f"TTL must be a number, A {type(ttl)} was provided")

        try:  # Raise an error if the data hash does not match the hash received
            h = HMAC(self._integrity_key, hashes.SHA256())
            h.update(ciphertext_package)  # Hash the data sent
            h.verify(encryption_hmac)  # Verify the data hash using the HMAC sent
        except InvalidSignature:
            raise InvalidToken("HMACs do not match")

        # Decryptor object using 128-bit AES in CBC mode with the received IV
        decryptor = Cipher(algorithms.AES(self._confidentiality_key), modes.CBC(iv)).decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()  # Decrypt the ciphertext
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()  # Unpad the plaintext
        return plaintext


key = os.urandom(32)
crypt = Crypto_Cipher_Test(key)
ct = crypt.encrypt_test(b"hello")
pt = crypt.decrypt_test(ct, 6, 3)
print(pt.decode())

