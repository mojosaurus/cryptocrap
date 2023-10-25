import string
import random

def generate_random_string(length):
    """
    Generates a random string of a given length .

    args:
        length : The length of the random string to be generated
    return:
        generated random string
    """
    # The list of allowed characters
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(random.choice(characters) for i in range(length))
    return random_string


if __name__ == "__main__":
    print (generate_random_string(256))