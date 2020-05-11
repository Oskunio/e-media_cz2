from Crypto.Util import number


def generateKey(length):
    print("Key generator")
    print("Random prime number")
    return number.getPrime(length)
