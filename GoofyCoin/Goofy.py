from ecdsa import SigningKey
import CryptoUtils
from GoofyCoin import GoofyCoin
from GoofyChain import GoofyChain
from GoofyUser import GoofyUser

from loguru import logger
import sys
import random
import hashlib


logger.remove()
logger.add(sys.stdout, level="TRACE")

class Goofy:
    """
    Master class Goofy.
    """
    name        = "goofy"
    goofyChain  = GoofyChain()
    def __init__(self):

        # Using ECDSA digital signature scheme, as discussed in the book.
        # https://www.cs.miami.edu/home/burt/learning/Csc609.142/ecdsa-cert.pdf
        self._privateKey = SigningKey.generate()
        self._publicKey = self._privateKey.verifying_key

        logger.debug("Initializing Goofy Crypto")

        # TODO 1 : Create a [Private Key, Public Key] combo for persistence
        # TODO 2 : Persist the Blockchain

    def getPublicKey(self):
        return self._publicKey


    def createCoin(self):
        """
        To a coin, Goofy 
        1. generates a unique coin ID uniqueCoinID that he's never generate before
        2. constucts the string CreateCoin[uniqueCoinID]
        3. He the computes the digital signature of this string with his secret signing key.
        The string, together with Goofy's signature is a coin.
        """

        # 1. Create a unique coin id
        uniqueCoinID = CryptoUtils.generate_random_string(256)

        # 2. Construct the string CreateCoin [uniqueCoinID]
        msgString = "CreateCoin [" + uniqueCoinID + "]"

        # 3. Compute the digital signature with Goofy's Private Key
        signature = self._privateKey.sign_deterministic(bytes(msgString, "utf-8"))

        # 4. The string, together with Goofy's signature is a coin
        newCoin =  GoofyCoin(uuid=uniqueCoinID, owner=self.getPublicKey(), message=msgString, signature=signature)
        logger.debug("Created a goofycoin  {}".format(newCoin))
        # 5. Append to the Blockchain
        self.goofyChain.append(newCoin)

        return newCoin


    def createUser(self, name=''):
        gUser = GoofyUser(name)
        return gUser
        #self.goofyChain.append(gUser)

    def transferCoin(self, coinSignature, sourceUser, targetUser):
        """
        Transfers the coin specified by coinSignature from sourceUser to targetUser
        """
        # 1. Find the coin with the right signature in the GoofyChain
        thisCoin = self.goofyChain.findCoinBySignature(coinSignature)

        # 1. Calculate the SHA256 hash of the signature
        m = hashlib.sha256()
        m.update(coinSignature)
        message = "Pay " + str(m.digest()) + " to " + str(targetUser.getPublicKey())
        logger.debug("Attempting to {}".format(message))

        # 2. Sign this with Target User's private key
        #signature = self._privateKey.sign_deterministic(bytes(message, 'utf-8'))
        signature = targetUser.getPrivateKey().sign_deterministic(bytes(message, "utf-8"))
        
        newCoin = GoofyCoin(uuid=thisCoin.uuid, owner=targetUser.getPublicKey(), message=message, signature=signature)
        newCoin.verify(targetUser.getPublicKey())
        self.goofyChain.append(newCoin)
        logger.info(self.goofyChain)

    def getCoinsByUser(self, userPublicKey):
        """
        Returns the list of coins currently owned by the user with the given Public Key.
        God knows how this will be done 
        """
        self.goofyChain.findCoinsByUser(userPublicKey)