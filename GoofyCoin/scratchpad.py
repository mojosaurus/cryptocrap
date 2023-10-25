from Goofy import Goofy
from loguru import logger
import sys
import random

"""

"""        
if __name__ == "__main__":
    goofy = Goofy()
    coins = []
    for i in range(5):
        logger.info("***** Iteration {} *********".format(i))
        thisCoin = goofy.createCoin()
        thisCoin.verify(goofy.getPublicKey())
        coins.append(thisCoin)
        logger.info("+++++++ Iteration {} +++++++".format(i))
      
    # Pick a signature at random
    randomCoin = coins[random.choice(range(len(coins)))]
    logger.info("Random Coin : {}".format(randomCoin.signature))
    
    #coin1 = goofy.createCoin()
    #print (coin.verify(goofy.getPublicKey()))
    ishwar = goofy.createUser("ishwar")
    goofy.transferCoin(randomCoin.signature, goofy, ishwar)

    vempa = goofy.createUser("vempa")
    goofy.transferCoin(randomCoin.signature, goofy, vempa)
    goofy.getCoinsByUser(ishwar.getPublicKey())