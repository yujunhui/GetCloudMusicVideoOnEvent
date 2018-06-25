import base64
from Cryptodome.Cipher import AES
import os
import json
import binascii

# 来源: https://blog.csdn.net/tzs_1041218129/article/details/52789153

__all__ = ['encrypt_data']

MODULUS = ('00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7'
           'b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280'
           '104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932'
           '575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b'
           '3ece0462db0a22b8e7')
PUBKEY = '010001'
NONCE = b'0CoJUm6Qyw8W8jud'


def aes(text, key):
    pad = 16 - len(text) % 16
    text = text + bytearray([pad] * pad)
    encryptor = AES.new(key, 2, b'0102030405060708')
    ciphertext = encryptor.encrypt(text)
    return base64.b64encode(ciphertext)


def rsa(text, pubkey, modulus):
    text = text[::-1]
    rs = pow(int(binascii.hexlify(text), 16),
             int(pubkey, 16), int(modulus, 16))
    return format(rs, 'x').zfill(256)


def encrypt_data(dict_data):
    """
    text = {
        "ids": "[\"12A059550A712E4DDB3013DCDE3C92B4\", \"5B0AF067CBB42F7789F7B97E13827565\"]",
        "resolution": "1080",
        "csrf_token": ""
    }
    """
    text = json.dumps(dict_data).encode('utf-8')
    secret = binascii.hexlify(os.urandom(16))[:16]

    params = aes(aes(text, NONCE), secret)
    encSecKey = rsa(secret, PUBKEY, MODULUS)
    data = {
        "params": params.decode(),
        "encSecKey": encSecKey
    }

    return data
