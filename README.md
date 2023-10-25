# cryptocrap
Hands-on exercises, from the book https://github.com/bitcoinbook/bitcoinbook

## Exercise 1 : GoofyCoin
1. Goofy can create new coins by simplly signing the statement that hes making a new coin with a unqiue coin ID
2. Whoever owns a coin can pass it on to someone else by signing a statement that saying, "Pass on this coin to X" where X is specified as a public key
3. Anyone can verify the validity of a coin by following the chain of hash pointers back to its creation by Goofy, verifying all the signatures along the way.

### Limitations
1. Double spending is a problem with GoofyCoin

### TODO
1. Persist the BlockChain
2. Persist user keys on drive

### How to run
1. Create a virtual environment
3. source virtualenvironment file
2. python scratchpad.py