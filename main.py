from keygen import makeKeyFiles
import rsa_algorithm
import test
import os
import png
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


if __name__ == '__main__':
    print("RSA")
    if not os.path.exists('publickey.txt') and not os.path.exists('privatekey.txt'):
        keyLength = 1024
        makeKeyFiles(1024)

    filename1 = './images/square.png'
    filename2 = './images/encryptedSquare.png'
    filename3 = './images/decryptedSquare.png'
    # filename4 = './images/dog.png'
    # filename5 = './images/encryptedDog.png'
    # filename6 = './images/decryptedDog.png'

    # getting n and e from publickey
    with open("publickey.txt", "r") as publickey:
        for line in publickey:
            currentline = line.split(",")
            n = int(currentline[1])
            e = int(currentline[2])

    # getting d from privatekey
    with open("privatekey.txt", "r") as privatekey:
        for line in privatekey:
            currentline = line.split(",")
            d = int(currentline[1])

    png.encryptPNG(filename1, filename2, n, e,  64)
    png.decryptPNG(filename2, filename3, n, d)

    img1 = mpimg.imread(filename1)
    img2 = mpimg.imread(filename1)
    img3 = mpimg.imread(filename1)

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
