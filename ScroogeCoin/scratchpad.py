from Scrooge import Scrooge
from ScroogeUser import ScroogeUser
from ScroogeCoin import ScroogeCoin
from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, level="TRACE")

if __name__ == "__main__":
    scrooge = Scrooge()

    # Create multiple users
    ishwar = ScroogeUser("ishwar")
    vempa = ScroogeUser("vempa")
    karthik = ScroogeUser("karthik")

    coins = [
        ScroogeCoin(value=1, recipient=ishwar),
        ScroogeCoin(value=1, recipient=vempa),
        ScroogeCoin(value=1, recipient=karthik)
    ]

    scrooge.createCoins(coins)

    coins = [
        ScroogeCoin(value=2, recipient=ishwar),
        ScroogeCoin(value=2, recipient=vempa),
        ScroogeCoin(value=2, recipient=karthik)
    ]

    scrooge.createCoins(coins)

    coins = [
        ScroogeCoin(value=3, recipient=ishwar),
        ScroogeCoin(value=3, recipient=vempa),
        ScroogeCoin(value=3, recipient=karthik)
    ]

    scrooge.createCoins(coins)