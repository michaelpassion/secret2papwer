# -*- coding: utf-8 -*-

from cryptography.fernet import Fernet

def generate_key():
    """生成秘钥并保存到文件
    Returns: None
    """
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    

def load_key():
    """加载key

    Returns: None
    """
    return open("secret.key", "rb").read()


def encrypt_message(message):
    """加密信息

    Args:
        message (string): 待加密的字符串

    Returns:
        string: 加密后的字符串
    """
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypt_message = f.encrypt(encoded_message)
    return encrypt_message


def decrypt_message(encrypted_message):
    """加密信息

    Args:
        encrypted_message (string): 加密的字符串

    Returns:
        string: 解密后的字符串
    """
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    return decrypted_message.decode()

if __name__ == "__main__":
    # generate_key() # execute only once 
    # encrypt_message("Hello world")
    decrypt_message(b'gAAAAABk4x4CvJGOmq1na3FxpkP88OqV9-S71ZYjDYFvQI5lPSvV7pu36Ps8E75JmxoOA8wQW9LGgXzG4u1omtzf7_nCgfSBnw==')