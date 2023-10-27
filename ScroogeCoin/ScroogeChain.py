import hashlib
from ecdsa import SigningKey, VerifyingKey, keys
import pickle

from loguru import logger
import sys

logger.add(sys.stdout, level="TRACE")

class ScroogeBlock:
    """
    Each block in ScroogeChain is  transaction
    """
    uuid        =   ""
    hashPointer = None
    data        = None
    signature   = None

    def __init__(self, uuid=uuid, data=data, signature=signature):
        self.uuid = uuid
        self.data = data
        self.signature = signature
        logger.debug ("Creating a new GoofyBlock {}".format(self))

    def validateBlock(self, publicKey):
        """
        Is this a valid block - is this block signed by Scrooge?
        """
        
        try:
            isVerified = publicKey.verify(self.signature, pickle.dumps(self.data))
            logger.debug ("This is a valid block. Signed by Scrooge")
        except keys.BadSignatureError:
            logger.error("Invalid, bad signature")
            return False
        except AssertionError:
            logger.error("Invalid, no signature")
            return False
        
        return True

    def __str__(self):
        return """ \
                uuid        :   {} \
                hashPointer :   {} \
                data        :   {} \
                signature   :   {}  \
            """.format(self.uuid, self.hashPointer, self.data, self.signature)

class ScroogeChain:
    transactions = []
    """
    ScroogeChain is a series of ScroogeBlocks, each with one transaction in it.
    Each block has the id of the transcation (uuid)
    transaction contents (data)
    and a hashPointer to the previous block.
    Scrooge digitally signs the final hash pointer, which binds all of the data in this entire structure
    and publishes the signature along with the block chain
    """
    def __init__(self):
        logger.debug("Initializing ScroogeChain")
    
    def commit(self, scroogeBlock):
        """
        Commit scroogeBlock to the ScroogeChain
        """

        if len(self.transactions) == 0:
            logger.debug ("This is the Genesis block. Setting the HashPointer as genesis block")
            scroogeBlock.hashPointer = "genesis block"
        else:
            # Get the previous block's signature
            logger.debug ("Not a genesis block")
            previousCoinSignature = self.transactions[len(self.transactions)-1].signature
            
            # Calculate the hash of the previous block's signature
            m = hashlib.sha256()
            m.update(previousCoinSignature)
            scroogeBlock.hashPointer = m.digest()

        self.transactions.append(scroogeBlock)
        logger.debug("Length of the BlockChain : {}".format(len(self.transactions)))

    def validateChain(self, publickKey):
        """
        This function validates the BlockChain
        """
        logger.info("Validating the current block chain")
        
        lastHashPointer = self.transactions[-1].hashPointer
        logger.debug("Last hashPointer : {}".format(lastHashPointer))

        # All chains need to validate their first transaction.
        self.transactions[0].validateBlock(publickKey)

        for idx, blockNode in enumerate(list(reversed(self.transactions))[1:]):
            logger.info("Validating the chain Iteration : {}".format(idx))
            thisSignature = blockNode.signature

            m = hashlib.sha256()
            m.update(thisSignature)
            checkHashPointer = m.digest()
            if (lastHashPointer == checkHashPointer):
                logger.debug("We have a match")
            else :
                logger.error("Tough luck")

            # Update lastHashPointer to, well, the last one
            lastHashPointer = blockNode.hashPointer
            blockNode.validateBlock(publickKey)

    def __str__(self):
        return "\n".join([transaction in self.transactions])