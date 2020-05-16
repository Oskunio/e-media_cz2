import keygen
import png
import rsa_algorithm

filename1 = './images/Square.png'
filename2 = './images/encryptedSquare.png'
filename3 = './images/decryptedSquare.png'
filename4 = './images/Dog.png'
filename5 = './images/encryptedDog.png'
filename6 = './images/decryptedDog.png'

keyLength = 512
key = keygen.generateKey(keyLength)
publicKey = key[0]
privateKey = key[1]
n = publicKey[0]
e = publicKey[1]

liczba = 10

zakodowana = rsa_algorithm.encrypt(liczba,n,e)
odkodowana = rsa_algorithm.decrypt(zakodowana,privateKey,e)

print('odkodowana:')
print(odkodowana)



png.encryptPNG(filename1, filename2, n, e,  64)
png.decryptPNG(filename2, filename3, privateKey, e)
#png.encryptPNG(filename4, filename5, n, e,  64)
#png.decryptPNG(filename5, filename6, privateKey, e)


