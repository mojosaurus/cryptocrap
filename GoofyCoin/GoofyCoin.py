import random
import string
import hashlib
import CryptoUtils

from ecdsa import SigningKey, VerifyingKey, keys

from loguru import logger
import sys


logger.remove()
logger.add(sys.stdout, level="TRACE")

class GoofyCoin:
    uuid        = ""
    owner       = ""
    message     = ""
    signature   = ""
    def __init__(self, uuid=uuid, owner=owner, message=message, signature=signature):
        # Creates a new coin with the said message and signature
        logger.trace("Creating a new GoofyCoin")
        self.uuid = uuid
        self.owner = owner
        self.message = message
        self.signature = signature

    def __str__(self):
        return ("\n \
            UUID    : {}\n \
            Owner   : {}\n \
            Message : {}\n \
            Signature : {}" \
                .format(self.uuid, self.owner, self.message, self.signature))

    def verify(self, publicKey):
        """
        Check if this is a valid coin, given Goofy's public key
        """
        try:
            isVerified = publicKey.verify(self.signature, bytes(self.message, "utf-8"))
            logger.debug ("This is a valid coin")
        except keys.BadSignatureError:
            logger.error("Invalid, bad signature")
            return False
        except AssertionError:
            logger.error("Invalid, no signature")
            return False
        
        return True