from ecdsa import SigningKey
from loguru import logger
import sys

logger.add(sys.stdout, level="TRACE")

class ScroogeUser:
    name        = None
    def __init__(self, name=""):
        """
        Initiate the user with a private key and a public key
        """
        logger.debug("Creating a new user with name {}".format(name))
        # Using ECDSA digital signature scheme, as discussed in the book.
        # https://www.cs.miami.edu/home/burt/learning/Csc609.142/ecdsa-cert.pdf
        self.name = name
        self._privateKey = SigningKey.generate()
        self._publicKey = self._privateKey.verifying_key
        

    def getPublicKey(self):
        return self._publicKey

    def getPrivateKey(self):
        return self._privateKey

    def verifyTransaction(self):
        """
        Anybody can verify that a transaction(ScroogeBlock) was endorsed by Scrooge by checking Scrooge's signature
        on the block that it appears in
        """
        pass
