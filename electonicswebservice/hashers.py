import zlib
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import json
import base64, os


def generate_keys_rsa():
    modulus_length = 256*16
    privatekey = RSA.generate(modulus_length, Random.new().read)
    publickey = privatekey.publickey()
    exprivatekey = base64.b85encode(base64.b64encode(privatekey.exportKey())).decode()
    expublickey = base64.b85encode(base64.b64encode(publickey.exportKey())).decode()
    return exprivatekey, expublickey


def encrypt_message_rsa(a_message, publickey):
    impublickey = RSA.importKey(base64.b64decode(base64.b85decode(publickey.encode())))
    encryptor = PKCS1_OAEP.new(impublickey)
    encrypted_msg = encryptor.encrypt(a_message.encode())
    encoded_encrypted_msg = base64.b85encode(base64.b64encode(encrypted_msg)).decode()
    return encoded_encrypted_msg


def decrypt_message_rsa(encoded_encrypted_msg, privatekey):
    imprivatekey = RSA.importKey(base64.b64decode(base64.b85decode(privatekey.encode())))
    decoded_msg = base64.b64decode(base64.b85decode(encoded_encrypted_msg.encode()))
    decryptor = PKCS1_OAEP.new(imprivatekey)
    decoded_decrypted_msg = decryptor.decrypt(decoded_msg).decode()
    return decoded_decrypted_msg


