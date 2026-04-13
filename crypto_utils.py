from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

import os

# ------------------------RSA

def generate_rsa_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size = 2048)
    public_key = private_key.public_key()
    return private_key, public_key

def serialize_public_key(public_key):
    return public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                   format=serialization.PublicFormat.SubjectPublicKeyInfo)


def load_public_key(pem_data):
    return serialization.load_pem_public_key(pem_data)


def rsa_encrypt(data, public_key):
    return public_key.encrypt( data, padding.OAEP( mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                   algorithm=hashes.SHA256(), label=None ))


def rsa_decrypt(cipher, private_key):
    return private_key.decrypt( cipher, padding.OAEP( mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                      algorithm=hashes.SHA256(), label=None ) )

#------------------------AES

def generate_aes_key():
    return AESGCM.generate_key(256)

def aes_encrypt(key, data):
    aes = AESGCM(key)
    nonce = os.urandom(12)
    cipher = aes.encrypt(nonce,data,None)
    return nonce+cipher

def aes_decrypt(key, data):
    aes = AESGCM(key)
    nonce = data[:12]
    cipher = data[12:]
    return aes.decrypt(nonce, cipher, None)






