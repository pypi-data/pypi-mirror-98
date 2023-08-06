# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import re
import os
import json
import uuid
import time
import hmac
import base64
import hashlib
import logging
from dateutil import parser
from datetime import datetime
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Protocol import KDF
from .utils import bord, bchr, to_str, to_bytes, smart_str, smart_bytes
from .base import AESCryptor, AESBinCryptor, CryptorError, DecryptionError


class AESEAXCryptor(AESCryptor):
    mode = AES.MODE_EAX

    def __init__(self, key, nonce=None, tag=None):
        super().__init__(key)
        self.nonce = nonce
        self.tag = tag

    def aes_encrypt(self, key, data, *args, **kwargs):
        cipher = AES.new(key, self.mode)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        self.tag = tag
        self.nonce = cipher.nonce
        return ciphertext

    def aes_decrypt(self, key, data, *args, **kwargs):
        _nonce = self._base64_decode(self.nonce)
        _tag = self._base64_decode(self.tag)
        cipher = AES.new(key, self.mode, _nonce)
        _data = cipher.decrypt_and_verify(data, _tag)
        return _data

    def post_encrypt_data(self, data):
        _data = super().post_encrypt_data(data)
        _nonce = self._base64_encode(self.nonce)
        _tag = self._base64_encode(self.tag)
        return _data, _nonce, _tag

    def post_decrypt_data(self, data):
        return super().post_decrypt_data(data)


def generate_key(size=16):
    return AESEAXCryptor.generate_key(size=size)


generate_key.__doc__ = AESEAXCryptor.generate_key.__doc__


def decrypt(data, key, nonce=None, tag=None):
    cryptor = AESEAXCryptor(key=key, nonce=nonce, tag=tag)
    return cryptor.decrypt(data, key)


decrypt.__doc__ = AESEAXCryptor.decrypt.__doc__


def encrypt(data, key, nonce=None, tag=None):
    cryptor = AESEAXCryptor(key=key, nonce=nonce, tag=tag)
    return cryptor.encrypt(data, key)


encrypt.__doc__ = AESEAXCryptor.encrypt.__doc__
