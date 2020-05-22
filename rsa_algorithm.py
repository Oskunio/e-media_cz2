

# Encrypt
# m - the 'message' to be encoded
# n - public key(part 1)
# e - public key(part 2)
# returns encrypted message
def encrypt(m, n, e):
    return pow(m, e, n)


# Decrypt
# c - the 'cipher' to be decoded
# n - public key(part 1)
# d - private key
# returns decrypted message
def decrypt(c, n, d):
    return pow(c, d, n)
