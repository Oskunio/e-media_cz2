import keygen
import png

filename1 = './images/Square.png'
filename2 = './images/newSquare.png'
filename3 = './images/dog.png'
filename4 = './images/newDog.png'
filename5 = './images/tygrys.png'
filename6 = './images/newTygrys.png'

keyLength = 10
key = keygen.generateKey(keyLength)
publicKey = key[0]
privateKey = key[1]
n = publicKey[0]
e = publicKey[1]

png.encryptPNG(filename1, filename2, n, e, keyLength)
png.encryptPNG(filename3, filename4, n, e, keyLength)
png.encryptPNG(filename5, filename6, n, e, keyLength)


