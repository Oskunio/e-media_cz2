from keygen import makeKeyFiles
import rsa_algorithm
import test
import os
import png
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


if __name__ == '__main__':
    print("RSA")
    keyLength = 1024
    if not os.path.exists('publickey.txt') and not os.path.exists('privatekey.txt'):
        makeKeyFiles(keyLength)

    filename1 = './images/square.png'
    filename2 = './images/encryptedSquare.png'
    filename3 = './images/decryptedSquare.png'
    # filename1 = './images/dog.png'
    # filename2 = './images/encryptedDog.png'
    # filename3 = './images/decryptedDog.png'

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

    blockSize = int((keyLength / 8) - 42)
    png.encryptPNG(filename1, filename2, n, e,  blockSize)
    png.decryptPNG(filename2, filename3, n, d)

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
