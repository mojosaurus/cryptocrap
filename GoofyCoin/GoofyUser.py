from loguru import logger
import sys
from ecdsa import SigningKey

"""
A user in the Goofy system
"""
logger.add(sys.stdout, level="TRACE")

class GoofyUser:
    name        = None
    def __init__(self, name=""):
        """
        Initiate the user with a private key and a public key
        """
        logger.debug("Creating a new user with name "+name)
        # Using ECDSA digital signature scheme, as discussed in the book.
        # https://www.cs.miami.edu/home/burt/learning/Csc609.142/ecdsa-cert.pdf
        self.name = name
        self._privateKey = SigningKey.generate()
        self._publicKey = self._privateKey.verifying_key
        

    def getPublicKey(self):
        return self._publicKey

    def getPrivateKey(self):
        return self._privateKey

    def myCoins(self):
        """
        Returns the list of coins owned by this user
        Anyone can verify the validity of a coin by following the chain of hash pointers 
        back to its creation by Goofy, verifying signatures all the way
        """
        pass
