import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
from typing import Optional

from gen_salt import gen_salt
from logger import logger_config

class FileHandler:
    def __init__(
        self, 
        *paths: str, 
        password: str, 
        decrypt_flag: bool = False,
        env_path: Optional[str] = None
    ) -> None:
        # Logger
        self.logger = logger_config("FileHandler")

        # Salt
        gen_salt(env_path)

        self.paths = paths
        self._salt = os.getenv("SALT", "").encode()
        self._password = password
        self.decrypt_flag = decrypt_flag

        # Set KDF
        self.kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.get_salt(),
            iterations=1_200_000
        )

        # Set key
        self.derive_key_from_password()

        # Create Fernet object
        self.fernet = Fernet(self.get_key())

        self.logger.debug(f"Paths: {" ".join(path for path in self.paths)}")

    def main(self) -> None:
        for path in self.paths:
            self.logger.debug(f"Path: {path}")

            try:
                if self.is_dir(path):
                    raise ValueError("Path cannot be a directory")

                if not self.decrypt_flag:
                    self.encrypt_file(path)
                else:
                    self.decrypt_file(path)
            except Exception as e:
                self.logger.error(e, exc_info=True)

    def derive_key_from_password(self) -> None:
        self._raw_key = self.kdf.derive(self.get_password().encode())
        self._key = urlsafe_b64encode(self.get_raw_key())
    
    def verify_key(self) -> None:
        return self.kdf.verify(self.get_password().encode(), self.get_key())
    
    def encrypt_file(self, path: str) -> None:
        self.logger.info("Encrypting file...")

        try:
            # Read file
            with open(path, "rb") as file:
                data = file.read()
                self.logger.debug("Read file successfully")

            encrypted = self.fernet.encrypt(data)
            self.logger.debug("Encrypted data successfully")

            # Save file with password
            with open(path, mode="wb") as file:
                file.write(encrypted)
        except Exception as e:
            self.logger.error(f"Error encrypting file: {e}", exc_info=True)
            raise

    def decrypt_file(self, path: str) -> None:
        self.logger.info("Decrypting file...")

        try:
            # Read file
            with open(path, "rb") as file:
                encrypted = file.read()
                self.logger.debug("Read data successfully")

            decrypted = self.fernet.decrypt(encrypted)
            self.logger.debug("Decrypted data successfully")

            # Save file
            with open(path, "wb") as file:
                file.write(decrypted)
        except Exception as e:
            self.logger.error(f"Error decrypting file: {e}", exc_info=True)

    # --- Utils ---
    def is_dir(self, path: str) -> bool:
        return os.path.isdir(path)

    def is_abs_path(self, path: str) -> bool:
        return os.path.isabs(path)
    
    # --- Getters and setters ---
    def get_salt(self) -> bytes:
        return self._salt
    
    def get_password(self) -> str:
        return self._password
    
    def get_key(self) -> bytes:
        return self._key
    
    def get_raw_key(self) -> bytes:
        return self._raw_key