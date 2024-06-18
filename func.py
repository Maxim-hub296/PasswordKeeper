import toml
from const import FILE_NAME_DB
from passlib.context import CryptContext
from cryptography.fernet import Fernet
import base64


def create_toml_file():
    data = {
        "users": {
        },
        "passwords": {
        }
    }

    with open(FILE_NAME_DB, "w") as file:
        toml.dump(data, file)


def read_toml_file():
    with open(FILE_NAME_DB, "r") as file:
        data = toml.load(file)
        return data


def write_toml_file(data: dict):
    with open(FILE_NAME_DB, "w") as file:
        toml.dump(data, file)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)


class Crypto:

    @staticmethod
    def generate_cipher_suite(user_password):
        # Преобразование строки в байты
        bytes_data = user_password.encode()

        # Дополнение строки до 32 байт
        while len(bytes_data) < 32:
            bytes_data += b'\x00'

        # Преобразование в base64
        key = base64.b64encode(bytes_data)

        # Создание шифра на основе ключа
        cipher_suite = Fernet(key)
        return cipher_suite

    @staticmethod
    def encrypt(plain_text, user_password):
        cipher_suite = Crypto.generate_cipher_suite(user_password)
        encrypted_text = cipher_suite.encrypt(plain_text.encode())
        encrypted_text = Crypto.bytes_to_utf8(encrypted_text)
        return encrypted_text

    @staticmethod
    def decrypt(encrypted_text, user_password):
        cipher_suite = Crypto.generate_cipher_suite(user_password)
        text = Crypto.utf8_to_bytes(encrypted_text)
        decrypted_text = cipher_suite.decrypt(text).decode()
        return decrypted_text

    @staticmethod
    def bytes_to_utf8(byte_string):
        utf8_string = byte_string.decode('utf-8')
        return utf8_string

    @staticmethod
    def utf8_to_bytes(utf8_string):
        byte_string = utf8_string.encode('utf-8')
        return byte_string


encrypt_pass = 'gAAAAABmcUthEcdUJNshonwtpWKvYkLwpdau1JL22oQQqh9HPpG5vZYtz76jBLgNl2PM9BbRKD62zn-M0ShGWIRon_LjI8fUEw=='
user_password = '1'

print(Crypto.decrypt(encrypt_pass, user_password))
