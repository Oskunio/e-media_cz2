import matplotlib.image as img
import numpy as np

from keygen import getKeyValues
from showImage import showImage

from cbc import CBC
from ecb import ECB
from ecb_lib import ECB_LIB

if __name__ == '__main__':
    print("RSA")
    keyLength = 1024
    n, e, d = getKeyValues(keyLength)

    original_file = './images/japan.png'

    en_ECB_file = './images/encryptedJapanECB.png'
    de_ECB_file = './images/decryptedJapanECB.png'

    en_ECB_lib_file = './images/encryptedJapanECB2.png'
    de_ECB_lib_file = './images/decryptedJapanECB2.png'

    en_CBC_file = './images/encryptedJapanCBC.png'
    de_CBC_file = './images/decryptedJapanCBC.png'

    en_CBC_lib_file = './images/encryptedJapanCBC2.png'
    de_CBC_lib_file = './images/decryptedJapanCBC2.png'

    # LIB CHECK
    ecb = ECB_LIB(original_file, en_ECB_lib_file, de_ECB_lib_file, n, e, d)
    ecb.encryptPNG()
    ecb.decryptPNG()

    # CUSTOM ECB CHECK
    ecb = ECB(original_file, en_ECB_file, de_ECB_file, n, e, d)
    ecb.encryptPNG()
    ecb.decryptPNG()

    # CUSTOM CBC CHECK
    cbc = CBC(original_file, en_CBC_file, de_CBC_file, n, e, d)
    cbc.encryptPNG()
    cbc.decryptPNG()

    # DISPLAYING IMAGES
    showImage(original_file, en_ECB_lib_file,
              de_ECB_lib_file, "ECB using RSA from library")
    showImage(original_file, en_ECB_file, de_ECB_file, "ECB using custom RSA")
    showImage(original_file, en_CBC_file, de_CBC_file, "CBC using custom RSA")
