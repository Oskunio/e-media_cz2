

# Encrypt
# message - the 'message' to be encoded
# n - public key(part 1)
# e - public key(part 2)
# returns encrypted message
def encrypt(m, n, e):
    print("Encription\n")
    return pow(m, e, n)


# Decrypt
# message - the 'message' to be decoded
# n - private key
# e - public key(part 1)
# returns decrypted message
def decrypt(c, d, n):
    print("Decription\n")
    return pow(c, d, n)
