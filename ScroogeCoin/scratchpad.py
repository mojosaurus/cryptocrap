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
    
    coins_1 = [
        ScroogeCoin(value=1, recipient=ishwar),
        ScroogeCoin(value=1, recipient=vempa),
        ScroogeCoin(value=1, recipient=karthik)
    ]

    scrooge.createCoins(coins_1)

    coins_2 = [
        ScroogeCoin(value=2, recipient=ishwar),
        ScroogeCoin(value=2, recipient=vempa),
        ScroogeCoin(value=2, recipient=karthik)
    ]

    scrooge.createCoins(coins_2)
    
    coins_3 = [
        ScroogeCoin(value=1, recipient=ishwar),
        ScroogeCoin(value=1, recipient=vempa),
        ScroogeCoin(value=1, recipient=karthik)
    ]

    scrooge.createCoins(coins_3)

    # Let's take a simple example of destroying coin 3(3) of value 3 and creating 3 coins with value 1 each
    # and assigning it to the same user
    scroogeTransaction = {
        "consume" : [
            {"uuid" : "1(0)"},
            {"uuid" : "1(1)"}
        ],
        "pay"  : [
            {"value" : 1, "recipient" : ishwar},
            {"value" : 1, "recipient" : ishwar},
            #{"value" : 4, "recipient" : ishwar}
        ]
    }
    scrooge.payCoins(scroogeTransaction)

    duplicateTransaction = {
        "consume" : [
            {"uuid" : "1(1)"}
        ],
        "pay" : [
            {"value" : 1, "recipient" : vempa}
        ]
    }
    scrooge.payCoins(duplicateTransaction)