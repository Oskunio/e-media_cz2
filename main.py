import png

from keygen import getKeyValues
from libCheck import libCheck, rsaLibImage
from showImage import showImage

if __name__ == '__main__':
    print("RSA")
    keyLength = 1024
    n, e, d = getKeyValues(keyLength)

    filename1 = './images/japan.png'
    filename2 = './images/encryptedJapan.png'
    filename3 = './images/decryptedJapan.png'
    filename4 = './images/encryptedJapan2.png'
    filename5 = './images/decryptedJapan2.png'

    print("Lib RSA is working for small messages: ", libCheck(n, e, d))

    # szyfrowanie implementowanym rsa
    png.encryptPNG(filename1, filename2, n, e)
    png.decryptPNG(filename2, filename3, n, d)

    showImage(filename1, filename2, filename3)

    # szyfrowanie rsa z bilbioteki
    rsaLibImage(n, e, d, filename1, filename4, filename5)
    showImage(filename1, filename4, filename5)
