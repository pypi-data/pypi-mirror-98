# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import base64
import rncryptor
import logging
from nimbus_utils.encoding import smart_str, smart_bytes

__all__ = ["aescryptor", "rncryptor", "RNCryptor"]

logger = logging.getLogger("encrypt")


class RNCryptor(rncryptor.RNCryptor):
    """
    加密解密
    MODE: CBC
    PADDING: PKCS#7
    SALT: 8
    """
    def encrypt(self, data, password):
        try:
            endata = super(RNCryptor, self).encrypt(data=data, password=password)
        except rncryptor.RNCryptorError as e:
            logger.error(e)
            endata = ""
        return endata

    def decrypt(self, data, password):
        try:
            dedata = super(RNCryptor, self).decrypt(data=data, password=password)
        except rncryptor.DecryptionError as e:
            logger.error(e)
            dedata = ""
        return dedata

    def pre_encrypt_data(self, data):
        data = smart_bytes(data)
        return super(RNCryptor, self).pre_encrypt_data(data)

    def post_encrypt_data(self, data):
        endata = super(RNCryptor, self).post_encrypt_data(data)
        endata = smart_bytes(endata)
        return smart_str(base64.urlsafe_b64encode(endata))

    def pre_decrypt_data(self, data):
        data = base64.urlsafe_b64decode(smart_bytes(data))
        data = smart_bytes(data)
        return super(RNCryptor, self).pre_decrypt_data(data)

    def post_decrypt_data(self, data):
        dedata = super(RNCryptor, self).post_decrypt_data(data)
        return smart_str(dedata)


aescryptor = RNCryptor()

