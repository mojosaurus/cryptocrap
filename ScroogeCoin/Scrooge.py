from ecdsa import SigningKey

import random
import hashlib
from ScroogeChain import ScroogeChain, ScroogeBlock
from ScroogeCoin import ScroogeCoin
import pickle
import json
import codecs

from loguru import logger
import sys
logger.add(sys.stdout, level="TRACE")

class Scrooge:
    """
    Master class for ScroogeCoin ecoystem. This is the central user that controls all transactions
    """
    name        = "scrooge"
    def __init__(self):
        # Using ECDSA digital signature scheme, as discussed in the book.
        # https://www.cs.miami.edu/home/burt/learning/Csc609.142/ecdsa-cert.pdf
        self._privateKey = SigningKey.generate()
        self._publicKey = self._privateKey.verifying_key

        logger.debug("Initializing Scrooge Crypto")
        # Initlializing ScroogeChain. This must be done just once. 
        # TODO : Change this to a Singleton class later to avoid multiple ScroogeChains
        self.scroogeChain = ScroogeChain()


    def getNewTransactionID(self):
        """
        returns a new transaction ID, which is len(self.scroogeChain)+1
        """
        return len(self.scroogeChain.transactions)+1

    def getPublicKey(self):
        return self._publicKey

    def validateCoin(self, scroogeCoin):
        """
        Is this a valid coin
        """
        try:
            isVerified = self._publicKey.verify(scroogeCoin.signature, bytes(scroogeCoin.message, "utf-8"))
            logger.debug ("This is a valid coin. Signed by Scrooge")
        except keys.BadSignatureError:
            logger.error("Invalid coin, bad signature")
            return False
        except AssertionError:
            logger.error("Invalid coin, no signature")
            return False

    def createCoins(self, scroogeCoins):
        """
        Allow multiple coins to be created in the one transaction
        Each coin has a serial number within the transaction.
        Each coin also has a value; it is worth a certain number of scroogeCoins.
        Each coin also has a receipient, which is a publicKey that gets the coin when it's created.
        A coin ID is a combination of a transaction ID and the coin's serial number within that transaction
        """
        logger.info("Starting the transaction")
        transactionID = self.getNewTransactionID()
        logger.info ("New transactionID is {}".format(transactionID))

        for idx, scroogeCoin in enumerate(scroogeCoins):
            scroogeCoin.serialNumber = idx
            scroogeCoin.uuid         = "{}({})".format(transactionID, idx)
            scroogeCoin.message      = "CreateCoin [ {} ]".format(scroogeCoin.uuid)
            scroogeCoin.signature    = self._privateKey.sign_deterministic(bytes(scroogeCoin.message, "utf-8"))

        logger.info("Printing ScroogeCoins info before persisting to ScroogeChain")
        [logger.info(scroogeCoin) for scroogeCoin in scroogeCoins]

        # scroogeCoins is an object. Needs to be converted to bytes and then signed
        transactionSignature = self._privateKey.sign_deterministic(
            pickle.dumps(scroogeCoins)
        )
        # Creating a new transaction
        scroogeBlock = ScroogeBlock(uuid=transactionID, data=scroogeCoins, 
                signature=transactionSignature, transactionType="createCoins")
        
        self.scroogeChain.commit(scroogeBlock)
        self.scroogeChain.validateChain(self._publicKey)


    def payCoins(self, transaction):
        """
        This transaction destroys some coins, and creates new coins of the same total value.
        The new coins might belong to different people (public keys)
        This transcactions have to be signed by everyone who's paying in a coin.
        """
        # 1. The consumed coins are valid, that is, they were really created in the previous transactions
        # 2. The consumed coins were not already consumed in some previous transaction. That is, that is not a double spend
        # 3. The total value of the output coins  is equal to the total value of the coins that went in
        # 4. The transaction is validly signed by the owners of all the consumed coins
        self.validateTransaction(transaction)
        #logger.debug(transaction)

    def validateTransaction(self, transaction):
        # 1. The consumed coins are valid, that is, they were really created in the previous transactions
        # 2. The total value of output coins is equal to the total value of coins that went in
        consumeValue = 0
        consumeCoins = []
        for idx, coin in enumerate(transaction["consume"]):
            thisCoin = self.scroogeChain.findCoinByUUID(coin["uuid"])
            if thisCoin == False:
                logger.error("We don't have a match. Abandon this transaction")
                return False
            
            consumeCoins.append(thisCoin)
            self.validateCoin(thisCoin) # Check if this is a valid coin
            if self.scroogeChain.isCoinConsumed(thisCoin):
                return False
            consumeValue += thisCoin.value
        logger.info("Total value : {}, count of coins : {}".format(consumeValue, len(consumeCoins)))
        
        payValue = 0
        for idx, payNode in enumerate(transaction["pay"]):
            payValue += payNode["value"]
        
        if (consumeValue != payValue):
            logger.error("Total value of output coins is NOT equal to the total value of coins that went in")
            return False

        # The exercise does not mention that all the consumed coins need to be owned by the same user. 
        # So, not checking that part.
        # Secondly, the block Chain gets validate after every transaction. So, not doing that now

        # 2. The consumed coins were not already consumed in some previous transaction. That is, that is not a double spend
        
        # Ok, we are all set now.
        scroogeCoins = []
        for payNode in transaction["pay"]:
            newCoin = ScroogeCoin(value=payNode["value"], recipient=payNode["recipient"])
            scroogeCoins.append(newCoin)

        logger.info("Starting the transaction")
        transactionID = self.getNewTransactionID()
        logger.info ("New transactionID is {}".format(transactionID))

        for idx, scroogeCoin in enumerate(scroogeCoins):
            scroogeCoin.serialNumber = idx
            scroogeCoin.uuid         = "{}({})".format(transactionID, idx)
            scroogeCoin.message      = "CreateCoin [ {} ]".format(scroogeCoin.uuid)
            scroogeCoin.signature    = self._privateKey.sign_deterministic(bytes(scroogeCoin.message, "utf-8"))

        logger.info("Printing ScroogeCoins info before persisting to ScroogeChain")
        [logger.info(scroogeCoin) for scroogeCoin in scroogeCoins]

        # scroogeCoins is an object. Needs to be converted to bytes and then signed
        transactionSignature = self._privateKey.sign_deterministic(
            pickle.dumps(scroogeCoins)
        )
        # Creating a new transaction
        ownerSignatures = {}
        for consumedCoin in consumeCoins:
            ownerSignature = consumedCoin.recipient.getPrivateKey().sign_deterministic(bytes(consumedCoin.message, "utf-8"))
            ownerSignatures[consumedCoin.uuid] = ownerSignature

        scroogeBlock = ScroogeBlock(uuid=transactionID, data=scroogeCoins, 
            signature=transactionSignature, transactionType="payCoins",
            consumedCoinIDs=[consumedCoin.uuid for consumedCoin in consumeCoins],
            signatures = ownerSignatures)

        
        self.scroogeChain.commit(scroogeBlock)
        scroogeBlock.validateBlock(self._publicKey)
        