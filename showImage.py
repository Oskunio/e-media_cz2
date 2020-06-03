import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def showImage(filename1, filename2, filename3, title):
    img1 = mpimg.imread(filename1)
    img3 = mpimg.imread(filename3)

    fig = plt.figure()
    a = fig.add_subplot(1, 3, 1)
    fig.suptitle(title, fontsize=16)

    try:
        img2 = mpimg.imread(filename2)
        a = fig.add_subplot(1, 3, 2)
        a.set_title("Encrypted image")
        imgplot = plt.imshow(img2)
    except RuntimeError as e:
        print('Caught RuntimeError', e)

    a.set_title("Image")
    imgplot = plt.imshow(img1)
    a = fig.add_subplot(1, 3, 3)
    a.set_title("Decrypted image")
    imgplot = plt.imshow(img3)
    plt.show()
