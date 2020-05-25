from keygen import makeKeyFiles
import rsa_algorithm
import os
import png
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


if __name__ == '__main__':
    print("RSA")
    keyLength = 1024
    if not os.path.exists('publickey.txt') and not os.path.exists('privatekey.txt'):
        makeKeyFiles(keyLength)

    #filename1 = './images/square.png'
    #filename2 = './images/encryptedSquare.png'
    #filename3 = './images/decryptedSquare.png'
    #filename1 = './images/dog.png'
    #filename2 = './images/encryptedDog.png'
    #filename3 = './images/decryptedDog.png'
    filename1 = './images/chmura.png'
    filename2 = './images/encryptedChmura.png'
    filename3 = './images/decryptedChmura.png'
    # getting n and e from publickey.txt
    with open("publickey.txt", "r") as publickey:
        for line in publickey:
            currentline = line.split(",")
            n = int(currentline[1])
            e = int(currentline[2])

    # getting d from privatekey.txt
    with open("privatekey.txt", "r") as privatekey:
        for line in privatekey:
            currentline = line.split(",")
            d = int(currentline[1])
    print('key:',n)
    print('dlugosc klucza',len(str(n)))
    liczba = 123451234512345123451234512345123451234511111111111111111111111111111111111111111111111111111111111135
    zaszyfrowana = rsa_algorithm.encrypt(liczba,n,e)
    odszyfrowana = rsa_algorithm.decrypt(zaszyfrowana,n,d)

    blockSize = int((keyLength / 8) - 42)
    png.encryptPNG(filename1, filename2, n, e,  blockSize)
    png.decryptPNG(filename2, filename3, n, d, blockSize)

    """
    img1 = mpimg.imread(filename1)
    img2 = mpimg.imread(filename2)  # 2 instead of 1
    img3 = mpimg.imread(filename3)  # 3 instead of 1

    fig = plt.figure()
    a = fig.add_subplot(1, 3, 1)
    a.set_title("Image")
    imgplot = plt.imshow(img1)
    a = fig.add_subplot(1, 3, 2)
    a.set_title("Encrypted image")
    imgplot = plt.imshow(img2)
    a = fig.add_subplot(1, 3, 3)
    a.set_title("Decrypted image")
    imgplot = plt.imshow(img3)
    plt.show()
"""