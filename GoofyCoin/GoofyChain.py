from loguru import logger
import sys
import hashlib


logger.remove()
logger.add(sys.stdout, level="TRACE")

class GoofyBlock:
    """
    Building block of GoofyChain
    """
    hashPointer = None
    data        = None
    def __init__(self, data):
        logger.info ("Creating a new GoofyBlock with the following data : {}".format(data))
        self.data = data

class GoofyChain:
    """
    A basic implementation of BlockChain for GoofyCoin
    """
    def __init__(self):
        logger.debug("Initializing GoofyChain. Length 0")
        self._chain = []

    def append(self, obj):
        block = GoofyBlock(obj)
        if len(self._chain) == 0:
            logger.debug ("This is the Genesis block. Setting the HashPointer as genesis block")
            block.hashPointer = "genesis block"
        else:
            # Get the previous block's signature
            logger.debug ("Not a genesis block")
            previousCoinSignature = self._chain[len(self._chain)-1].data.signature
            
            # Calculate the hash of the previous block's signature
            m = hashlib.sha256()
            m.update(previousCoinSignature)
            block.hashPointer = m.digest()

        block.data = obj
        self._chain.append(block)
        logger.debug("Length of the BlockChain : {}".format(len(self._chain)))
        #self.validateChain()

    def validateChain(self):
        """
        This function validates the BlockChain
        """
        logger.trace("Validating the current block chain")
        
        lastHashPointer = self._chain[-1].hashPointer
        logger.debug("Last hashPointer : {}".format(lastHashPointer))
        
        for idx, blockNode in enumerate(list(reversed(self._chain))[1:]):
            logger.info("Validating the chain Iteration : {}".format(idx))
            
            thisSignature = blockNode.data.signature

            m = hashlib.sha256()
            m.update(thisSignature)
            checkHashPointer = m.digest()
            if (lastHashPointer == checkHashPointer):
                logger.debug("We have a match")
            else :
                logger.error("Tough luck")

            # Update lastHashPointer to, well, the last one
            lastHashPointer = blockNode.hashPointer

    def findCoinBySignature(self, coinSignature):
        for idx, goofyNode in enumerate(self._chain):
            logger.info("Searching for {}".format(coinSignature))
            if goofyNode.data.signature == coinSignature:
                logger.info("Excellent. Found the match. Returning")
                return goofyNode.data

    def findCoinsByUser(self, userPublicKey):
        logger.info("Searching for coins by {}".format(str(userPublicKey)))
        ret = []
        for idx, goofyNode in enumerate(self._chain):
            if goofyNode.data.verify(userPublicKey):
                logger.debug("Found a match by the user")
                ret.append(goofyNode)
            else:
                logger.debug("Not a match")

        return ret

    def __str__(self):
        # Printing the BlockChain
        ret = []
        for idx, blockNode in enumerate(self._chain):
            ret.append("Node in blockChain : {}".format(blockNode.data))
        return "\n".join(ret)